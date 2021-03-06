from __future__ import annotations
import datetime
from os import path
import hashlib
import json
from pathlib import Path
from typing import Any

class BaseCache:
    def __init__(self, key: str, ext: str = None):
        self.key = key
        self.ext = ext or key

    def cache_item(self, cache: Cache, id: str, data: str, metadata: dict[str, Any]):
        cache.record_entry(id, metadata)
        cache.store_data(metadata['filename'], data)

    def get_metadata(self, id: str, data: str) -> dict[str, Any]:
        timestamp = int(datetime.datetime.now().timestamp())
        metadata = {
            'timestamp': timestamp,
            'hash': self.hash(data),
            'filename': f'{id}-{timestamp}.{self.ext}'
        }
        return metadata

    def hash(self, data: str) -> str:
        return hashlib.md5(data.encode()).hexdigest()

    def is_same(self, meta1: dict[str, Any], meta2: dict[str, Any]) -> bool:
        return meta1 is not None and meta2 is not None and meta1['hash'] == meta2['hash']

class Cache:
    caches: dict[str, BaseCache]
    config: dict[str, Any]
    folder: str
    config_file: str

    def __init__(self, cache_folder: str, cache_file: str):
        self.caches = {}
        self.folder = cache_folder
        self.config_file = cache_file
        self.load_config()
        Path(self.folder).mkdir(parents=True, exist_ok=True)

    def load_config(self):
        if not path.isfile(self.config_file):
            self.config = {}
            self.save_config()
        with open(self.config_file, 'r', encoding='utf-8') as file:
            self.config = json.loads(file.read())

    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.config))

    def registerCache(self, cache):
        self.caches[cache.key] = cache

    def update_cache(self, id: str, data_type: str, data: str, only_if_differs=True):
        old_meta = self.get_latest_entry(id)
        new_meta = self.caches[data_type].get_metadata(id, data)
        if only_if_differs and self.caches[data_type].is_same(old_meta, new_meta):
            return
        self.caches[data_type].cache_item(self, id, data, new_meta)

    def record_entry(self, id: str, metadata: dict):
        if id not in self.config:
            self.config[id] = []
        self.config[id].append(metadata)
        self.save_config()

    def get_latest_entry(self, id: str) -> dict:
        latest: dict[str, Any] = None
        latest_val: int = 0
        if id not in self.config:
            self.config[id] = []
        for meta in self.config[id]:
            if meta['timestamp'] > latest_val:
                latest = meta
                latest_val = meta['timestamp']
        return latest

    def store_data(self, filename: str, data: str):
        with open(path.join(self.folder, filename), 'w', encoding='utf-8') as file:
            file.write(data)

    def read_data(self, filename: str) -> str:
        with open(path.join(self.folder, filename), 'r', encoding='utf-8') as file:
            return file.read()

