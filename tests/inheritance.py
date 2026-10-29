from abc import ABCMeta, abstractmethod
from collections import OrderedDict


class Registry(OrderedDict):
    def first(self):
        return next(iter(self))


class CustomError(Exception):
    pass


class Base:
    pass


class Child(Base):
    pass


class Shape(metaclass=ABCMeta):
    @abstractmethod
    def area(self):
        pass
