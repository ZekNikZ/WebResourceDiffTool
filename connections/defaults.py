import sys
from logging import Handler, StreamHandler
from connections.base import Connection, LogHandlerMixin

class ConsoleLogHandler(LogHandlerMixin, Connection):
    def __init__(self):
        settings = {
            'id': 'builtin/console',
            'type': 'builtin',
            'log_level': 'DEBUG'
        }
        super().__init__(settings, 'builtin/console')

    def createHandler(self) -> Handler:
        return StreamHandler()