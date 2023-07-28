import collections.abc
import typing
from typing import (
    Any,
    ClassVar,
    Final,
    ForwardRef,
    Generic,
    Literal,
    NoReturn,
    Optional,
    Protocol,
    Tuple,
    Union,
)
import typing_extensions

from .utils import (
    is_any,
    is_final,
    is_literal,
    is_protocol,
    is_runtime_protocol,
    is_subclass,
    is_type_var,
    type_var_to_type,
)


def is_subtype(lhs: Any, rhs: Any, /) -> bool:
    """Check whether `lhs` is a subtype of `rhs`"""

    lhs_origin: Optional[Any] = typing.get_origin(lhs)
    lhs_args: Tuple[Any, ...] = typing.get_args(lhs)
    rhs_origin: Optional[Any] = typing.get_origin(rhs)
    rhs_args: Tuple[Any, ...] = typing.get_args(rhs)

    #
    # [Any check] Everything is a subtype of `Any`
    #
    if is_any(rhs):
        return True

    # [Sentinel check] Only the sentinel is a valid subtype of itself
    if rhs in (None, Ellipsis) and lhs is not rhs:
        return False

    #
    # [Identity check] Everything is a subtype of itself
    #
    if lhs is rhs:
        return True

    if isinstance(rhs, type):
        #
        # [Subclass check] A subclass is a subtype of its superclass
        #
        if is_subclass(lhs, rhs):
            return True

        #
        # [Protocol check] A protocol implementation is a subtype of the protocol
        #
        if is_protocol(rhs) and is_runtime_protocol(rhs) and isinstance(lhs, rhs):
            return True

        return False

    # [ForwardRef check]
    if isinstance(rhs, ForwardRef):
        raise NotImplementedError

    # [Final check]
    if is_final(rhs):
        return is_subtype(lhs, rhs_args[0])

    # [Literal check]
    if is_literal(rhs):
        raise NotImplementedError

    # [SpecialForm check]
    if isinstance(rhs, typing._SpecialForm):
        # Any: Covered by "any check"
        # NoReturn: Same in t and te
        # ClassVar: Same in t and te
        # Final: Different in te
        # Union: Exclusive to t
        # Optional: Exclusive to t
        # Literal: Different in te

        if rhs is NoReturn:
            raise ValueError("Invalid type")

        if rhs_origin is ClassVar:
            return is_subtype(lhs, rhs_args[0])

        if rhs_origin is Union:
            return any(is_subtype(lhs, arg) for arg in rhs_args)

        if rhs_origin is Optional:
            # Optional[T] should only ever be represented as Union[T, None]
            raise ValueError("Invalid type")

        raise NotImplementedError

    # [GenericAlias check]
    if isinstance(rhs, typing._GenericAlias) and rhs_origin is not None:
        if rhs_origin is typing_extensions.Final:
            return is_subtype(lhs, rhs_args[0])

        raise NotImplementedError

    #
    # [Case 5: LHS Union check]
    #
    # TODO
    # 1. is_union(lhs) and all(is_subtype(arg) for arg in get_args(lhs))
    #       E.g. is_subtype(Union[int, float], Number)
    # 2. ...

    #
    # [Case 6: RHS TypeVar check]
    # if is_type_var(rhs):
    #     return is_subtype(lhs, type_var_to_type(rhs))

    # check if it's an invalid type
    # if rhs in (Generic, Protocol):
    #     raise ValueError(f"{rhs!r} is not valid as a type")

    raise NotImplementedError
