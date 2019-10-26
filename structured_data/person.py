"""
https://schema.org/Person
"""
from structured_data.base import Text, Thing


class Person(Thing):
    PROPERTIES = (
        'name'
    )

    def __init__(self, name: Text):
        self._name: Text = Text(name)


if __name__ == '__main__':
    pass
