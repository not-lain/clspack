import pytest

from clspack import pack
from members import Empty, Point


@pytest.fixture
def packed():
    return pack(Point)


@pytest.mark.parametrize(
    "snippet",
    [
        "class Point:",
        "dims = 2",
        "# hidden init comment",
        "def __repr__(self):",
        "def __eq__(self, other):",
        "@property",
        "@y.setter",
        "@staticmethod",
        "@classmethod",
        "class Meta:",
    ],
)
def test_contains_member(packed, snippet):
    assert snippet in packed


def test_compiles(packed):
    compile(packed, "<packed>", "exec")


def test_round_trip(packed):
    namespace = {}
    exec(packed, namespace)
    point_cls = namespace["Point"]
    point = point_cls(3, 4)
    assert repr(point) == "Point(3, 4)"
    assert point == point_cls(3, 4)
    point.y = 5
    assert point.y == 5
    assert point_cls.origin_distance(3, 4) == 5
    assert point_cls.origin() == point_cls(0, 0)
    assert point_cls.Meta.label == "point"
    assert "triple quotes" in point_cls.__doc__


def test_empty_class():
    assert pack(Empty) == "class Empty:\n    pass"
