class CreateNodeException(Exception):
    errors: list[str]

    def __init__(self, errors: list[str], *args):
        super().__init__(*args)
        self.errors = errors
