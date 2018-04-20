class NixError(BaseException):
    def __init__(self, failure_type, message):
        self.failure_type = failure_type
        self.message = message

        super(BaseException, self).__init__()
