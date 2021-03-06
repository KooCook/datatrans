import datetime
import numbers

__all__ = ['Boolean', 'Number', 'Float', 'Integer', 'Text', 'URL', 'Date', 'DateTime', 'Time']

Boolean = bool
# Boolean is subclass of Number different from schema.org
Number = numbers.Number
Float = float
Integer = int
Text = str


class URL(Text):

    def __init__(self, *args):
        if not self.is_url(self):
            raise ValueError('not a valid URL')
        super().__init__()

    @staticmethod
    def is_url(x):
        try:
            if 'http://' in x and len(x) > 7:
                return True
            if 'https://' in x and len(x) > 8:
                return True
            return False
        except TypeError:
            return False


class Date(datetime.date):
    """
    Represents ``Date``.
    Adds JSON support to Python Standard Library ``datetime.Date``.

    References:
        https://en.wikipedia.org/wiki/ISO_8601#Dates
    """
    def json_serial(self):
        return self.isoformat()


class Time(datetime.time):
    """
    Represents ``Time``.
    Adds JSON support to Python Standard Library ``datetime.Time``

    References:
        https://en.wikipedia.org/wiki/ISO_8601#Times
    """
    def json_serial(self):
        return self.isoformat()


class DateTime(datetime.datetime, Date):
    """
    Represents ``DateTime``.
    Adds JSON support to Python Standard Library ``datetime.DateTime``

    References:
        https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations
    """
    def __str__(self):
        """
        Returns ISO 8601 format date

        # TODO: make tests
        """
        return super().isoformat()

    def json_serial(self):
        return self.isoformat()

    @classmethod
    def fromisoformat(cls, date_string: str) -> 'DateTime':
        """
        Args:
            date_string: The string to convert to DateTime
        """
        # noinspection PyTypeChecker
        return super().fromisoformat(date_string.replace('Z', '+00:00'))


if __name__ == '__main__':
    import json
    import datatrans.utils

    print(json.dumps(Date(2018, 3, 10), default=datatrans.utils.json_encoder))
    print(json.dumps(Time(0, 20, 0), default=datatrans.utils.json_encoder))
    print(json.dumps(DateTime(2000, 3, 10, 12, 5), default=datatrans.utils.json_encoder))
    pass
