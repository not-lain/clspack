# clspack
clspack is a python library that packagizes python classes

## how to use 
install clspack
```
pip install clspack
```

define your class in main

```python
class MyClass():
  """hi"""
  test = 1
  def __init__(self):
    # hidden init comment
    pass
  @classmethod
  def cls_method(cls):
    pass
```
get source code for your class
```python
from clspack import pack
pack(MyClass)
```
