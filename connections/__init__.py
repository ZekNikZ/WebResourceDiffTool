from typing import Any, Callable
from config import config
import logs

from connections.base import Connection
from connections.defaults import ConsoleLogHandler
from connections.canvas import CanvasConnection

logger = logs.get('CONNECTION')

class ConnMang:
    connections: list[Connection]
    connection_types: dict[str, Callable[[dict[str, Any]], Connection]]

    def __init__(self):
        self.connections = []
        self.connection_types = {}
        self.conn_num = 0

    def loadConnections(self, connections: list[dict[str, Any]]) -> None:
        # Load connections
        for conn in connections:
            conn_type = conn.get('type')
            if conn_type is None:
                logger.error(f"Connection {self.conn_num} is missing a connection type")
                continue
            creator = self.connection_types.get(conn_type)
            if conn_type is None:
                logger.error(f"Connection {self.conn_num} is using invalid connection type '{conn_type}'")
                continue
            self.connections.append(creator(conn))
            self.conn_num += 1

    def loadConnection(self, connection: Connection) -> None:
        self.connections.append(connection)
        self.conn_num += 1

    def registerConnectionType(self, key: str, builder: Callable[[dict[str, Any]], Connection]) -> None:
        self.connection_types[key] = builder

    def getConnection(self, id: str, conn_type: str):
        for c in self.connections:
            if c.id == id and c.type() == conn_type:
                return c
        return None

# Create the connection manager
connection_manager = ConnMang()

# Register connection types
connection_manager.registerConnectionType(CanvasConnection.conn_type, CanvasConnection)

# Built-ins
connection_manager.loadConnection(ConsoleLogHandler())

# Connections
connection_manager.loadConnections(config['connections'])