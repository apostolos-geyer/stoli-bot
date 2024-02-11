from typing import Optional
import os

from interactions import (
    Extension,
    SlashContext,
    SlashCommand,
    Attachment,
    Modal,
    ShortText,
)

from src.models.beat import Beat
from src.models.producer import Producer
from src.services.notion import crud as notion_crud

from src.bot.beats.options import (
    title,
    key,
    detune,
    bpm,
    beat_url,
    beat_file,
)


def CREATE_PROFILE_MODAL() -> Modal:
    return Modal(
        ShortText(label="Producer Name / Stage Name", custom_id="name", required=True),
        ShortText(label="Email", custom_id="email", required=False),
        ShortText(label="Instagram", custom_id="instagram", value="", required=False),
        ShortText(label="TikTok", custom_id="tiktok", value="", required=False),
        ShortText(label="YouTube", custom_id="youtube", value="", required=False),
        title="Create your producer profile",
        custom_id="create_profile",
    )


async def get_producer_from_discord_id(discord_id: str) -> Optional[Producer]:
    query_response = await notion_crud.notion_query_producers(discord_id=discord_id)
    if query_response:
        producer: Producer = Producer.from_query(query_response[0])  # noqa
        return producer
    return None


class Beats(Extension):
    """Commands used to send beats to the bot for usage by Apostoli"""

    print(
        f'loaded extension from beats/extension.py, TESTING_GUILD: {os.getenv('DISCORD_TESTING_GUILD')}'
    )

    def __init__(self, *args):
        self.users_registered = dict()

    beats_base: SlashCommand = SlashCommand(
        name="beats",
        description="Send a beat to Apostoli",
        scopes=[os.getenv("DISCORD_TESTING_GUILD")],
    )

    profile_group: SlashCommand = beats_base.group(
        name="profile",
        description="Create or update your producer profile, or query someone else's.",
    )

    @profile_group.subcommand(
        sub_cmd_name="create", sub_cmd_description="Create your producer profile"
    )
    async def create_profile(self, ctx: SlashContext):
        """Create your producer profile"""

        discord_id: str = ctx.user.username

        if producer_profile := await get_producer_from_discord_id(
            discord_id=discord_id
        ):
            await ctx.send(
                f"User {ctx.user.mention} cannot register as they already have: {producer_profile}",
                ephemeral=True,
            )
            return

        mod = CREATE_PROFILE_MODAL()
        await ctx.send_modal(mod)

        modal_ctx = await ctx.bot.wait_for_modal(mod)
        user_detail: dict = modal_ctx.responses | {"discord_id": discord_id}
        producer_entry: Producer = Producer(**user_detail)

        await notion_crud.notion_create(producer_entry)

        if await get_producer_from_discord_id(discord_id=discord_id):
            return await modal_ctx.send(
                f"User {ctx.user.mention} registered: {producer_entry}"
            )

        raise Exception("An error occurred or something lol not my problem tbh")

    @profile_group.subcommand(
        sub_cmd_name="check", sub_cmd_description="Check your producer profile"
    )
    async def check_profile(self, ctx: SlashContext):
        """Check your producer profile"""

        discord_id: str = ctx.user.username

        if producer_profile := await get_producer_from_discord_id(
            discord_id=discord_id
        ):
            return await ctx.send(f"{producer_profile}")
        else:
            return await ctx.send(
                f"-_- u need to register first {ctx.user.mention}.. \n use /beats profile register :333 then i can have ur INFORMATION "
            )

    send_group = beats_base.group(name="send", description="Send a beat to Apostoli")

    async def send_beat(
        self,
        ctx: SlashContext,
        title: str,
        url: str,
        bpm: Optional[int] = None,
        key: Optional[str] = None,
        detune: Optional[int] = None,
    ):
        discord_id = ctx.user.username

        producer_profile: Producer
        if (
            producer_profile := await get_producer_from_discord_id(
                discord_id=discord_id
            )
        ) is None:
            await ctx.send(
                f"{ctx.user.mention} you must register your producer profile first. Use /profile check"
            )
            return

        producer_name: str = producer_profile.name

        try:
            beat_entry = Beat(
                title=title,
                producer_name=producer_name,
                bpm=bpm,
                key=key,
                detune=detune,
                link=url,
            )
            await notion_crud.notion_create(beat_entry)

            msg = f"""\
            {ctx.user.mention}
            thanks for the beat {producer_name}. 

            your submission:
            title: {title}
            bpm: {bpm if bpm is not None else "...no bpm attached... do you not know or are you just fucking lazy bitch xD"}
            key: {key if key is not None else "—_— oh great... you didnt specify the KEY... do you know how inaccurate key detectors are??? F.U"}
            detune: {detune if detune is not None else "no detune? if ts off by .1 Hz from A=440 i will fucking find you gang."}
            file: {url}
            """

            return await ctx.send(msg)
        except Exception as e:
            return await ctx.send(
                f"somefing went wrong daddy im sowwy o.o.. pwease dont punish me\n {e}"
            )

    @send_group.subcommand(
        sub_cmd_name="file", sub_cmd_description="Send a beat file to Apostoli"
    )
    @title()
    @beat_file()
    @bpm()
    @key()
    @detune()
    async def send_beat_file(
        self,
        ctx: SlashContext,
        title: str,
        file: Attachment,
        bpm: Optional[int] = None,
        key: Optional[str] = None,
        detune: Optional[int] = None,
    ):
        """Send a beat file to Apostoli"""

        return await self.send_beat(ctx, title, file.url, bpm, key, detune)

    @send_group.subcommand(
        sub_cmd_name="url", sub_cmd_description="Send a beat url to Apostoli"
    )
    @title()
    @beat_url()
    @bpm()
    @key()
    @detune()
    async def send_beat_url(
        self,
        ctx: SlashContext,
        title: str,
        url: str,
        bpm: Optional[int] = None,
        key: Optional[str] = None,
        detune: Optional[int] = None,
    ):
        return await self.send_beat(ctx, title, url, bpm, key, detune)
