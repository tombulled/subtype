import collections.abc
import typing
from typing import (
    Any,
    ClassVar,
    Final,
    Literal,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from .models import NormalisedType
from .types import GenericAlias

GENERIC_ALIAS_MAP: Final[Mapping[type, typing._GenericAlias]] = {
    value.__origin__: value
    for key, value in typing.__dict__.items()
    if key in typing.__all__ and isinstance(value, typing._GenericAlias)
}


def _type_var_to_type(tv: TypeVar, /) -> Any:
    bound: Optional[Any] = tv.__bound__
    constraints: Tuple[Any, ...] = tv.__constraints__

    if bound is not None:
        return bound

    if constraints:
        return Union.__getitem__(constraints)  # type: ignore

    return Any


def normalise(type_: Any, /) -> NormalisedType:
    if type_ in GENERIC_ALIAS_MAP:
        type_ = GENERIC_ALIAS_MAP[type_]

    if isinstance(type_, TypeVar):
        type_ = _type_var_to_type(type_)

    origin: Optional[Any] = typing.get_origin(type_)
    args: Tuple[Any, ...] = typing.get_args(type_)

    if type_ in (None, Ellipsis) or isinstance(type_, type):
        return NormalisedType(type_)

    # Temporarily assume that if it's a primitive, then in it's an arg of Literal[...]
    if isinstance(type_, (str, int)):
        return NormalisedType(type_)

    if isinstance(type_, typing._SpecialForm):
        if type_ in (Any,):
            return NormalisedType(type_)
        elif type_._name in (ClassVar._name, Final._name):  # type: ignore
            return normalise(type_[Any])
        elif type_ is Union:
            raise ValueError("Union requires two or more type arguments")
        elif type_ is Optional:
            raise ValueError("Optional[...] must have exactly one type argument")
        elif type_ is Literal:
            raise ValueError("Literal[...] must have at least one parameter")

        raise NotImplementedError

    if isinstance(type_, GenericAlias) and origin is not None:
        if not args:
            if origin is tuple:
                args = (Any, ...)
            elif origin is collections.abc.Callable:
                args = (..., Any)
            else:
                args = tuple(Any for _ in type_.__parameters__)
        elif origin is collections.abc.Callable:
            a, r = args

            args = tuple(arg for arg in a) + (r,)

        return NormalisedType(origin, tuple(normalise(arg) for arg in args))

    raise TypeError(f"Expected type or generic alias, got {type(type_)}")
