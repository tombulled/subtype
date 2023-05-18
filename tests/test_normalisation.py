import collections.abc
import decimal
from typing import (Any, AsyncIterable, AsyncIterator, Awaitable, ByteString,
                    Callable, ClassVar, Collection, Container, Coroutine, Final,
                    Generator, Hashable, ItemsView, Iterable, Iterator,
                    KeysView, List, Literal, Mapping, MappingView, MutableMapping,
                    MutableSequence, MutableSet, Optional, Reversible, Sequence, Set,
                    Sized, Tuple, Type, TypeVar, Union, ValuesView)

import pytest
from typing_extensions import ParamSpec

from subtype import NormalisedType, normalise


def n(*args) -> NormalisedType:
    return NormalisedType(*args)


# TODO:
#   * ForwardRef
@pytest.mark.parametrize(
    "type_,expected",
    (
        # builtins
        (None, n(None)),
        (int, n(int)),
        (str, n(str)),
        (complex, n(complex)),
        (bytes, n(bytes)),
        (bool, n(bool)),
        (float, n(float)),
        (object, n(object)),
        (type, n(type, (n(Any),))),
        (bytearray, n(bytearray)),
        (decimal.Decimal, n(decimal.Decimal)),
        (list, n(list, (n(Any),))),
        (tuple, n(tuple, (n(Any), n(...)))),
        (set, n(set, (n(Any),))),
        # Super-special typing primitives.
        (Any, n(Any)),
        (Callable, n(collections.abc.Callable, (n(...), n(Any)))),
        (
            Callable[[str, int], bool],
            n(
                collections.abc.Callable,
                (
                    n(str),
                    n(int),
                    n(bool),
                ),
            ),
        ),
        # vvv currently not implemented
        # (Callable[ParamSpec("PS"), Any], n(collections.abc.Callable, (n(...), n(Any)))),
        (ClassVar, n(ClassVar, (n(Any),))),
        (ClassVar[int], n(ClassVar, (n(int),))),
        (Final, n(Final, (n(Any),))),
        (Final[int], n(Final, (n(int),))),
        # TODO: 'ForwardRef'
        # TODO: 'Generic'
        # TODO: 'Literal' with no args should throw exception
        (Literal["fish", 123], n(Literal, (n("fish"), n(123)))),
        # TODO: 'Optional' with no args should throw exception
        (Optional[int], n(Union, (n(int), n(type(None))))),
        # TODO: 'Protocol'
        (Tuple, n(tuple, (n(Any), n(...)))),
        (Tuple[int, ...], n(tuple, (n(int), n(...)))),
        (Tuple[int, str], n(tuple, (n(int), n(str)))),
        (Type, n(type, (n(Any),))),
        (Type[int], n(type, (n(int),))),
        (TypeVar("T"), n(Any)),
        (TypeVar("T", bound=int), n(int)),
        (TypeVar("T", str, bytes), n(Union, (n(str), n(bytes)))),
        # TODO: 'Union' with no args should throw exception
        (Union[int, str], n(Union, (n(int), n(str)))),
        # Types from `typing` (no type parameters)
        (List, n(list, (n(Any),))),
        (Container, n(collections.abc.Container, (n(Any),))),
        (Hashable, n(collections.abc.Hashable)),
        (Sized, n(collections.abc.Sized)),
        (Iterable, n(collections.abc.Iterable, (n(Any),))),
        (Collection, n(collections.abc.Collection, (n(Any),))),
        (Iterator, n(collections.abc.Iterator, (n(Any),))),
        (Reversible, n(collections.abc.Reversible, (n(Any),))),
        (Generator, n(collections.abc.Generator, (n(Any), n(Any), n(Any)))),
        (Sequence, n(collections.abc.Sequence, (n(Any),))),
        (MutableSequence, n(collections.abc.MutableSequence, (n(Any),))),
        (ByteString, n(collections.abc.ByteString)),
        (Set, n(set, (n(Any),))),
        (MutableSet, n(collections.abc.MutableSet, (n(Any),))),
        (Mapping, n(collections.abc.Mapping, (n(Any), n(Any)))),
        (MutableMapping, n(collections.abc.MutableMapping, (n(Any), n(Any)))),
        (MappingView, n(collections.abc.MappingView, (n(Any),))),
        (ItemsView, n(collections.abc.ItemsView, (n(Any), n(Any)))),
        (KeysView, n(collections.abc.KeysView, (n(Any),))),
        (ValuesView, n(collections.abc.ValuesView, (n(Any),))),
        (Awaitable, n(collections.abc.Awaitable, (n(Any),))),
        (Coroutine, n(collections.abc.Coroutine, (n(Any), n(Any), n(Any)))),
        (AsyncIterable, n(collections.abc.AsyncIterable, (n(Any),))),
        (AsyncIterator, n(collections.abc.AsyncIterator, (n(Any),))),
        # Types from `typing` (with type parameters)
        (List[int], n(list, (n(int),))),
        # Type variables
    ),
)
def test_normalise(type_: Any, expected: NormalisedType) -> None:
    assert normalise(type_) == expected
