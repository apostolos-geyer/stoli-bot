from dataclasses import dataclass, field
from stoli_bot.src.services.notion.model_utils import (
    NotionDatatype,
    notion_metadata,
    notion_object,
)

@notion_object(object_name='PRODUCER')
@dataclass
class Producer:
    name: str = field(
        metadata=notion_metadata(NotionDatatype.TITLE)
    )

    discord_id: str = field(
        metadata=notion_metadata(NotionDatatype.RICH_TEXT)
    )

    email: str | None = field(
        metadata=notion_metadata(NotionDatatype.RICH_TEXT), default=None
    )

    instagram: str | None = field(
        metadata=notion_metadata(NotionDatatype.RICH_TEXT), default=None
    )

    tiktok: str | None = field(
        metadata=notion_metadata(NotionDatatype.RICH_TEXT), default=None
    )

    x: str | None = field(
        metadata=notion_metadata(NotionDatatype.RICH_TEXT), default=None
    )

    youtube: str | None = field(
        metadata=notion_metadata(NotionDatatype.RICH_TEXT), default=None
    )