import pytest

from lab2.graphic_sequence import validate_graphic_sequence


@pytest.mark.parametrize(
    "sequence, expected",
    [
        ([2, 2, 2], True),
        ([3, 3, 1, 1], False),
        ([2, -1, 1], False),
        ([1, 1, 1], False),
        ([0, 0, 0], True),
        ([], True),
        ([1, 1], True),
        ([3, 3, 2, 2, 2], True),
        ([4, 1, 1, 1, 1], True),
        ([5, 1, 1, 1, 1], False),
        # from presentation
        ([1, 3, 2, 3, 2, 4, 1], True),
        ([1, 3, 3, 4, 2, 3, 1], False),
        ([1, 3, 3, 7, 2, 3, 1], False),
        ([2, 2, 6, 4, 4, 6, 6], False)
    ],
)
def test_validate_graphic_sequence(sequence, expected):
    assert validate_graphic_sequence(sequence) is expected