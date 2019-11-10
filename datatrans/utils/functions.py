import re
import string
from typing import Iterable, Match, Optional

NUMERAL = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
}


def snake_to_camel(s: str) -> str:
    """Returns a new str in camelCase, given an str in snake_case.
    Removes all underscore before and after.

    Examples:
        >>> snake_to_camel('snake_to_camel')
        'snakeToCamel'
        >>> snake_to_camel('__snake_to_camel__')
        'snakeToCamel'
        >>> snake_to_camel('snakeToCamel')
        'snakeToCamel'
        >>> snake_to_camel('lonesnake')
        'lonesnake'
    """
    first, *others = [word for word in s.split('_') if word]
    return first + ''.join(s.title() for s in others)


def camel_to_snake(s: str) -> str:
    """Returns a new str in snake_case, given an str in camelCase.

    Raises:
        ValueError: When original str is not in camelCase

    Examples:
        >>> camel_to_snake('camelToSnake')
        'camel_to_snake'
        >>> camel_to_snake('camel_to_snake')
        Traceback (most recent call last):
          ...
        ValueError: original str is not in camelCase: 'camel_to_snake'
        >>> camel_to_snake('lonecamel')
        'lonecamel'
    """
    if '_' in s:
        raise ValueError('original str is not in camelCase: \'{}\''
                         .format(s))
    for u in string.ascii_uppercase:
        s = s.replace(u, '_' + u.lower())
    return s


def to_constant(s: str) -> str:
    """Returns a new str in CONSTANT_CASE, given any str.

    Examples:
        >>> to_constant('to_constant')
        'TO_CONSTANT'
        >>> to_constant('Meals, Entrees, and Side Dishes')
        'MEALS_ENTREES_AND_SIDE_DISHES'
        >>> to_constant('American Indian/Alaska Native Foods')
        'AMERICAN_INDIANALASKA_NATIVE_FOODS'
    """
    s = s.replace(' ', '_')
    s = ''.join(c.upper() for c in s if c in string.ascii_letters or c in '_')
    assert s.isidentifier(), s
    return s


def trim_spaces(s: str) -> str:
    """Trims excess spaces

    Examples:
        >>> trim_spaces(' pretty')
        'pretty'
        >>> trim_spaces(' CHEDDAR CHEESE')
        'CHEDDAR CHEESE'
        >>> trim_spaces(' salt  ')
        'salt'
    """
    return ' '.join(_ for _ in s.split(' ') if _)


def parse_str_unicode(s: str) -> str:
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
    return pattern.sub(unicode_repl, s)


def read_numeral(s: str) -> int:
    """Converts string containing numeral under 13 to `int`.

    Args:
        s (str): positional only. string to parse

    Examples:
        >>> read_numeral('One')
        1
        >>> read_numeral('two')
        2
        >>> read_numeral('three')
        3
        >>> read_numeral('four')
        4
        >>> read_numeral('five')
        5
        >>> read_numeral('six')
        6
        >>> read_numeral('seven ')
        7
        >>> read_numeral('eight')
        8
        >>> read_numeral('nine')
        9
        >>> read_numeral('  ten ')
        10
        >>> read_numeral('ELEVEN')
        11
        >>> read_numeral('twelve')
        12
    """
    try:
        return NUMERAL[''.join(s.lower().split(' '))]
    except KeyError as e:
        raise ValueError('cannot parse \'{}\' as numerals'
                         .format(s)) from e.__context__


def _parse_unicode_vulgar(s: str) -> float:
    if '⅟' in s:
        *number, fraction = s.split('⅟')
        fraction = 1 / float(fraction)
    else:
        *number, fraction = list(s)
        try:
            fraction = {
                '¼': 0.25,
                '½': 0.5,
                '¾': 0.75,
                '⅐': 1 / 7,
                '⅑': 1 / 9,
                '⅓': 1 / 3,
                '⅔': 2 / 3,
                '⅕': 0.2,
                '⅖': 0.4,
                '⅗': 0.6,
                '⅘': 0.8,
                '⅙': 1 / 6,
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
                             .format(s, fraction)) from e.__context__
    number = float(''.join(number)) if number else 0
    return number + fraction


def parse_vulgar_fractions(s: str) -> float:
    """Converts ``string`` containing vulgar fractions to ``float``.

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
        >>> parse_vulgar_fractions('1/2')
        0.5
    """
    if not isinstance(s, str):
        raise TypeError('invalid argument of type \'{}\''.format(s.__class__.__name__))
    if '/' in s:
        try:
            numerator, denominator = s.split('/')
            return float(numerator) / float(denominator)
        except ValueError:
            pass
    return _parse_unicode_vulgar(s)


def get_closest_match(s: str, subs: Iterable[str]) -> Optional[str]:
    """

    Examples:
        >>> get_closest_match('¾ cup (1½ sticks) cold unsalted butter, cut into ¼-inch pieces',
        ... ['unsalted butter', 'all-purpose flour', 'sugar', 'salt', 'water'])
        'unsalted butter'
        >>> get_closest_match('¾ cup (1½ sticks) cold unsalted butter, cut into ¼-inch pieces',
        ... ['unsalted butter', 'salted butter', 'butter', 'sugar', 'salt', 'water'])
        'unsalted butter'
        >>> get_closest_match('¾ cup (1½ sticks) cold unsalted butter, cut into ¼-inch pieces',
        ... ['salted butter', 'butter', 'sugar', 'salt', 'water'])
        'butter'
        >>> get_closest_match('¾ cup (1½ sticks) cold unsalted butter, cut into ¼-inch pieces',
        ... ['butter', 'sugar', 'salt', 'water'])
        'butter'
        >>> get_closest_match('¾ cup (1½ sticks) cold unsalted butter, cut into ¼-inch pieces',
        ... ['sugar', 'salt', 'water'])
    """
    import difflib
    matches = []
    for sub in subs:
        if sub in s:
            matches.append(sub)
    if matches:
        return difflib.get_close_matches(s, matches, cutoff=0)[0]
    try:
        return difflib.get_close_matches(s, subs)[0]
    except IndexError:
        return


def json_encoder(o):
    """
    Add JSON serialization capabilities to objects in this library.
    """
    if hasattr(o, 'json_serial'):
        return o.json_serial()
    else:
        raise TypeError(f'Object of type {o.__class__.__name__} '
                        f'is not JSON serializable')


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
