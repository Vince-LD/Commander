# Should create an exception by ExpectedResult class

class UnexpectedResultError(ValueError):
    """Generic exception to signal an unexpected result"""


class CommandNotExecuted(ValueError):
    """Error used to signal that the command was not executed which is required to call
    certain methods"""
