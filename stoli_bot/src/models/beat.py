from dataclasses import dataclass, field
from stoli_bot.src.services.notion.model_utils import (
    NotionDatatype,
    notion_metadata,
    notion_object,
)


@notion_object(object_name='BEAT')
@dataclass
class Beat:
    title: str = field(
        metadata=notion_metadata(NotionDatatype.TITLE)
    )

    producer_name: str = field(
        metadata=notion_metadata(NotionDatatype.RICH_TEXT)
    )

    link: str = field(
        metadata=notion_metadata(NotionDatatype.FILES)
    )

    key: str | None = field(
        default=None, metadata=notion_metadata(NotionDatatype.RICH_TEXT)
    )

    detune: float | None = field(
        default=None, metadata=notion_metadata(NotionDatatype.NUMBER)
    )

    bpm: float | None = field(
        default=None, metadata=notion_metadata(NotionDatatype.NUMBER)
    )

