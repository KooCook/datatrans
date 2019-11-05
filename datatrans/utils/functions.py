from typing import Match

from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent.parent


def snake_to_camel(string: str) -> str:
    """Returns a new str in camelCase, given an str in snake case.
    Removes all underscore before and after.

    Examples:
        >>> snake_to_camel('snake_to_camel')
        'snakeToCamel'
        >>> snake_to_camel('__snake_to_camel__')
        'snakeToCamel'
        >>> snake_to_camel('snakeToCamel')
        'snakeToCamel'
    """
    first, *others = [word for word in string.split('_') if word]
    return first + ''.join(s.title() for s in others)


def trim_spaces(string: str) -> str:
    """Trims excess spaces

    Examples:
        >>> trim_spaces(' pretty')
        'pretty'
        >>> trim_spaces(' CHEDDAR CHEESE')
        'CHEDDAR CHEESE'
        >>> trim_spaces(' salt  ')
        'salt'
    """
    return ' '.join(_ for _ in string.split(' ') if _)


def parse_str_unicode(string: str) -> str:
    """Returns `string` with literal unicode replaced with actual unicode.

    Examples:
        >>> parse_str_unicode('\\u00be cup (1\\u00bd sticks) cold unsalted butter, cut into \\u00bc-inch pieces')
        '¾ cup (1½ sticks) cold unsalted butter, cut into ¼-inch pieces'
        >>> parse_str_unicode('¾ cup (1½ sticks) cold unsalted butter, cut into ¼-inch pieces')
        '¾ cup (1½ sticks) cold unsalted butter, cut into ¼-inch pieces'
    """
    def unicode_repl(matchobj: Match):
        m = matchobj.group(0)
        return eval("'" + m[2:] + "'")

    pattern = re.compile(r'\\u\d\d\d\d')
    return pattern.sub(unicode_repl, string)


def parse_vulgar_fractions(string: str) -> float:
    """Converts ``str`` containing vulgar fractions to ``float``.

    Raises:
        ValueError: When `string` is invalid
        TypeError: When `string` is not a `str`

    Examples:
        >>> parse_vulgar_fractions('¾')
        0.75
        >>> parse_vulgar_fractions('1½')
        1.5
        >>> parse_vulgar_fractions('¼')
        0.25
        >>> parse_vulgar_fractions('3⅟100')
        3.01
        >>> parse_vulgar_fractions('')
        Traceback (most recent call last):
          ...
        ValueError: ...
        >>> parse_vulgar_fractions('three quarters')
        Traceback (most recent call last):
          ...
        ValueError: ...
        >>> parse_vulgar_fractions(5)
        Traceback (most recent call last):
          ...
        TypeError: ...
    """
    if not isinstance(string, str):
        raise TypeError('invalid argument of type \'{}\''.format(string.__class__.__name__))
    try:
        if '⅟' in string:
            *number, fraction = string.split('⅟')
            fraction = 1 / float(fraction)
        else:
            *number, fraction = list(string)
            try:
                fraction = {
                    '¼': 0.25,
                    '½': 0.5,
                    '¾': 0.75,
                    '⅐': 1/7,
                    '⅑': 1/9,
                    '⅓': 1/3,
                    '⅔': 2/3,
                    '⅕': 0.2,
                    '⅖': 0.4,
                    '⅗': 0.6,
                    '⅘': 0.8,
                    '⅙': 1/6,
                    '⅛': 0.125,
                    '⅜': 0.375,
                    '⅝': 0.625,
                    '⅞': 0.875,
                    '⅟': None,
                    '↉': 0,
                }[fraction]
            except KeyError as e:
                raise ValueError('invalid string \'{}\', '
                                 '\'{}\' is not a vulgar fraction'
                                 .format(string, fraction)) from e.__context__
        number = float(''.join(number)) if number else 0
        return number + fraction
    except ValueError as e:
        raise


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
