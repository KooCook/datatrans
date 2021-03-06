"""

References:
    https://schema.org/Person
"""
from datatrans.structured_data.base import Text, Thing


class Person(Thing):
    PROPERTIES = (
        'name'
    )

    def __init__(self, name: Text):
        self._name: Text = Text(name)


if __name__ == '__main__':
    import json
    from datatrans import utils

    print(json.dumps(Person('Mary Stone'), default=utils.json_encoder))
    pass
