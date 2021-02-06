from abc import ABCMeta, abstractmethod


class IScraper(metaclass=ABCMeta):
    @abstractmethod
    def teams_chals(self):
        pass

