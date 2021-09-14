from connections import Connection
from typing import Any
from canvasapi import Canvas
from exceptions import *
import logs

# logger = logs.get('CONNECTION')

class CanvasConnection(Connection):
    conn_type = 'canvas'

    def __init__(self, settings: dict[str, Any]):
        super().__init__(CanvasConnection.conn_type, settings)

        api_url = settings.get('api_url')
        if api_url is None:
            # logger.error(f"Could not load Canvas connection '{self.id}': missing api_url")
            raise MissingSettingsError(f"Could not load Canvas connection '{self.id}': missing api_url")
        api_token = settings.get('api_token')
        if api_token is None:
            # logger.error(f"Could not load Canvas connection '{self.id}': missing api_token")
            raise MissingSettingsError(f"Could not load Canvas connection '{self.id}': missing api_url")

        try:
            self.canvas = Canvas(api_url, api_token)
        except Exception as e:
            # logger.error(f"Could not load Canvas connection '{self.id}': unexpected error")
            # logger.exception(e)
            raise CustomConnectionError(e.message)

    def canvas(self) -> Canvas:
        return self.canvas