from stoli_bot.src.services.notion.crud import notion_create, notion_query_producers
from stoli_bot.src.models.producer import Producer
from stoli_bot.src.models.beat import Beat
import asyncio


async def main():
    # producer = Producer(
    #     name="jim",
    #     discord_id="jim1234",
    #     email="afake.email@example.cum",
    # )
    #
    # result = await notion_create(producer)
    # print(result)
    #
    # query = await notion_query_producers(discord_id='jim1234')
    # print(query[0])

    # beat = Beat(
    #     title='title',
    #     producer_name='producer_name',
    #     link='https://foo.bar',
    #     bpm=100
    # )

    # result = await notion_create(beat)
    # print(result)

    query = await notion_query_producers(discord_id='1apostoli')
    print(query[0])

    print(Producer.from_query(query[0])) # noqa


if __name__ == "__main__":
    asyncio.run(main())




