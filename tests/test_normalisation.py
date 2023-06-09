import collections.abc
import contextlib
import decimal
import typing as t
import typing_extensions as te
from typing import (
    AbstractSet,
    Any,
    AnyStr,
    AsyncContextManager,
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    ByteString,
    Callable,
    ChainMap,
    ClassVar,
    Collection,
    Container,
    ContextManager,
    Coroutine,
    Counter,
    DefaultDict,
    Deque,
    Dict,
    Final,
    FrozenSet,
    Generator,
    Generic,
    Hashable,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    List,
    Literal,
    Mapping,
    MappingView,
    MutableMapping,
    MutableSequence,
    MutableSet,
    NamedTuple,
    NoReturn,
    Optional,
    OrderedDict,
    Protocol,
    Reversible,
    Sequence,
    Set,
    Sized,
    SupportsAbs,
    SupportsBytes,
    SupportsComplex,
    SupportsFloat,
    SupportsIndex,
    SupportsInt,
    SupportsRound,
    Text,
    Tuple,
    Type,
    TypeVar,
    TypedDict,
    Union,
    ValuesView,
)

import pytest
from typing_extensions import ParamSpec

from subtype import NormalisedType, normalise

T = TypeVar("T")
PS = ParamSpec("PS")


def n(*args) -> NormalisedType:
    return NormalisedType(*args)


# TODO:
#   * ForwardRef
#   typing_extensions, e.g. Self and Annotated
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
        (dict, n(dict, (n(Any), n(Any)))),
        (collections.deque, n(collections.deque, (n(Any),))),
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
        #   E.g. ForwardRef["int"] -> int
        (Literal["fish", 123], n(Literal, (n("fish"), n(123)))),
        (Optional[int], n(Union, (n(int), n(type(None))))),
        (Tuple, n(tuple, (n(Any), n(...)))),
        (Tuple[int, ...], n(tuple, (n(int), n(...)))),
        (Tuple[int, str], n(tuple, (n(int), n(str)))),
        (Type, n(type, (n(Any),))),
        (Type[int], n(type, (n(int),))),
        (TypeVar("T"), n(Any)),
        (TypeVar("T", bound=int), n(int)),
        (TypeVar("T", str, bytes), n(Union, (n(str), n(bytes)))),
        (Union[int, str], n(Union, (n(int), n(str)))),
        # ABCs (from collections.abc).
        (AbstractSet, n(collections.abc.Set, (n(Any),))),
        (AbstractSet[str], n(collections.abc.Set, (n(str),))),
        (ByteString, n(collections.abc.ByteString)),
        (Container, n(collections.abc.Container, (n(Any),))),
        (Container[int], n(collections.abc.Container, (n(int),))),
        (ContextManager, n(contextlib.AbstractContextManager, (n(Any),))),
        (ContextManager[int], n(contextlib.AbstractContextManager, (n(int),))),
        (Hashable, n(collections.abc.Hashable)),
        (ItemsView, n(collections.abc.ItemsView, (n(Any), n(Any)))),
        (ItemsView[str, int], n(collections.abc.ItemsView, (n(str), n(int)))),
        (Iterable, n(collections.abc.Iterable, (n(Any),))),
        (Iterable[str], n(collections.abc.Iterable, (n(str),))),
        (Iterator, n(collections.abc.Iterator, (n(Any),))),
        (Iterator[str], n(collections.abc.Iterator, (n(str),))),
        (KeysView, n(collections.abc.KeysView, (n(Any),))),
        (KeysView[str], n(collections.abc.KeysView, (n(str),))),
        (Mapping, n(collections.abc.Mapping, (n(Any), n(Any)))),
        (Mapping[str, int], n(collections.abc.Mapping, (n(str), n(int)))),
        (MappingView, n(collections.abc.MappingView, (n(Any),))),
        (MappingView[str], n(collections.abc.MappingView, (n(str),))),
        (MutableMapping, n(collections.abc.MutableMapping, (n(Any), n(Any)))),
        (MutableMapping[str, int], n(collections.abc.MutableMapping, (n(str), n(int)))),
        (MutableSequence, n(collections.abc.MutableSequence, (n(Any),))),
        (MutableSequence[str], n(collections.abc.MutableSequence, (n(str),))),
        (MutableSet, n(collections.abc.MutableSet, (n(Any),))),
        (MutableSet[str], n(collections.abc.MutableSet, (n(str),))),
        (Sequence, n(collections.abc.Sequence, (n(Any),))),
        (Sequence[str], n(collections.abc.Sequence, (n(str),))),
        (Sized, n(collections.abc.Sized)),
        (ValuesView, n(collections.abc.ValuesView, (n(Any),))),
        (ValuesView[str], n(collections.abc.ValuesView, (n(str),))),
        (Awaitable, n(collections.abc.Awaitable, (n(Any),))),
        (Awaitable[str], n(collections.abc.Awaitable, (n(str),))),
        (AsyncIterator, n(collections.abc.AsyncIterator, (n(Any),))),
        (AsyncIterator[str], n(collections.abc.AsyncIterator, (n(str),))),
        (AsyncIterable, n(collections.abc.AsyncIterable, (n(Any),))),
        (AsyncIterable[str], n(collections.abc.AsyncIterable, (n(str),))),
        (Coroutine, n(collections.abc.Coroutine, (n(Any), n(Any), n(Any)))),
        (
            Coroutine[str, int, bool],
            n(collections.abc.Coroutine, (n(str), n(int), n(bool))),
        ),
        (Collection, n(collections.abc.Collection, (n(Any),))),
        (Collection[str], n(collections.abc.Collection, (n(str),))),
        (AsyncGenerator, n(collections.abc.AsyncGenerator, (n(Any), n(Any)))),
        (AsyncGenerator[int, str], n(collections.abc.AsyncGenerator, (n(int), n(str)))),
        (AsyncContextManager, n(contextlib.AbstractAsyncContextManager, (n(Any),))),
        (
            AsyncContextManager[int],
            n(contextlib.AbstractAsyncContextManager, (n(int),)),
        ),
        # Structural checks, a.k.a. protocols.
        (Reversible, n(collections.abc.Reversible, (n(Any),))),
        (Reversible[str], n(collections.abc.Reversible, (n(str),))),

        # WARN: Currently broken vvv
        # (SupportsAbs, n(SupportsAbs, (n(Any),))),
        (SupportsBytes, n(SupportsBytes)),
        (SupportsComplex, n(SupportsComplex)),
        (SupportsFloat, n(SupportsFloat)),
        (SupportsIndex, n(SupportsIndex)),
        (SupportsInt, n(SupportsInt)),
        # WARN: Currently broken vvv
        # (SupportsRound, n(SupportsRound, (n(Any),))),
        # Concrete collection types.
        (ChainMap, n(collections.ChainMap, (n(Any), n(Any)))),
        (ChainMap[str, int], n(collections.ChainMap, (n(str), n(int)))),
        (Counter, n(collections.Counter, (n(Any),))),
        (Counter[int], n(collections.Counter, (n(int),))),
        (Deque, n(collections.deque, (n(Any),))),
        (Deque[int], n(collections.deque, (n(int),))),
        (Dict, n(dict, (n(Any), n(Any)))),
        (Dict[str, int], n(dict, (n(str), n(int)))),
        (DefaultDict, n(collections.defaultdict, (n(Any), n(Any)))),
        (DefaultDict[str, int], n(collections.defaultdict, (n(str), n(int)))),
        (List, n(list, (n(Any),))),
        (List[int], n(list, (n(int),))),
        (OrderedDict, n(collections.OrderedDict, (n(Any), n(Any)))),
        (OrderedDict[str, int], n(collections.OrderedDict, (n(str), n(int)))),
        (Set, n(set, (n(Any),))),
        (Set[str], n(set, (n(str),))),
        (FrozenSet, n(frozenset, (n(Any),))),
        (FrozenSet[str], n(frozenset, (n(str),))),
        (NamedTuple, n(NamedTuple)),
        (TypedDict, n(TypedDict)),
        (Generator, n(collections.abc.Generator, (n(Any), n(Any), n(Any)))),
        (
            Generator[int, str, bool],
            n(collections.abc.Generator, (n(int), n(str), n(bool))),
        ),
        # One-off things.
        (AnyStr, n(Union, (n(bytes), n(str)))),
        (NoReturn, n(NoReturn)),
        (Text, n(Text)),
        # Type variables
        # ...
    ),
)
def test_normalise(type_: Any, expected: NormalisedType) -> None:
    assert normalise(type_) == expected


@pytest.mark.parametrize(
    "type_",
    (
        # TODO: 'Generic', with or without args should throw an exception
        Generic,
        Generic[T],
        Literal,
        Optional,
        # TODO: 'Protocol', with or without args should throw an exception
        Protocol,
        Protocol[T],
        # TODO: 'Union' with no args should throw exception
        Union,
    )
)
def test_normalise_raises_exception(type_: Any) -> None:
    with pytest.raises(ValueError):
        normalise(type_)