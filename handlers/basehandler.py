
class BaseHandler:
    """Handler to be extended so it can be caught in the main function"""

    @staticmethod
    def has_description():
        return True

    @staticmethod
    def build_handler():
        raise NotImplementedError

    @staticmethod
    def command_name():
        raise NotImplementedError

    @staticmethod
    def command_description():
        raise NotImplementedError
        