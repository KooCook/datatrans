from operator import itemgetter
from typing import Iterable
import warnings
import json

from datatrans.utils.functions import snake_to_camel
from datatrans.utils.classes.encoder import JSONEncoder

__all__ = ['DataClass']


def one_itemgetter(*items):
    def get(obj):
        for item in items:
            try:
                return obj[item]
            except IndexError:
                pass
            except KeyError:
                pass
        if isinstance(items, int):
            raise IndexError('tuple index out of range')
        raise KeyError('no keys matching {}'.format(str(items)[1:-1]))
    return get


def none_or_itemgetter(item, *items):
    if items:
        raise NotImplementedError

    def get(obj):
        try:
            return obj[item]
        except IndexError:
            return None
        except KeyError:
            return None
    return get


class DataClassMeta(type):
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        try:
            if name != 'DataClass' and namespace['__attr__'] == ():
                raise AttributeError('class attribute \'__attr__\' is not '
                                     'defined in {}'.format(name))
        except KeyError:
            raise AttributeError('class attribute \'__attr__\' is not '
                                 'defined in {}'.format(name))

        try:
            namespace['__slots__'] = tuple(map(itemgetter(0), namespace['__attr__']))
            # __types__ and __inits__ are constructed here so that
            # the error comes up in class creation time
            namespace['__types__'] = tuple(map(itemgetter(1), namespace['__attr__']))
            namespace['__inits__'] = tuple(map(one_itemgetter(2, 1), namespace['__attr__']))
            namespace['__params__'] = tuple(map(none_or_itemgetter(3), namespace['__attr__']))
        except IndexError as e:
            raise AttributeError('class {} is missing some type specification '
                                 'in __attr__'.format(name)) from e.__context__

        return super().__new__(mcs, name, bases, namespace)


def validate_data_empty(_dict_: dict, strict: bool, suppress_warning: bool) -> None:
    """ Raises exception or warning if _dict_ is not empty. """
    if len(_dict_) != 0:
        if strict:
            raise ValueError(
                'Extra keys unused \'{}\' '.format(_dict_)
            )
        elif suppress_warning:
            warnings.warn(
                'Extra keys unused \'{}\' '.format(_dict_),
                ResourceWarning)


class DataClass(metaclass=DataClassMeta):

    __attr__ = ()
    # ((name, type[, init][, kwargs]), ...)

    def __init__(self, _dict_: dict = None, **kwargs):
        """

        Args:
            _dict_: A dict with fields in camelCase to base data class on
        """
        if _dict_ is None:
            _dict_ = {}
        elif not isinstance(_dict_, dict):
            raise ValueError('\'_dict_\' should be a \'dict\'')

        # try:
        #     types = list(map(itemgetter(1), self.__attr__))
        #     inits = list(map(one_itemgetter(2, 1), self.__attr__))
        # except IndexError as e:
        #     raise AttributeError('class {} is missing some type specification '
        #                          'in __attr__'.format(self.__class__.__name__)
        #                          ) from e.__context__

        for i in range(len(self.__slots__)):
            attr = self.__slots__[i]
            type_ = self.__types__[i]
            init = self.__inits__[i]
            params = self.__params__[i]
            try:
                if _dict_[snake_to_camel(attr)] is not None:
                    # so that TypeError isn't raised and falsely suppressed
                    if params is None:
                        setattr(self, attr, init(_dict_.pop(snake_to_camel(attr))))
                    else:
                        setattr(self, attr, init(_dict_.pop(snake_to_camel(attr)), **params))
                else:
                    setattr(self, attr, None)
            except KeyError:
                setattr(self, attr, None)
            value = getattr(self, attr)
            if not isinstance(value, type_) and value is not None:
                raise TypeError('instance attribute \'{}\' is not of '
                                'specified type (\'{}\' is not \'{}\')'
                                .format(attr, type(value), type_))

        validate_data_empty(_dict_, kwargs.pop('strict', True), kwargs.pop('suppress_warning', False))

    @property
    def dict(self) -> dict:
        """ Returns a dict of the data with fields in camelCase. """
        return {snake_to_camel(field): getattr(self, field)
                for field in self.__slots__
                if getattr(self, field) is not None}

    def items(self) -> Iterable:
        return self.dict.items()

    def json_serial(self):
        return self.dict

    def __repr__(self):
        return json.dumps(self.dict, cls=JSONEncoder)
