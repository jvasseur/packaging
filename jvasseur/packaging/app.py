import abc

class App(abc.ABC):
    @abc.abstractmethod
    def versions(self):
        pass