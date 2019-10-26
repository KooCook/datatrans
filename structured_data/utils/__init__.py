
def has_context(json_ld: str) -> bool:
    """
    Returns True if '"@context" is in ``json-ld`` and False otherwise.
    """
    return '"@context"' in json_ld


def with_context(json_ld: str, context='https://schema.org/') -> str:
    if json_ld[0] != '{':
        raise ValueError('json-ld is invalid')
    if json_ld[-1] != '}':
        raise ValueError('json-ld is invalid')
    if has_context(json_ld):
        raise ValueError('json-ld already has context')
    if json_ld[1] != '"':
        raise AssertionError('Don\'t use with un-minified json-ld')
    if '"@type"' not in json_ld:
        import warnings
        warnings.warn('adding context to json-ld without "@type"')
    return '{"@context":"{}"'.format(context) + json_ld[0:]


def default(o):
    """
    Add JSON serialization capabilities to objects in this library.
    """
    if hasattr(o, 'json_serial'):
        return o.json_serial()
    else:
        raise TypeError(f'Object of type {o.__class__.__name__} '
                        f'is not JSON serializable')


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
