
from typing import Optional
import os

from interactions import (
    Extension,
    SlashContext,
    SlashCommand,
    Attachment,
    Modal,
    ModalContext,
    ShortText,
)

from stoli_bot.src.services.notion.client import NotionClient
from stoli_bot.src.bot.beats.options import (
    title,
    producer,
    key,
    detune,
    bpm,
    beat_url,
    beat_file,
)

class Beats(Extension):
    """Commands used to send beats to the bot for usage by Apostoli"""

    print(f'loaded extension from beats/extension.py, TESTING_GUILD: {os.getenv('DISCORD_TESTING_GUILD')}')

    beats_base: SlashCommand = SlashCommand(
        name='beats',
        description='Send a beat to Apostoli',
        scopes=[os.getenv('DISCORD_TESTING_GUILD')]
    )

    profile_group: SlashCommand = beats_base.group(
        name='profile',
        description='Create or update your producer profile, or query someone else\'s.'
    )

    @profile_group.subcommand(sub_cmd_name='create', sub_cmd_description='Create your producer profile')
    async def create_profile(self, ctx: SlashContext):
        """Create your producer profile"""

        create_profile_modal: Modal = Modal(
            ShortText(
                label="Producer Name / Stage Name",
                custom_id="producer_name",
                required=True,
            ),
            ShortText(
                label="Email",
                custom_id="email",
                required=False,
            ),
            ShortText(
                label="Instagram",
                custom_id="instagram",
                value="",
                required=False,
            ),
            ShortText(
                label="TikTok",
                custom_id="tiktok",
                value="",
                required=False,

            ),
            ShortText(
                label="X/Twitter",
                custom_id="x",
                value="",
                required=False,
            ),
            title="Create your producer profile",
            custom_id="create_profile",
        )

        print(create_profile_modal.to_dict())

        await ctx.send_modal(create_profile_modal)

        modal_ctx: ModalContext = await ctx.bot.wait_for_modal(create_profile_modal)

        print(modal_ctx.responses)

        await modal_ctx.send(str(modal_ctx.responses))

    send_group = beats_base.group(name='send', description='Send a beat to Apostoli')

    @send_group.subcommand(sub_cmd_name='file', sub_cmd_description='Send a beat file to Apostoli')
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

        notion: NotionClient = NotionClient()
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

    @send_group.subcommand(sub_cmd_name='url', sub_cmd_description='Send a beat url to Apostoli')
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
        notion: NotionClient = NotionClient()
        response = await notion.create_beat_entry(title, producer, url, key, detune, bpm)

        print(response)

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
