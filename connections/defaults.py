from logging import Handler, StreamHandler
import logging
from connections import Connection, LogHandlerMixin

class ConsoleLogHandler(LogHandlerMixin, Connection):
    def __init__(self):
        settings = {
            'id': 'console',
            'type': 'builtin',
            'log_level': 'DEBUG'
        }
        super().__init__('builtin/console', settings)

    def createHandler(self) -> Handler:
        return StreamHandler()