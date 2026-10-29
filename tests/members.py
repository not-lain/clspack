class Point:
    """A point in 2D space.

    Docstring with \"\"\"triple quotes\"\"\" inside.
    """

    dims = 2

    def __init__(self, x, y):
        # hidden init comment
        self.x = x
        self._y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @staticmethod
    def origin_distance(x, y):
        return (x**2 + y**2) ** 0.5

    @classmethod
    def origin(cls):
        return cls(0, 0)

    class Meta:
        """nested class"""

        label = "point"


class Empty:
    pass
