import inspect
import textwrap
from typing import Optional


def pack(cls, output_file: Optional[str] = None) -> str:
    """
    Extract and package a Python class source code.

    Args:
        cls: The class to pack
        output_file: Optional file path to save the packed class

    Returns:
        The packed class source code as a string

    Raises:
        NotImplementedError: If class is not defined in __main__
        TypeError: If cls is not a class
    """
    if not inspect.isclass(cls):
        raise TypeError(f"Expected a class, got {type(cls)}")

    cls_name = cls.__name__
    cls_module = cls.__module__

    # Build the packed class code
    lines = []

    # Handle imports for parent classes
    imports = []
    parent_classes = []

    for base in cls.__mro__[1:-1]:  # Exclude cls itself and 'object'
        if base.__module__ != cls_module:
            imports.append(f"from {base.__module__} import {base.__name__}")
            parent_classes.append(base.__name__)
        else:
            parent_classes.append(base.__name__)

    # Add imports
    if imports:
        lines.extend(sorted(set(imports)))
        lines.append("")

    # Build class definition
    parents_str = ", ".join(parent_classes) if parent_classes else ""
    lines.append(f"class {cls_name}({parents_str}):")

    # Add docstring
    if cls.__doc__:
        lines.append(f'    """{cls.__doc__}"""')

    # Process class attributes and methods
    for key, value in cls.__dict__.items():
        # Skip special attributes
        if key in ("__module__", "__doc__", "__dict__", "__weakref__"):
            continue

        # Skip dunder methods that are inherited
        if key.startswith("__") and key.endswith("__"):
            if key not in ("__init__", "__new__", "__call__"):
                continue

        # Handle classmethods and staticmethods
        if isinstance(value, (classmethod, staticmethod)):
            try:
                source = inspect.getsource(value.__func__)
                indented_source = _indent_source(source, 1)
                lines.append(indented_source)
            except (OSError, TypeError):
                pass
        # Handle methods and functions
        elif inspect.isfunction(value) or inspect.ismethod(value):
            try:
                source = inspect.getsource(value)
                indented_source = _indent_source(source, 1)
                lines.append(indented_source)
            except (OSError, TypeError):
                pass
        # Handle class attributes
        elif not inspect.isclass(value):
            try:
                attr_repr = repr(value)
                lines.append(f"    {key} = {attr_repr}")
            except Exception:
                pass

    # Join all lines
    result = "\n".join(lines)

    # Save to file if specified
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
            f.write("\n")

    return result


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
