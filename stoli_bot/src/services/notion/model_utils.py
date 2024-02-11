import traceback
from dataclasses import fields, is_dataclass, Field
from enum import StrEnum, auto
from typing import Callable, Optional
from functools import reduce, partial


class NotionDatatype(StrEnum):
    TITLE = auto()
    RICH_TEXT = auto()
    NUMBER = auto()
    FILES = auto()


CONVERTERS: dict[NotionDatatype, Callable] = {}
RESPONSE_PARSERS: dict[NotionDatatype, Callable] = {}


def converter(notion_type: NotionDatatype):
    global CONVERTERS

    def register(converter: Callable) -> Callable:
        CONVERTERS[notion_type] = converter
        return converter

    return register


def response_parser(notion_type: NotionDatatype):
    global RESPONSE_PARSERS

    def register(response_parser: Callable) -> Callable:
        RESPONSE_PARSERS[notion_type] = response_parser
        return response_parser

    return register


@converter(NotionDatatype.TITLE)
def title(text: str) -> dict:
    return {'title': [{'text': {'content': text}}]}


@converter(NotionDatatype.RICH_TEXT)
def rich_text(text: str) -> dict:
    return {'rich_text': [{'text': {'content': text}}]}


@converter(NotionDatatype.NUMBER)
def number(value: int | float) -> dict:
    return {'number': value}


@converter(NotionDatatype.FILES)
def files(url: str) -> dict:
    return {'files': [{'name': str(url), 'external': {'url': str(url)}}]}


@response_parser(NotionDatatype.TITLE)
def title(property_name: str, properties: dict) -> str | None:  # noqa: F811
    prop: dict | None = properties.get(property_name, None)
    if prop is None:
        raise ValueError('Nonexistent property/field on notion object')

    prop_list: list[dict] = prop[prop['type']]  # for some reason actual value is stored under key of type
    if len(prop_list) == 0:
        return None
    else:
        item: dict = prop_list[0]
        plain_text: str = item['plain_text']
        return plain_text


@response_parser(NotionDatatype.RICH_TEXT)
def rich_text(property_name: str, properties: dict) -> str | None:  # noqa: F811
    prop: dict | None = properties.get(property_name, None)
    if prop is None:
        raise ValueError('Nonexistent property/field on notion object')

    prop_list: list[dict] = prop[prop['type']]  # for some reason actual value is stored under key of type
    if len(prop_list) == 0:
        return None
    else:
        item: dict = prop_list[0]
        plain_text: str = item['plain_text']
        return plain_text


@response_parser(NotionDatatype.NUMBER)
def number(property_name: str, properties: dict) -> int | float | None:  # noqa: F811
    prop: dict | None = properties.get(property_name, None)
    if prop is None:
        raise ValueError('Nonexistant property / field on notion object')

    num: int | float | None = prop.get('number', None)
    return num


@response_parser(NotionDatatype.FILES)
def files(property_name: str, properties: dict) -> str | None:  # noqa: F811
    prop: dict | None = properties.get(property_name, None)
    if prop is None:
        raise ValueError('Nonexistant property / field on notion object')

    prop_list: list[dict] = prop['files']

    if len(prop_list) == 0:
        return None

    else:
        item: dict = prop_list[0]
        url = item['external']['url']
        return url


def notion_metadata(
        property_type: NotionDatatype,
        converter: Optional[Callable] = None,
        response_parser: Optional[Callable] = None
) -> dict:
    if not converter:
        global CONVERTERS, RESPONSE_PARSERS

        if default_converter := CONVERTERS.get(property_type, None):
            converter = default_converter

        else:
            raise ValueError(f'No default converter for property type: {property_type}')

        if default_parser := RESPONSE_PARSERS[property_type]:
            response_parser = default_parser

        else:
            raise ValueError(f'No default response parser for property type: {property_type}')

    return {'notion': {'property_type': property_type, 'converter': converter, 'response_parser': response_parser}}


def notion_object(object_name: str):
    def _field_to_notion_dict(instance, field: Field) -> dict:
        if (notion_meta := field.metadata.get('notion')) and (
                (value := getattr(instance, field.name, None)) is not None):
            try:
                return {field.name: notion_meta['converter'](value)}

            except Exception as e:
                traceback.print_exc(limit=3)
                raise e

        else:
            return {}

    def _unify_dicts(dict1: dict, dict2: dict) -> dict:
        return dict1 | dict2

    def _cls_to_notion_dict(instance) -> dict[str, dict]:
        return reduce(
            _unify_dicts,
            map(partial(_field_to_notion_dict, instance), fields(instance)),
            {}
        )

    def _field_from_notion_response(field: Field, response: dict):
        notion_meta = field.metadata.get('notion')
        if notion_meta and (property_name := field.name):
            parser = notion_meta['response_parser']
            try:
                properties = response.get('properties', {})
                return {field.name: parser(property_name, properties)}
            except Exception as e:
                traceback.print_exc(limit=3)
                raise ValueError(f"Error parsing field '{field.name}': {e}")
        return {}

    def _cls_from_notion_response(cls, response: dict):
        kwargs = reduce(
            _unify_dicts,
            map(partial(_field_from_notion_response, response=response), fields(cls)),
            {}
        )
        return cls(**kwargs)

    def wrapper(cls: type):
        if not is_dataclass(cls):
            raise TypeError('Only dataclasses may be made notion_convertible')

        cls.__notion_db_name__ = object_name

        @property
        def notion_dict(self):
            return _cls_to_notion_dict(self)

        @classmethod # noqa
        def from_query(__cls, response: dict) -> object:
            return _cls_from_notion_response(__cls, response)

        setattr(cls, 'notion_dict', notion_dict)
        setattr(cls, 'from_query', from_query)

        return cls

    return wrapper
