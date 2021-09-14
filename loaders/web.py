from exceptions import *
from typing import Any
import requests
from loaders import DataEntry, Loader, CompositeLoader
import logs

log = logs.get('LOADER')

class SinglePageLoader(Loader):
    def __init__(self):
        super().__init__('single')

    def load(self, settings: dict[str, Any]) -> list[DataEntry]:
        # Get URL
        url = settings.get('url')
        if url is None:
            log.error(f"Parameter 'url' is not provided in settings for watcher '{settings['id']}'")
            raise MissingSettingsError(f"Parameter 'url' is not provided in settings for watcher '{settings['id']}'")

        # Check if we need to bypass ssl
        bypass_ssl_certs = settings.get('bypass_ssl_certs') or False

        # Attempt download
        try:
            data = str(requests.get(url, verify=not bypass_ssl_certs).text)
        except Exception as e:
            log.error(f"Could not load web resource '{url}' in watcher '{settings['id']}'")
            log.exception(e.message)
            raise LoaderError(f"Could not load web resource '{url}' in watcher '{settings['id']}'")

        return [DataEntry(data)]

class WebLoader(CompositeLoader):
    def __init__(self) -> None:
        super().__init__('web')

        self.registerChild(SinglePageLoader())