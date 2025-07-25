# dev/test_main.py
import logging
from telegram.ext import ApplicationBuilder, Application
from src.data.database import init_db
from src.config.logging_config import setup_logging
from dev.log_handler import *  # ✅ Your conversation handler
from src.scheduler.scheduler import prompt_scheduler

BOT_TOKEN = "7164033808:AAF2GdT69JDedcrwNC25W9qGA1wTIwRBizU"

def main():
    init_db()
    setup_logging()
    logging.getLogger(__name__).info("MomentBot starting...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    setup_handlers(app)
    prompt_scheduler(app)
    app.add_handler(log_handler)

    print("✅ MomentBot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()