import typing
import typing_extensions

from typing import Protocol, TypeVar, Union

from subtype.utils import is_any, is_protocol, type_var_to_type


def test_is_any() -> None:
    assert is_any(typing.Any)
    assert is_any(typing_extensions.Any)

    assert not is_any(int)
    assert not is_any(str)


def test_is_protocol() -> None:
    class Foo:
        pass

    assert not is_protocol(Foo)

    class Printer(Protocol):
        def print(self) -> None:
            ...

    assert is_protocol(Printer)

    class NotPrinter(Printer):
        pass

    assert not is_protocol(NotPrinter)

    class ShinyPrinter(Printer, Protocol):
        pass

    assert is_protocol(ShinyPrinter)


def test_type_var_to_type() -> None:
    assert type_var_to_type(TypeVar("T")) is typing.Any
    assert type_var_to_type(TypeVar("T", bound=str)) is str
    assert type_var_to_type(TypeVar("T", int, str)) == Union[int, str]
