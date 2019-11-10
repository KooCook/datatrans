import enum

__all__ = ['JSONEnum']


class JSONEnum(enum.Enum):
    """ JSON serializable enum (with default=utils.json_encoder). """
    def json_serial(self):
        return self.value
