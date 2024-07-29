from dotenv import load_dotenv
import os
import bot

load_dotenv()

def main() -> None:
    load_dotenv()
    bot.start(os.getenv("TELEGRAM_BOT_TOKEN"))

if __name__ == "__main__":
    main()