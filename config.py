# .env preloader
from dotenv import load_dotenv
load_dotenv()

from typing import Any
import os
import json

API_URL = os.getenv('CANVAS_API_URL')
API_TOKEN = os.getenv('CANVAS_API_TOKEN')

# Load settings file
settings = None
with open('settings.json', 'r', encoding='utf-8') as settings_file:
    settings = settings_file.read()

config: dict[str, Any] = json.loads(settings)
