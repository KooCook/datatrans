import datetime
import enum

from datatrans.structured_data.base import Number


class LengthUnit(enum.Enum):
    pass


class Distance:
    """Schema.org's Distance

    Properties that take Distances as values are of the form
    '<Number> <Length unit of measure>'. E.g., '7 ft'.
    """
    def __init__(self, number: Number, unit: LengthUnit):
        self._value = number
        self._unit = unit

    def __str__(self):
        return '{} {}'.format(self._value, self._unit.value)

    def json_serial(self):
        return self.__str__()


class Duration(datetime.timedelta):
    """Schema.org's Duration

    Represents ``Duration``.
    Adds JSON support to Python Standard Library ``datetime.timedelta``

    References:
        https://en.wikipedia.org/wiki/ISO_8601#Durations
    """

    def __str__(self):
        return self.iso_format()

    def iso_format(self) -> str:
        """
        Returns ISO 8601 format duration.
        Year, month, and week is not used due to ambiguity.
        """
        day = '{}D'.format(self.days) if self.days else ''
        hours = self.seconds // 3600
        minutes = (self.seconds % 3600) // 60
        seconds = self.seconds % 60
        time = 'T{}{}{}'.format(
            '{}H'.format(hours) if hours else '',
            '{}M'.format(minutes) if minutes else '',
            '{}S'.format(seconds) if seconds else ''
        )
        return 'P{}{}' .format(day, time) if day or time != 'T' else 'P0D'

    def json_serial(self):
        return self.iso_format()


class EnergyUnit(enum.Enum):
    CALORIE = 'calories'


class Energy:
    """Schema.org's Energy

    Properties that take Energy as values are of the form
    <Number> <Energy unit of measure>'.
    """
    def __init__(self, number: Number, unit: EnergyUnit):
        self._value = number
        self._unit = unit

    def __str__(self):
        return '{} {}'.format(self._value, self._unit.value)

    def json_serial(self):
        return self.__str__()


class MassUnit(enum.Enum):
    KILOGRAM = 'kg'
    GRAM = 'g'
    MILLIGRAM = 'mg'


class Mass:
    """Schema.org's Mass

    Properties that take Mass as values are of the form
    '<Number> <Mass unit of measure>'. E.g., '7 kg'.
    """
    def __init__(self, number: Number, unit: MassUnit):
        self._value = number
        self._unit = unit

    def __str__(self):
        return '{} {}'.format(self._value, self._unit.value)

    def json_serial(self):
        return self.__str__()


if __name__ == '__main__':
    import json
    from datatrans import utils

    print(json.dumps(Duration(minutes=120), default=utils.json_encoder))
    pass
