from logging import Formatter, Handler, Logger
from typing import Any, Callable
from config import config
import logging

class Connection:
    def __init__(self, conn_type: str, settings: dict[str, Any]):
        self.conn_type = conn_type
        self.id = settings.get('id')
        if self.id is None:
            raise ValueError('Connection is missing ID')

    def type(self) -> str:
        return self.conn_type

class LogHandlerMixin:
    DEFAULT_FORMAT = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    def __init__(self, settings: dict[str, Any]):
        super().__init__(settings)
        level: int = self.LEVELS.get(settings.get('log_level'))
        format: str = settings.get('format')
        self.handler = self.initHandler(format or self.DEFAULT_FORMAT, level)

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

from connections.defaults import ConsoleLogHandler
from connections.canvas import CanvasConnection

class ConnMang:
    connections: list[Connection]
    connection_types: dict[str, Callable[[dict[str, Any]], Connection]]

    def __init__(self):
        self.connections = []
        self.connection_types = []

        # Built-ins
        self.connections.append(ConsoleLogHandler())

    def loadConnections(self, connections: list[dict[str, Any]]) -> None:
        # Load connections
        i = 0
        for conn in connections:
            conn_type = conn.get('type')
            if conn_type is None:
                # logger.error(f"Connection {i} is missing a connection type")
                continue
            creator = self.connection_types.get(conn_type)
            if conn_type is None:
                # logger.error(f"Connection {i} is using invalid connection type '{conn_type}'")
                continue
            self.connections.append(creator(conn))
            i += 1

    def getLogHandlers(self) -> list[LogHandlerMixin]:
        return list(filter(lambda conn: isinstance(conn, LogHandlerMixin), self.connections))

    def registerConnectionType(self, key: str, builder: Callable[[dict[str, Any]], Connection]) -> None:
        self.connection_types[key] = builder

    def getConnection(self, id: str, conn_type: str):
        for c in self.connections:
            if c.id == id and c.type() == conn_type:
                return c
        return None

connection_manager = ConnMang()
connection_manager.registerConnectionType(CanvasConnection.conn_type, CanvasConnection)
connection_manager.loadConnections(config['connections'])