from typing import Any
from logging import Formatter, Handler, Logger
import logging
import logs

logger = logs.get('connection')

class Connection:
    def __init__(self, settings: dict[str, Any], conn_type: str):
        self.conn_type = conn_type
        self.id = settings.get('id')
        if self.id is None:
            raise ValueError('Connection is missing ID')

    def type(self) -> str:
        return self.conn_type

class LogHandlerMixin:
    DEFAULT_FORMAT = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, settings: dict[str, Any], *args):
        super().__init__(settings, *args)
        format: str = settings.get('format')
        self.handler = self.initHandler(format or self.DEFAULT_FORMAT, settings.get('log_level'))

        # Register handler
        logs.addHandler(self)
        logger.info(f"Registered connection '{self.id}' as a log handler")

    def initHandler(self, format: str, level: int) -> Handler:
        handler = self.createHandler()
        handler.setFormatter(self.createFormatter(format))
        handler.setLevel(level)
        return handler

    def createFormatter(self, format: str) -> Formatter:
        return Formatter(format, datefmt=self.DATE_FORMAT)

    def createHandler(self) -> Handler:
        raise NotImplementedError('Subclass needs to define createHandler()')

    def attach(self, logger: Logger):
        logger.addHandler(self.handler)
