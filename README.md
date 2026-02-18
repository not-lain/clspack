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


pack(MyClass)
```
