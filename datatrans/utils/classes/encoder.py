import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'json_serial'):
            return o.json_serial()
        else:
            raise TypeError(f'Object of type {o.__class__.__name__} '
                            f'is not JSON serializable')
