import abc
import json
from typing import List

from structured_data import utils


class Thing(metaclass=abc.ABCMeta):

    PROPERTIES = NotImplemented

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.PROPERTIES is NotImplemented:
            raise NotImplementedError('class attribute \'PROPERTIES\' is not '
                                      'defined in {}'.format(cls.__name__))

    def json_serial(self):
        properties = {'@type': self.type}
        for k, v in self.__dict__.items():
            if utils.snake_to_camel(k) in self.PROPERTIES and v is not None:
                properties[utils.snake_to_camel(k)] = v
        return properties

    def __str__(self):
        return json.dumps(self, default=utils.default)

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def add_context(self, context: str = 'https://schema.org/'):
        from structured_data.base.data_type import Text
        self._context = Text(context)

    def has_context(self):
        return hasattr(self, '_context')

    @property
    def context(self) -> str:
        if self.has_context():
            return self._context
        raise AttributeError('This \'Thing\' has no \'context\'')


class Property(list, List):
    """
    Represents a JSON-LD property.
    """
    def __init__(self, *args, class_=None):
        if class_ is not None:
            super().__init__(map(class_, args))
        else:
            super().__init__(args)

    def __repr__(self):
        if self.__len__() == 0:
            return ''
        if self.__len__() == 1:
            return super().__repr__()[1:-1]
        return super().__repr__()

    # TODO: Fix JSONEncoder (list of 1 item should be change to the item itself)


if __name__ == '__main__':
    from structured_data.base.data_type import Text
    urls = [
        Text('http://example.com/coffee_cake.html'),
    ]
    print(Property(*urls))
    t = Thing()
    print(t.has_context())
    t.add_context()
    print(t.context)
    pass
