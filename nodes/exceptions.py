class NodeException(Exception):
    """Base exception class for node-related errors."""

    pass


class NodeValidationException(NodeException):
    def __init__(self, type: str, message: str, parameters: dict = {}, *args):
        super().__init__(*args)
        self.type = type
        self.message = message
        self.parameters = parameters
