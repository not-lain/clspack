import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(__file__))

from clspack import pack
from external import Placeholder

class MyClass:
    """hi"""

    test = 1

    def __init__(self):
        # hidden init comment
        pass

    @classmethod
    def cls_method(cls):
        pass


def test_local_class_contains_header():
    result = pack(MyClass)
    assert "class MyClass" in result


def test_local_class_contains_init():
    result = pack(MyClass)
    assert "def __init__" in result


def test_local_class_contains_classmethod():
    result = pack(MyClass)
    assert "def cls_method" in result


def test_local_class_contains_attribute():
    result = pack(MyClass)
    assert "test = 1" in result


def test_local_class_returns_string():
    assert isinstance(pack(MyClass), str)

def test_external_class_contains_header():
    result = pack(Placeholder)
    assert "class Placeholder" in result


def test_external_class_contains_init():
    result = pack(Placeholder)
    assert "def __init__" in result


def test_external_class_contains_classmethod():
    result = pack(Placeholder)
    assert "def cls_method" in result


def test_external_class_contains_attribute():
    result = pack(Placeholder)
    assert "test = 1" in result


def test_external_class_returns_string():
    assert isinstance(pack(Placeholder), str)


def test_raises_for_non_class_int():
    with pytest.raises(TypeError):
        pack(42)


def test_raises_for_non_class_string():
    with pytest.raises(TypeError):
        pack("not a class")
