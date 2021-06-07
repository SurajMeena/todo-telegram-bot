import os
import logging
import firebase_admin
from firebase_admin import db
from bot.bot import bot
from dotenv import load_dotenv
from configparser import ConfigParser


# Logging at the start to catch everything

logging.basicConfig(filename="debug.log", filemode="a", format="%(created)f - %(asctime)s - %(funcName)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO)

LOGS = logging.getLogger(__name__)

name = 'todogroup_bot'

# Read from config file
config_file = f"{name}.ini"
config = ConfigParser()
config.read(config_file)

# Extra details
__version__ = '0.0.1'
__author__ = 'suraj'

# Global Variables
bot = bot(name)
load_dotenv()

databaseURL = os.getenv("databaseURL")
key_path = os.getenv("relative_key_path")

cred_obj = firebase_admin.credentials.Certificate(key_path)

default_app = firebase_admin.initialize_app(cred_obj, {
	"databaseURL":databaseURL
	})
