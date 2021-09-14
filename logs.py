import logging

handlers = []

LOGS = {}

def add(name: str) -> logging.Logger:
    name = name.upper()
    LOGS[name] = logging.getLogger(name)
    for h in handlers:
        h.attach(LOGS[name])
    LOGS[name].setLevel(logging.DEBUG)
    return LOGS[name]

def get(name: str) -> logging.Logger:
    name = name.upper()
    if name in LOGS:
        return LOGS[name]
    return add(name)

def addHandler(handler) -> None:
    handlers.append(handler)
    for log in LOGS.values():
        handler.attach(log)
