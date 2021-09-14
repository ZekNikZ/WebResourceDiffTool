from typing import Any
import json

# Load settings file
settings = None
with open('settings.json', 'r', encoding='utf-8') as settings_file:
    settings = settings_file.read()

config: dict[str, Any] = json.loads(settings)
