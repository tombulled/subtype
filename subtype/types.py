import typing
from typing import Sequence, Union

__all__: Sequence[str] = (
    "GenericAlias",
    "Type",
)


GenericAlias = typing._GenericAlias  # type: ignore
Type = Union[None, type]
