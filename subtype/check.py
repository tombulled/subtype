from typing import Any

from .utils import (
    is_any,
    is_protocol,
    is_runtime_protocol,
    is_type_var,
    type_var_to_type,
)


def is_subtype(lhs: Any, rhs: Any, /) -> bool:
    """Check whether `lhs` is a subtype of `rhs`"""

    #
    # [Case 1: Any check] Everything is a subtype of `Any`
    #
    if is_any(rhs):
        return True

    #
    # [Case 2: Identity check] Everything is a subtype of itself
    #
    if lhs is rhs:
        return True

    #
    # [Case 3: Subclass check] A subclass is a subtype of its superclass
    #
    if issubclass(lhs, rhs):
        return True

    #
    # [Case 4: Protocol check] A protocol implementation is a subtype of the protocol
    #
    if is_protocol(rhs) and is_runtime_protocol(rhs) and isinstance(lhs, rhs):
        return True

    #
    # [Case 5: LHS Union check]
    #
    # TODO
    # 1. is_union(lhs) and all(is_subtype(arg) for arg in get_args(lhs))
    #       E.g. is_subtype(Union[int, float], Number)
    # 2. ...

    #
    # [Case 6: RHS TypeVar check]
    if is_type_var(rhs):
        return is_subtype(lhs, type_var_to_type(rhs))

    return False
