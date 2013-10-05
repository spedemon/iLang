
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


# Exceptions 
class UnexpectedParameterType(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr("Unexpected parameter type: "+str(self.value))
        
class ParameterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr("Parameter error: "+str(self.value))

class InconsistentGraph(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr("Parameter error: "+str(self.value))        