from interactions import Extension, SlashContext, SlashCommand, Attachment
from typing import Optional
import os

from .options import title, producer, key, detune, bpm, beat_url, beat_file

from stoli_bot.src.services.notion import NotionService


class Beats(Extension):
    """Commands used to send beats to the bot for usage by Apostoli"""

    print(f'loaded extension from beats/extension.py, TESTING_GUILD: {os.getenv('DISCORD_TESTING_GUILD')}')

    beats_base = SlashCommand(name='beats', description='Send a beat to Apostoli',
                              scopes=[os.getenv('DISCORD_TESTING_GUILD')])

    send_beat = beats_base.group(name='send', description='Send a beat to Apostoli')

    @send_beat.subcommand(sub_cmd_name='file', sub_cmd_description='Send a beat file to Apostoli')
    @title()
    @producer()
    @beat_file()
    @key()
    @detune()
    @bpm()
    async def send_beat_file(
            self,
            ctx: SlashContext,
            title: str,
            producer: str,
            file: Attachment,
            key: str,
            detune: Optional[int] = None,
            bpm: Optional[int] = None,
    ):
        """Send a beat file to Apostoli"""

        notion = NotionService()
        response = await notion.create_beat_entry(title, producer, file.url, key, detune, bpm)

        msg = f"""\
                CURRENTLY NOT IMPLEMENTED... TEST RESPONSE
                ------------------------------------------
                Beat Name: {title}
                Producer Name: {producer}
                Key: {key}
                Detune: {detune}
                BPM: {bpm}
                Beat File: {file.url}
                """

        await ctx.send(msg)

    @send_beat.subcommand(sub_cmd_name='url', sub_cmd_description='Send a beat url to Apostoli')
    @title()
    @producer()
    @beat_url()
    @key()
    @detune()
    @bpm()
    async def send_beat_url(
            self,
            ctx: SlashContext,
            title: str,
            producer: str,
            url: str,
            key: str,
            detune: Optional[int] = None,
            bpm: int = None,
    ):

        notion = NotionService()
        response = await notion.create_beat_entry(title, producer, url, key, detune, bpm)

        msg = f"""\
                CURRENTLY NOT IMPLEMENTED... TEST RESPONSE
                ------------------------------------------
                Beat Name: {title}
                Producer Name: {producer}
                Key: {key}
                Detune: {detune}
                BPM: {bpm}
                Beat File: {url}
                """

        await ctx.send(msg)
