class IdMixin:
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
