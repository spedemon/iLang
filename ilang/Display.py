
# ilang - Inference Language 
# Stefano Pedemonte
# Oct. 2013, Alessandria, Italy


from exceptions import UnexpectedParameterType, ParameterError
from verbose import print_important, print_runtime, print_debug

class MatplotlibDisplay():
    def __init__(self,tracer=None): 
        self.tracer = tracer 
        
    def attach_to_tracer(self,tracer): 
        self.tracer = tracer
        
    def imagesc(self,variable,sample_idex=None): 
        pass 
        
