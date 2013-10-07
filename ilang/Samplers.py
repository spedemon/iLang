
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


from exceptions import UnexpectedParameterType, ParameterError
from verbose import print_important, print_runtime, print_debug


class AutoSampler():
    def __init__(self,graph=None): 
        self.graph = graph 
        
    def sample(self,n_samples, trace=True): 
        pass 
        
    def attach_to_graph(self,graph): 
        self.graph = graph 
    
        
