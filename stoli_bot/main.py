from dotenv import load_dotenv
import os 
import sys

load_dotenv()


def main():
    # check if we're in a docker container or not
    if os.getenv('DOCKER_FLAG', False):
        print("Running in a docker container")
        sys.path.append('/app')
    

    from src.bot.client import bot

    bot.load_extension("src.bot.beats.extension")
    bot.start()  # Start the bot

if __name__ == "__main__":
    main()
