from typing import List
import abc
import json

from structured_data import utils


class Thing(metaclass=abc.ABCMeta):

    PROPERTIES = NotImplemented

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.PROPERTIES is NotImplemented:
            raise NotImplementedError('class attribute \'PROPERTIES\' is not '
                                      'defined in {}'.format(cls.__name__))

    def json_serial(self):
        return {utils.snake_to_camel(k): v for k, v in self.__dict__.items()
                if utils.snake_to_camel(k) in self.PROPERTIES}

    def __str__(self):
        return json.dumps(self, default=utils.default)

    def get_type_specification(self) -> str:
        return '"@type":"{}"'.format(self.__class__.__name__)

    def add_context(self, context: str = 'https://schema.org/'):
        from structured_data.base.data_type import Text
        self._context = Text(context)

    def has_context(self):
        return hasattr(self, '_context')

    @property
    def context(self):
        if self.has_context():
            return self._context
        raise AttributeError('This \'Thing\' has no \'context\'')


class Property(list, List):
    """
    Represents a JSON-LD property.
    """
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        if self.__len__() == 0:
            return ''
        if self.__len__() == 1:
            return super().__repr__()[1:-1]
        return super().__repr__()


if __name__ == '__main__':
    pass
