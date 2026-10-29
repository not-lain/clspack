"""Tests for classes whose source file is unavailable (e.g. notebooks)."""

import inspect

import pytest

from clspack import pack
from external import Placeholder
from inheritance import Registry, Shape
from members import Empty, Point

_getsource = inspect.getsource


def _getsource_without_classes(obj):
    if inspect.isclass(obj):
        raise OSError("could not find class definition")
    return _getsource(obj)


@pytest.fixture(autouse=True)
def no_class_source(monkeypatch):
    monkeypatch.setattr("clspack.utils.inspect.getsource", _getsource_without_classes)


def test_external_class():
    result = pack(Placeholder)
    compile(result, "<packed>", "exec")
    assert "class Placeholder:" in result
    assert '"""class docstring"""' in result
    assert "test = 1" in result
    assert "# hidden init comment" in result
    assert "def cls_method(cls):" in result


def test_members_round_trip():
    result = pack(Point)
    assert "class Point:" in result
    assert "()" not in result.splitlines()[0]
    namespace = {}
    exec(result, namespace)
    point_cls = namespace["Point"]
    point = point_cls(3, 4)
    assert repr(point) == "Point(3, 4)"
    point.y = 5
    assert point.y == 5
    assert point_cls.origin_distance(3, 4) == 5
    assert point_cls.Meta.label == "point"
    assert point_cls.__doc__.splitlines()[0] == "A point in 2D space."
    assert '"""triple quotes"""' in point_cls.__doc__


def test_empty_class():
    assert pack(Empty) == "class Empty:\n    pass"


def test_inheritance():
    result = pack(Registry)
    assert result.startswith(
        "from collections import OrderedDict\n\n\nclass Registry(OrderedDict):"
    )


def test_metaclass():
    result = pack(Shape)
    compile(result, "<packed>", "exec")
    assert "class Shape(metaclass=ABCMeta):" in result
    assert "@abstractmethod" in result
