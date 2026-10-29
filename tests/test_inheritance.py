from clspack import pack
from inheritance import Child, CustomError, Registry, Shape


def test_external_base_is_imported():
    result = pack(Registry)
    assert result.startswith(
        "from collections import OrderedDict\n\n\nclass Registry(OrderedDict):"
    )


def test_builtin_base_is_not_imported():
    result = pack(CustomError)
    assert "import" not in result
    assert result.startswith("class CustomError(Exception):")


def test_same_module_base_is_not_imported():
    result = pack(Child)
    assert "import" not in result
    assert "class Child(Base):" in result


def test_metaclass_is_imported():
    result = pack(Shape)
    assert "from abc import ABCMeta" in result
    assert "class Shape(metaclass=ABCMeta):" in result


def test_round_trip():
    namespace = {}
    exec(pack(Registry), namespace)
    registry = namespace["Registry"](a=1, b=2)
    assert registry.first() == "a"
