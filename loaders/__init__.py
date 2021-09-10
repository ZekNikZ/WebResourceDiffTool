class DataEntry:
    def __init__(self, data: str, key: str=None):
        self.data = data
        self.key = key

class Loader:
    def __init__(self, name: str):
        self.name = name

    def load(self, settings: dict):
        raise NotImplementedError()

class CompositeLoader(Loader):
    def __init__(self, name:str=None):
        super().__init__(name)
        self.children = []

    def load(self, settings: dict):
        base, submodule, *rest = settings["loader"].split('/')
        if self.name is not None:
            settings["loader"] = f'{submodule}/{"/".join(rest)}'
            return self.loadSubmodule(submodule, settings)
        else:
            return self.loadSubmodule(base, settings)

    def loadSubmodule(self, submodule: str, settings: dict):
        for child in self.children:
            if child.name == submodule:
                return child.load(settings)
        raise ValueError()

    def registerChild(self, loader: Loader):
        self.children.append(loader)