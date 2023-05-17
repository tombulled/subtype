from typing import Any, List, Mapping, Protocol, runtime_checkable

import pytest

from subtype import is_subtype


class Cls:
    pass


class Parent:
    pass


class Child(Parent):
    pass


@runtime_checkable
class Processor(Protocol):
    def process(self, data: str, /) -> str:
        ...


class UpperProcessor:
    def process(self, data: str, /) -> str:
        return data.upper()


@pytest.mark.parametrize(
    "typ",
    (
        None,
        int,
        str,
        list,
        tuple,
        Any,
        List[int],
        Mapping[str, str],
        Cls,
    ),
)
def test_self(typ: Any) -> None:
    """
    Every type should be a valid subtype of itself
    """
    assert is_subtype(typ, typ)


@pytest.mark.parametrize(
    "lhs,rhs",
    ((Child, Parent),),
)
def test_subclass(lhs: Any, rhs: Any) -> None:
    """
    Every subclass should be a valid subtype
    """

    assert is_subtype(lhs, rhs)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    ((UpperProcessor, Processor, True),),
)
def test_implementation(lhs: Any, rhs: Any, expected: bool) -> None:
    """
    Every subclass should be a valid subtype
    """

    assert is_subtype(lhs, rhs) is expected


@pytest.mark.skip(reason="Functionality not yet implemented")
@pytest.mark.parametrize(
    "typ",
    (
        None,
        int,
        str,
        list,
        tuple,
        Any,
        List[int],
        Mapping[str, str],
    ),
)
def test_any(typ: Any) -> None:
    """
    Every type should be a valid subtype of `Any`
    """

    assert is_subtype(typ, Any)
