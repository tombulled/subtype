from pytest import fixture


class Cls:
    pass


class Parent:
    pass


class Child(Parent):
    pass


@fixture
def cls() -> type:
    return Cls


@fixture
def parent() -> type:
    return Parent


@fixture
def child() -> type:
    return Child
