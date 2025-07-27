import this# Entry point for the bot
import os
from dotenv import load_dotenv

load_dotenv()

print("DATABASE_URL →", os.getenv("DATABASE_URL"))