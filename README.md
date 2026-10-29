# clspack
clspack is a python library that packagizes python classes

## how to use 
install clspack
```
pip install clspack
```

```python
from clspack import pack
# extra imports for class inheritance
from rich.markdown import Markdown
from rich.console import Console


class MyClass(Markdown, Console):
    """class docstring"""
    test = 1
    @classmethod
    def cls_method(cls):
        # hidden classmethod comment
        pass


source = pack(MyClass)                          # return the packed class as a string
pack(MyClass, print_output=True)                # print it
pack(MyClass, output_file="my_class.py")        # save it to a file
```

`pack` always returns the packed source code, `print_output` and `output_file` can be combined.

The packed code contains the imports needed for the parent classes and metaclass, followed by the class source code.
When the class source file is not available (e.g. classes defined in a notebook or an interactive session),
the class is rebuilt member by member from its methods, properties, nested classes and attributes.

## limitations
* imports used inside method bodies or by class decorators (e.g. `@dataclass`) are not added
* parent classes defined in the same module as the packed class are not packed nor imported
