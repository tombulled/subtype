import builtins
import typing
from dataclasses import dataclass, field
from typing import Sequence, Tuple, Union

__all__: Sequence[str] = ("NormalisedType",)

Type = Union[None, type, typing._GenericAlias, type(...)]  # type: ignore

def _get_name(type_: Type) -> str:
    if type_ is None:
        return str(None)
    elif type_ is Ellipsis:
        return "..."
    elif isinstance(type_, typing._GenericAlias):  # type: ignore
        return str(type_)
    else:
        name: str = ""

        module: str = type_.__module__

        if module != builtins.__name__:
            name += f".{module}"

        return name + type_.__name__


@dataclass(frozen=True)
class NormalisedType:
    origin: Type
    args: Tuple["NormalisedType", ...] = field(default_factory=tuple)

    def __repr__(self) -> str:
        representation: str =  _get_name(self.origin)

        if self.args:
            representation += f"[{', '.join(repr(arg) for arg in self.args)}]"

        return representation