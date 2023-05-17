import collections.abc
from typing import Any, Callable, List, Sequence, Tuple

import pytest

from subtype import NormalisedType, normalise


def n(*args) -> NormalisedType:
    return NormalisedType(*args)


@pytest.mark.parametrize(
    "type_,expected",
    (
        (None, n(type(None))),
        (int, n(int)),
        (str, n(str)),
        (bytes, n(bytes)),
        (bool, n(bool)),
        (float, n(float)),
        (object, n(object)),
        (type, n(type)),
        (Any, n(Any)),
        (List, n(list, (n(Any),))),
        (Tuple, n(tuple, (n(Any), n(...)))),
        (Sequence, n(collections.abc.Sequence, (n(Any),))),
        (Callable, n(collections.abc.Callable, (n(...), n(Any)))),
        (List[int], n(list, (n(int),))),
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
    ),
)
def test_normalise(type_: Any, expected: NormalisedType) -> None:
    assert normalise(type_) == expected
