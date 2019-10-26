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
    """
    Represents ``Date``.
    Adds JSON support to Python Standard Library ``datetime.Date``.

    https://en.wikipedia.org/wiki/ISO_8601#Dates
    """
    def json_serial(self):
        return self.isoformat()


class Time(_datetime.time):
    """
    Represents ``Time``.
    Adds JSON support to Python Standard Library ``datetime.Time``

    https://en.wikipedia.org/wiki/ISO_8601#Times
    """
    def json_serial(self):
        return self.isoformat()


class DateTime(_datetime.datetime):
    """
    Represents ``DateTime``.
    Adds JSON support to Python Standard Library ``datetime.DateTime``

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


if __name__ == '__main__':
    pass
