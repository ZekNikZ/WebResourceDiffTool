from exceptions import LoaderError, MissingSettingsError
from loaders.web import WebLoader
from loaders import CompositeLoader
from loaders.canvas import CanvasLoader
from config import config
from caches import Cache
from caches.basic import HTMLCache, TextCache
import logs
import requests

# Initialize the connection manager
import connections

logger = logs.get('app')

def check_version():
    curr_version = None
    with open('version.txt', 'r') as file:
        curr_version = file.read()
    new_version = str(requests.get('https://zeknikz.github.io/WebResourceDiffTool/version.txt').text)
    if curr_version != new_version:
        curr_parts = list(map(int, curr_version.split('.')))
        new_parts = list(map(int, new_version.split('.')))
        for i in range(min(len(curr_parts), len(new_parts))):
            if curr_parts[i] > new_parts[i]:
                logger.info(f'This version of the diff tool ({curr_version}) is newer than the current release ({new_version})')
                return
            elif curr_parts[i] < new_parts[i]:
                logger.warning(f'This version of the diff tool ({curr_version}) is older than the current release ({new_version})')
                return
        if len(curr_parts) > len(new_parts):
            logger.info(f'This version of the diff tool ({curr_version}) is newer than the current release ({new_version})')
            return
        elif len(curr_parts) < len(new_parts):
            logger.warning(f'This version of the diff tool ({curr_version}) is older than the current release ({new_version})')
            return
    else:
        logger.info('Up to date!')

def main():
    # Setup logging
    logger.info('Initializing diff tool...')

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

    # Done init
    logger.info('Done initializing')

    # Load and cache watchers
    for watcher in config['watchers']:
        id = watcher['id']
        data_type = watcher['data_type']
        data = None
        try:
            data = base_loader.load(watcher)
        except Exception as e:
            logger.exception(e)
            logger.error(f"Watcher '{id}' did not succeed, look above for more details")
            pass

        if data is None:
            continue

        for item in data:
            cache_key = id + (f'-{item.key}' if item.key else '')
            base_cache.update_cache(cache_key, data_type, item.data)


if __name__ == '__main__':
    main()