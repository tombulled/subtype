from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print(self) -> None:
        raise NotImplementedError


class DogPrinter:
    def print(self) -> None:
        print("Woof!")


my_printer: Printer = DogPrinter()
