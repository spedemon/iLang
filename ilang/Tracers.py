
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


from exceptions import UnexpectedParameterType, ParameterError
from verbose import print_important, print_runtime, print_debug

class RamTracer():
    def __init__(self,sampler=None): 
        self.sampler = sampler 
        
    def attach_to_sampler(self,sampler): 
        self.sampler = sampler 
        

