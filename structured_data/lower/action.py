"""
https://schema.org/Action
"""
import enum


class Action(enum.Enum):
    WatchAction = 'https://schema.org/WatchAction'

    def json_serial(self):
        return self._value_
