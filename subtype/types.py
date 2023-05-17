import typing
from typing import Sequence, Union

__all__: Sequence[str] = ("Type",)


GenericAlias = typing._GenericAlias  # type: ignore
Type = Union[None, type]
