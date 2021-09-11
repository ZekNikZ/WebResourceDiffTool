import requests
import logging

from loaders import CompositeLoader
from loaders.canvas import CanvasLoader
from config import config
from caches import Cache
from caches.basic import HTMLCache, TextCache

def check_version():
    curr_version = None
    with open('version.txt', 'r') as file:
        curr_version = file.read()
    new_version = str(requests.get('https://zeknikz.github.io/WebResourceDiffTool/version.txt').text)
    logging.info('Checking for updates')
    if curr_version != new_version:
        logging.warning(f'This version of the diff tool ({curr_version}) does not match the latest release ({new_version}).')
    else:
        logging.info('Up to date!')

def main():
    # Setup logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info('Initializing diff tool')

    # Check version
    check_version()

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