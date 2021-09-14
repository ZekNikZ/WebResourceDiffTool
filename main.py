from exceptions import LoaderError, MissingSettingsError
from loaders.web import WebLoader
from loaders import CompositeLoader
from loaders.canvas import CanvasLoader
from config import config
from caches import Cache
from caches.basic import HTMLCache, TextCache
import logs
import requests

logger = logs.get('app')

def check_version():
    curr_version = None
    with open('version.txt', 'r') as file:
        curr_version = file.read()
    new_version = str(requests.get('https://zeknikz.github.io/WebResourceDiffTool/version.txt').text)
    logger.info('Checking for updates')
    if curr_version != new_version:
        logger.warning(f'This version of the diff tool ({curr_version}) does not match the latest release ({new_version}).')
    else:
        logger.info('Up to date!')

def main():
    # Setup logging
    logger.info('Initializing diff tool')

    # Check version
    check_version()

    # Load loader modules
    base_loader = CompositeLoader()
    base_loader.registerChild(CanvasLoader())
    base_loader.registerChild(WebLoader())

    # Load cache modules
    base_cache = Cache('data', config["cache_file"])
    base_cache.registerCache(HTMLCache())
    base_cache.registerCache(TextCache())

    # Load and cache watchers
    for watcher in config['watchers']:
        id = watcher['id']
        data_type = watcher['data_type']
        data = None
        try:
            data = base_loader.load(watcher)
        except LoaderError or MissingSettingsError:
            logger.error(f"Watcher '{id}' did not succeed, look above for more details")
            pass

        if data is None:
            continue

        for item in data:
            cache_key = id + (f'-{item.key}' if item.key else '')
            base_cache.update_cache(cache_key, data_type, item.data)


if __name__ == '__main__':
    main()