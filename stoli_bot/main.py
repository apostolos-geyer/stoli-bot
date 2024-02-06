from dotenv import load_dotenv
import asyncio

load_dotenv()



def main():
    from stoli_bot.src.bot.client import bot
    bot.load_extension('stoli_bot.src.bot.beats.extension')
    bot.start()  # Start the bot


if __name__ == '__main__':
    main()
