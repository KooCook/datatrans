__all__ = ['json_encoder']

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

    doctest.testmod()
