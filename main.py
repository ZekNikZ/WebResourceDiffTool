from loaders import CompositeLoader
from loaders.canvas import CanvasLoader
from config import config
from caches import Cache
from caches.basic import HTMLCache, TextCache

def main():
    # Load loader modules
    base_loader = CompositeLoader()
    base_loader.registerChild(CanvasLoader())

    # Load cache modules
    base_cache = Cache('data', config["cache_file"])
    base_cache.registerCache(HTMLCache())
    base_cache.registerCache(TextCache())

    # Load and cache watchers
    for watcher in config['watchers']:
        id = watcher['id']
        data_type = watcher['data_type']
        data = base_loader.load(watcher)

        for item in data:
            cache_key = id + (f'-{item.key}' if item.key else '')
            base_cache.update_cache(cache_key, data_type, item.data)



if __name__ == '__main__':
    main()