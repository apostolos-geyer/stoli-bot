import os
import asyncio
from typing import Optional

from notion_client import AsyncClient


class NotionService:
    def __init__(self):
        self.client: AsyncClient = AsyncClient(auth=os.getenv('NOTION_INTEGRATION_TOKEN'))
        print(
            f"""\
            Notion API loaded... 
            INTEGRATION_TOKEN: {os.getenv('NOTION_INTEGRATION_TOKEN')}
            V2_TOKEN: {os.getenv('NOTION_V2_TOKEN')}
            DB_ID: {os.getenv('NOTION_DB_ID')}
            """
        )

    @staticmethod
    def beat_db_entry(
            title: str,
            producer: str,
            url: str,
            key: str,
            detune: Optional[int] = None,
            bpm: int = None,
    ) -> dict:
        """Returns a dictionary representing a notion database entry in the beats database"""
        return {
            "title": {
                "title": [{"text": {"content": title}}]
            },

            "producer": {
                "rich_text": [
                    {"text": {"content": producer}}
                ]
            },

            "link": {
                "files": [
                    {
                        "name": title,
                        "external": {
                            "url": url
                        }
                    }
                ]
            },

            "key": {
                "rich_text": [
                    {"text": {"content": key}}
                ]
            },

            "detune": {
                "number": detune
            },

            "bpm": {
                "number": bpm
            }
        }

    async def create_beat_entry(self, title: str, producer: str, url: str, key: str, detune: int, bpm: int):
        response = await self.client.pages.create(
            parent={
                "database_id": os.getenv('NOTION_DB_ID')
            },
            properties=self.beat_db_entry(
                title=title,
                producer=producer,
                url=url,
                key=key,
                detune=detune,
                bpm=bpm,
            )
        )

        print(response)
        return response
