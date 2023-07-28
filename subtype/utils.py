import typing
import typing_extensions

from typing import Any, Optional, Protocol, Set, Tuple, TypeVar, Union

TYPES_ANY: Set[Any] = {typing.Any, typing_extensions.Any}


def is_any(t: Any, /) -> bool:
    return t in (typing.Any, typing_extensions.Any)


def is_final(t: Any, /) -> bool:
    return typing.get_origin(t) in (typing.Literal, typing_extensions.Literal)


def is_literal(t: Any, /) -> bool:
    return typing.get_origin(t) in (typing.Literal, typing_extensions.Literal)


def is_protocol(t: Any, /) -> bool:
    if not isinstance(t, type):
        return False

    if not issubclass(t, (typing.Protocol, typing_extensions.Protocol)):  # type: ignore
        return False

    return t._is_protocol is True  # type: ignore


def is_runtime_protocol(t: Any, /) -> bool:
    return is_protocol(t) and t._is_runtime_protocol is True


# def is_generic_alias(obj: Any, /) -> bool:
#     return isinstance(obj, typing._GenericAlias)  # type: ignore


def is_type_var(t: Any, /) -> bool:
    return isinstance(t, typing.TypeVar)


def type_var_to_type(type_var: TypeVar, /) -> Any:
    bound: Optional[Any] = type_var.__bound__
    constraints: Tuple[Any, ...] = type_var.__constraints__

    if bound is not None:
        return bound

    if constraints:
        return Union.__getitem__(constraints)  # type: ignore

    return Any


def is_subclass(lhs: Any, rhs: Any) -> bool:
    return isinstance(lhs, type) and isinstance(rhs, type) and issubclass(lhs, rhs)
