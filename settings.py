import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))

BASE_DIR = pathlib.Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
IMAGES_TMP_DIR = IMAGES_DIR / "tmp"
IMAGES_AVATAR_TMP_DIR = IMAGES_DIR / "avatars"