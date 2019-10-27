from pathlib import Path

BASE_DIR = Path(__file__).parent


def snake_to_camel(string: str) -> str:
    """
    Returns a new str in camelCase, given an str in snake case.
    Removes all underscore before and after.

    >>> snake_to_camel('snake_to_camel')
    'snakeToCamel'
    >>> snake_to_camel('__snake_to_camel__')
    'snakeToCamel'
    """
    first, *others = [word for word in string.split('_') if word]
    return first + ''.join(s.title() for s in others)