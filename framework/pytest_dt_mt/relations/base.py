class MetamorphicRelationError(Exception):
    def __init__(self, message, pytrace=False):
        super().__init__(message)
        self.pytrace = pytrace

class MetamorphicRelation:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def evaluate(self, result, dt_adapter=None):
        raise NotImplementedError("Subclasses must implement evaluate()")
