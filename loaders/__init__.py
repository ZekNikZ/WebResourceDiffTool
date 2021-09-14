from typing import Any, Union, Optional
class DataEntry:
    def __init__(self, data: str, key: Optional[str] = None):
        self.data = data
        self.key = key

class Loader:
    def __init__(self, name: str):
        self.name = name

    def load(self, settings: dict[str, Any]) -> DataEntry:
        raise NotImplementedError()

class CompositeLoader(Loader):
    children: list[Loader]

    def __init__(self, name: str = None):
        super().__init__(name)
        self.children = []

    def load(self, settings: dict[str, Any]) -> Union[DataEntry, list[DataEntry]]:
        base, submodule, *rest = settings["loader"].split('/')
        if self.name is not None:
            settings["loader"] = f'{submodule}/{"/".join(rest)}'
            return self.loadSubmodule(submodule, settings)
        else:
            return self.loadSubmodule(base, settings)

    def loadSubmodule(self, submodule: str, settings: dict[str, Any]) -> Union[DataEntry, list[DataEntry]]:
        for child in self.children:
            if child.name == submodule:
                return child.load(settings)
        raise ValueError(f"subloader '{submodule}' in loader '{self.name or 'base'}' was requested but was not found")

    def registerChild(self, loader: Loader):
        self.children.append(loader)