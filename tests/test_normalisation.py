import collections.abc
import contextlib
import decimal
import typing as t

import pytest
from typing_extensions import ParamSpec

from subtype.normalisation import NormalisedType, normalise

T = t.TypeVar("T")
PS = ParamSpec("PS")


def n(*args) -> NormalisedType:
    return NormalisedType(*args)


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
        (type, n(type, (n(t.Any),))),
        (bytearray, n(bytearray)),
        (decimal.Decimal, n(decimal.Decimal)),
        (list, n(list, (n(t.Any),))),
        (tuple, n(tuple, (n(t.Any), n(...)))),
        (set, n(set, (n(t.Any),))),
        (dict, n(dict, (n(t.Any), n(t.Any)))),
        (collections.deque, n(collections.deque, (n(t.Any),))),
        # Super-special typing primitives.
        (t.Any, n(t.Any)),
        (t.Callable, n(collections.abc.Callable, (n(...), n(t.Any)))),
        (
            t.Callable[[str, int], bool],
            n(
                collections.abc.Callable,
                (
                    n(str),
                    n(int),
                    n(bool),
                ),
            ),
        ),
        # TODO: vvv currently not implemented
        # (Callable[ParamSpec("PS"), Any], n(collections.abc.Callable, (n(...), n(Any)))),
        (t.ClassVar, n(t.ClassVar, (n(t.Any),))),
        (t.ClassVar[int], n(t.ClassVar, (n(int),))),
        (t.Final, n(t.Final, (n(t.Any),))),
        (t.Final[int], n(t.Final, (n(int),))),
        (t.ForwardRef, n(t.ForwardRef)),
        (t.Literal["fish", 123], n(t.Literal, (n("fish"), n(123)))),
        (t.Optional[int], n(t.Union, (n(int), n(type(None))))),
        (t.Tuple, n(tuple, (n(t.Any), n(...)))),
        (t.Tuple[int, ...], n(tuple, (n(int), n(...)))),
        (t.Tuple[int, str], n(tuple, (n(int), n(str)))),
        (t.Type, n(type, (n(t.Any),))),
        (t.Type[int], n(type, (n(int),))),
        (t.TypeVar("T"), n(t.Any)),
        (t.TypeVar("T", bound=int), n(int)),
        (t.TypeVar("T", str, bytes), n(t.Union, (n(str), n(bytes)))),
        (t.Union[int, str], n(t.Union, (n(int), n(str)))),
        # ABCs (from collections.abc).
        (t.AbstractSet, n(collections.abc.Set, (n(t.Any),))),
        (t.AbstractSet[str], n(collections.abc.Set, (n(str),))),
        (t.ByteString, n(collections.abc.ByteString)),
        (t.Container, n(collections.abc.Container, (n(t.Any),))),
        (t.Container[int], n(collections.abc.Container, (n(int),))),
        (t.ContextManager, n(contextlib.AbstractContextManager, (n(t.Any),))),
        (t.ContextManager[int], n(contextlib.AbstractContextManager, (n(int),))),
        (t.Hashable, n(collections.abc.Hashable)),
        (t.ItemsView, n(collections.abc.ItemsView, (n(t.Any), n(t.Any)))),
        (t.ItemsView[str, int], n(collections.abc.ItemsView, (n(str), n(int)))),
        (t.Iterable, n(collections.abc.Iterable, (n(t.Any),))),
        (t.Iterable[str], n(collections.abc.Iterable, (n(str),))),
        (t.Iterator, n(collections.abc.Iterator, (n(t.Any),))),
        (t.Iterator[str], n(collections.abc.Iterator, (n(str),))),
        (t.KeysView, n(collections.abc.KeysView, (n(t.Any),))),
        (t.KeysView[str], n(collections.abc.KeysView, (n(str),))),
        (t.Mapping, n(collections.abc.Mapping, (n(t.Any), n(t.Any)))),
        (t.Mapping[str, int], n(collections.abc.Mapping, (n(str), n(int)))),
        (t.MappingView, n(collections.abc.MappingView, (n(t.Any),))),
        (t.MappingView[str], n(collections.abc.MappingView, (n(str),))),
        (t.MutableMapping, n(collections.abc.MutableMapping, (n(t.Any), n(t.Any)))),
        (
            t.MutableMapping[str, int],
            n(collections.abc.MutableMapping, (n(str), n(int))),
        ),
        (t.MutableSequence, n(collections.abc.MutableSequence, (n(t.Any),))),
        (t.MutableSequence[str], n(collections.abc.MutableSequence, (n(str),))),
        (t.MutableSet, n(collections.abc.MutableSet, (n(t.Any),))),
        (t.MutableSet[str], n(collections.abc.MutableSet, (n(str),))),
        (t.Sequence, n(collections.abc.Sequence, (n(t.Any),))),
        (t.Sequence[str], n(collections.abc.Sequence, (n(str),))),
        (t.Sized, n(collections.abc.Sized)),
        (t.ValuesView, n(collections.abc.ValuesView, (n(t.Any),))),
        (t.ValuesView[str], n(collections.abc.ValuesView, (n(str),))),
        (t.Awaitable, n(collections.abc.Awaitable, (n(t.Any),))),
        (t.Awaitable[str], n(collections.abc.Awaitable, (n(str),))),
        (t.AsyncIterator, n(collections.abc.AsyncIterator, (n(t.Any),))),
        (t.AsyncIterator[str], n(collections.abc.AsyncIterator, (n(str),))),
        (t.AsyncIterable, n(collections.abc.AsyncIterable, (n(t.Any),))),
        (t.AsyncIterable[str], n(collections.abc.AsyncIterable, (n(str),))),
        (t.Coroutine, n(collections.abc.Coroutine, (n(t.Any), n(t.Any), n(t.Any)))),
        (
            t.Coroutine[str, int, bool],
            n(collections.abc.Coroutine, (n(str), n(int), n(bool))),
        ),
        (t.Collection, n(collections.abc.Collection, (n(t.Any),))),
        (t.Collection[str], n(collections.abc.Collection, (n(str),))),
        (t.AsyncGenerator, n(collections.abc.AsyncGenerator, (n(t.Any), n(t.Any)))),
        (
            t.AsyncGenerator[int, str],
            n(collections.abc.AsyncGenerator, (n(int), n(str))),
        ),
        (t.AsyncContextManager, n(contextlib.AbstractAsyncContextManager, (n(t.Any),))),
        (
            t.AsyncContextManager[int],
            n(contextlib.AbstractAsyncContextManager, (n(int),)),
        ),
        # Structural checks, a.k.a. protocols.
        (t.Reversible, n(collections.abc.Reversible, (n(t.Any),))),
        (t.Reversible[str], n(collections.abc.Reversible, (n(str),))),
        (t.SupportsAbs, n(t.SupportsAbs, (n(t.Any),))),
        (t.SupportsBytes, n(t.SupportsBytes)),
        (t.SupportsComplex, n(t.SupportsComplex)),
        (t.SupportsFloat, n(t.SupportsFloat)),
        (t.SupportsIndex, n(t.SupportsIndex)),
        (t.SupportsInt, n(t.SupportsInt)),
        (t.SupportsRound, n(t.SupportsRound, (n(t.Any),))),
        # Concrete collection types.
        (t.ChainMap, n(collections.ChainMap, (n(t.Any), n(t.Any)))),
        (t.ChainMap[str, int], n(collections.ChainMap, (n(str), n(int)))),
        (t.Counter, n(collections.Counter, (n(t.Any),))),
        (t.Counter[int], n(collections.Counter, (n(int),))),
        (t.Deque, n(collections.deque, (n(t.Any),))),
        (t.Deque[int], n(collections.deque, (n(int),))),
        (t.Dict, n(dict, (n(t.Any), n(t.Any)))),
        (t.Dict[str, int], n(dict, (n(str), n(int)))),
        (t.DefaultDict, n(collections.defaultdict, (n(t.Any), n(t.Any)))),
        (t.DefaultDict[str, int], n(collections.defaultdict, (n(str), n(int)))),
        (t.List, n(list, (n(t.Any),))),
        (t.List[int], n(list, (n(int),))),
        (t.OrderedDict, n(collections.OrderedDict, (n(t.Any), n(t.Any)))),
        (t.OrderedDict[str, int], n(collections.OrderedDict, (n(str), n(int)))),
        (t.Set, n(set, (n(t.Any),))),
        (t.Set[str], n(set, (n(str),))),
        (t.FrozenSet, n(frozenset, (n(t.Any),))),
        (t.FrozenSet[str], n(frozenset, (n(str),))),
        (t.NamedTuple, n(t.NamedTuple)),
        (t.TypedDict, n(t.TypedDict)),
        (t.Generator, n(collections.abc.Generator, (n(t.Any), n(t.Any), n(t.Any)))),
        (
            t.Generator[int, str, bool],
            n(collections.abc.Generator, (n(int), n(str), n(bool))),
        ),
        # One-off things.
        (t.AnyStr, n(t.Union, (n(bytes), n(str)))),
        (t.NoReturn, n(t.NoReturn)),
        (t.Text, n(t.Text)),
        # Type variables
        # TODO ...
        # Typing extensions (from `typing_extensions`)
        # TODO ...
    ),
)
def test_normalise(type_: t.Any, expected: NormalisedType) -> None:
    assert normalise(type_) == expected


@pytest.mark.parametrize(
    "type_",
    (
        t.Generic,
        t.Generic[T],
        t.Literal,
        t.Optional,
        t.Protocol,
        t.Protocol[T],
        t.Union,
        t.ForwardRef("SomeClass"),
    ),
)
def test_normalise_raises_exception(type_: t.Any) -> None:
    with pytest.raises(ValueError):
        normalise(type_)
