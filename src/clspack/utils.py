import inspect
import os
import textwrap

# attributes Python adds to every class body that should not be reproduced
_IMPLICIT_ATTRIBUTES = {
    "__module__",
    "__qualname__",
    "__doc__",
    "__dict__",
    "__weakref__",
    "__firstlineno__",
    "__static_attributes__",
    "__annotations__",
    "__annotate__",
    "__annotate_func__",
    "__annotations_cache__",
    "__orig_bases__",
    "__parameters__",
    "__abstractmethods__",
    "_abc_impl",
}


def pack(
    cls,
    output_file: str | os.PathLike | None = None,
    print_output: bool = False,
) -> str:
    """
    Extract and package a Python class source code.

    Args:
        cls: The class to pack
        output_file: Optional file path to save the packed class
        print_output: If True, print the packed class

    Returns:
        The packed class source code as a string

    Raises:
        TypeError: If cls is not a class
    """
    if not inspect.isclass(cls):
        raise TypeError(f"Expected a class, got {type(cls)}")

    imports = _build_imports(cls)
    source = _class_source(cls)
    result = "\n".join(imports) + "\n\n\n" + source if imports else source

    if print_output:
        print(result)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
            f.write("\n")

    return result


def _build_imports(cls) -> list[str]:
    """
    Build the import lines needed for the parent classes and metaclass.

    Args:
        cls: The class to inspect

    Returns:
        Sorted list of import lines
    """
    imports = set()
    metaclass = _explicit_metaclass(cls)
    dependencies = list(cls.__bases__)
    if metaclass is not None:
        dependencies.append(metaclass)

    for dep in dependencies:
        if dep is object or dep.__module__ in ("builtins", cls.__module__):
            continue
        # nested classes are imported through their outermost class
        imports.add(f"from {dep.__module__} import {dep.__qualname__.split('.')[0]}")

    return sorted(imports)


def _explicit_metaclass(cls):
    """
    Get the metaclass only if it is not already inherited from a base class.

    Args:
        cls: The class to inspect

    Returns:
        The metaclass, or None if it is implied
    """
    metaclass = type(cls)
    if metaclass is type or any(type(base) is metaclass for base in cls.__bases__):
        return None
    return metaclass


def _class_source(cls) -> str:
    """
    Get the class source code, rebuilding it if the source file is unavailable.

    Args:
        cls: The class to get the source of

    Returns:
        The class source code
    """
    try:
        return textwrap.dedent(inspect.getsource(cls)).rstrip()
    except (OSError, TypeError):
        # e.g. classes defined in a notebook or an interactive session
        return _rebuild_class(cls)


def _rebuild_class(cls) -> str:
    """
    Rebuild the class source code member by member.

    Args:
        cls: The class to rebuild

    Returns:
        The rebuilt class source code
    """
    parents = [base.__qualname__ for base in cls.__bases__ if base is not object]
    metaclass = _explicit_metaclass(cls)
    if metaclass is not None:
        parents.append(f"metaclass={metaclass.__qualname__}")
    header = (
        f"class {cls.__name__}({', '.join(parents)}):"
        if parents
        else f"class {cls.__name__}:"
    )

    members = []

    if cls.__doc__:
        members.append(_format_docstring(cls.__doc__))

    for key, value in cls.__dict__.items():
        if key in _IMPLICIT_ATTRIBUTES:
            continue

        # Handle classmethods and staticmethods
        if isinstance(value, (classmethod, staticmethod)):
            source = _function_source(value.__func__, key)
            if source:
                members.append(source)
        # Handle properties, the getter/setter/deleter each carry their decorator
        elif isinstance(value, property):
            for func in (value.fget, value.fset, value.fdel):
                source = _function_source(func, key)
                if source:
                    members.append(source)
        # Handle methods and functions
        elif inspect.isfunction(value):
            source = _function_source(value, key)
            if source:
                members.append(source)
        # Handle nested classes (skip references to classes defined elsewhere)
        elif inspect.isclass(value):
            if value.__qualname__ == f"{cls.__qualname__}.{key}":
                members.append(_class_source(value))
        # Handle class attributes (skip non-reproducible runtime objects)
        elif not (key.startswith("__") and key.endswith("__")):
            try:
                attr_repr = repr(value)
            except Exception:  # noqa: BLE001, S112 - arbitrary __repr__ may raise anything
                continue
            if not attr_repr.startswith("<"):
                members.append(f"{key} = {attr_repr}")

    if not members:
        members.append("pass")

    body = "\n\n".join(_indent_source(member, 1) for member in members)
    return f"{header}\n{body}"


def _function_source(func, name: str) -> str | None:
    """
    Get the source code of a function defined in a class body.

    Args:
        func: The function to get the source of
        name: The attribute name the function is stored under

    Returns:
        The function source code, or None if it is unavailable
    """
    # skip functions defined elsewhere and assigned to the class
    if func is None or func.__name__ not in (name, "<lambda>"):
        return None
    try:
        return textwrap.dedent(inspect.getsource(func)).rstrip()
    except (OSError, TypeError):
        # e.g. methods generated by decorators such as @dataclass
        return None


def _format_docstring(doc: str) -> str:
    """
    Format a docstring as a valid triple quoted string literal.

    Args:
        doc: The docstring

    Returns:
        The docstring literal
    """
    doc = inspect.cleandoc(doc)
    doc = doc.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    if doc.endswith('"'):
        doc = doc[:-1] + '\\"'
    if "\n" in doc:
        return f'"""{doc}\n"""'
    return f'"""{doc}"""'


def _indent_source(source: str, level: int = 1) -> str:
    """
    Properly indent source code.

    Args:
        source: The source code to indent
        level: Number of indentation levels (4 spaces each)

    Returns:
        Indented source code
    """
    indent = "    " * level
    dedented = textwrap.dedent(source)
    lines = dedented.split("\n")
    indented_lines = []

    for line in lines:
        if line.strip():
            indented_lines.append(indent + line)
        else:
            indented_lines.append(line)

    return "\n".join(indented_lines)
