# trunk-ignore-all(pylint/C0114)
# trunk-ignore-all(pylint/E0401)
import os

from notion_client import AsyncClient

NOTION_CONFIG = os.environ


def get_notion_client() -> AsyncClient:
    print(
        f"""\
                Notion API loaded... 
                INTEGRATION_TOKEN: {NOTION_CONFIG['INTEGRATION_TOKEN']}
                """
    )

    return AsyncClient(auth=NOTION_CONFIG["INTEGRATION_TOKEN"])


def get_database_id(table_name: str) -> str:
    return NOTION_CONFIG[f"{table_name}_DB_ID"]


async def notion_create(obj):
    if getattr(obj, "__notion_db_name__", None) is None:
        raise TypeError(
            "Object must be a dataclass decorated with @notion_object with a valid name to be added to notion table"
        )

    database_id: str = get_database_id(obj.__notion_db_name__)
    client: AsyncClient = get_notion_client()

    response = await client.pages.create(
        parent={"database_id": database_id}, properties=obj.notion_dict
    )

    return response


async def notion_query_producers(discord_id: str):
    """
    Currently supported kwargs: 'discord_id'
    """
    db_id: str = get_database_id("PRODUCER")
    client: AsyncClient = get_notion_client()

    response = await client.databases.query(
        **{
            "database_id": db_id,
            "filter": {"property": "discord_id", "rich_text": {"contains": discord_id}},
        }
    )

    result = response.get("results")
    if len(result) == 0:
        return None
    return result
