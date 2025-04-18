import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMINS = [int(i)  for i in os.getenv('ADMINS').split(',')]
BOT_NAME = os.getenv("BOT_NAME")