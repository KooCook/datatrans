import datetime as _datetime
import numbers as _numbers

Boolean = bool
# Boolean is subclass of Number different from schema.org
Number = _numbers.Number
Float = float
Integer = int
Text = str


class URL(Text):

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


class Date(_datetime.date):
    pass


class Time(_datetime.time):
    pass


class DateTime(_datetime.datetime):
    """
    https://en.wikipedia.org/wiki/ISO_8601#Dates
    """

    def __str__(self):
        """
        Returns ISO 8601 format date

        # TODO: make tests
        """
        return super().isoformat()
