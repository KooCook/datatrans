from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
