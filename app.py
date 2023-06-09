import typing
from typing import Dict, Generic, Literal, Optional, Protocol, Sequence, Type, TypeVar, Union, NamedTuple
import typing_extensions

# from subtype import normalise
# from subtype.normalisation import _type_var_to_type

# d = normalise(Sequence[int])
# d = normalise(Dict[str, int])

# T = TypeVar("T")
StrOrBytes = TypeVar("StrOrBytes", str, bytes)

# d = normalise(T)

# d = {
#     v.__origin__: v
#     for k, v in typing.__dict__.items()
#     if k in typing.__all__ and isinstance(v, typing._GenericAlias)
# }

# d = normalise(StrOrBytes)

# d1 = normalise(_type_var_to_type(TypeVar("T", str, bytes)))
# d2 = normalise(TypeVar("T", str, bytes))
# d3 = normalise(Union[str, bytes])

# assert normalise(StrOrBytes) == normalise(Union[str, bytes])

# x: Literal["foo", "bar"] = 1
# y: Optional = 1
# z: Union = 1


class Foo(NamedTuple):
    x: int


x: Type[NamedTuple] = Foo

x: Generic = 123
x: Protocol[int] = 123