import collections.abc
import typing
from typing import Any, Optional, Tuple

from .models import NormalisedType
from .types import GenericAlias


def normalise(type_: Any, /) -> NormalisedType:
    origin: Optional[Any] = typing.get_origin(type_)
    args: Tuple[Any, ...] = typing.get_args(type_)

    if type_ is None:
        type_ = type(None)

    if type_ in (type(None), Any, Ellipsis):
        return NormalisedType(type_)
    elif isinstance(type_, type):
        return NormalisedType(type_)
    elif isinstance(type_, GenericAlias) and origin is not None:
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
    else:
        raise TypeError(f"Expected type or generic alias, got {type(type_)}")
