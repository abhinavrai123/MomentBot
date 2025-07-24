# src/main.py

from momentbot.src.data.database import init_db

def main():
    # Step 1: Initialize the database tables
    init_db()

    # Step 2: Initialize the bot, handlers, etc.
    # from telegram.ext import ApplicationBuilder, ...
    # application = ApplicationBuilder().token(...).build()
    # ...

if __name__ == "__main__":
    main()
