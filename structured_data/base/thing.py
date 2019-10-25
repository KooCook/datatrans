class Thing:
    def get_type_specification(self) -> str:
        return '"@type":"{}"'.format(self.__class__.__name__)

    @staticmethod
    def get_context() -> str:
        return '"@context":"https://schema.org"'
