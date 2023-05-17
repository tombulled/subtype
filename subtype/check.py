import typing
from typing import Any, Protocol


def _is_protocol(type_: type, /) -> bool:
    return isinstance(type_, type) and issubclass(type_, type(Protocol))


def _is_runtime_protocol(type_: type, /) -> bool:
    return _is_protocol(type_) and getattr(type_, "_is_runtime_protocol", False) is True


def _is_generic_alias(obj: Any, /) -> bool:
    return isinstance(obj, typing._GenericAlias)  # type: ignore


def is_subtype(lhs: Any, rhs: Any, /) -> bool:
    """
    Check whether `lhs` is a subtype of `rhs`

    For example, `int` is a valid subtype of `Any`
    """

    #
    # Identity check - is `lhs` the same as `rhs`?
    #
    if lhs is rhs:
        return True

    #
    # Subclass check - is `lhs` a subclass of `rhs`?
    #
    if issubclass(lhs, rhs):
        return True

    #
    # Interface check - does `lhs` implement `rhs`?
    #
    if (
        isinstance(lhs, type)
        and isinstance(rhs, type)
        and _is_protocol(rhs)
        and _is_runtime_protocol(rhs)
        and isinstance(lhs, rhs)
    ):
        return True

    #
    # Generic alias check
    #
    # TODO

    return False
