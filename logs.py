import logging
from connections import connection_manager

handlers = connection_manager.getLogHandlers()

LOGS = {}

def add(name: str) -> logging.Logger:
    name = name.upper()
    LOGS[name] = logging.getLogger(name)
    for h in handlers:
        h.attach(LOGS[name])
    return LOGS[name]

def get(name: str) -> logging.Logger:
    name = name.upper()
    if name in LOGS:
        return LOGS[name]
    return add(name)