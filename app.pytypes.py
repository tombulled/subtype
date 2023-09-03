from dataclasses import dataclass
from typing import List

from pytypes import is_subtype


@dataclass
class Animal:
    name: str


class Dog(Animal):
    pass


class Cat(Animal):
    pass


d = is_subtype(List[Dog], List[Animal])
