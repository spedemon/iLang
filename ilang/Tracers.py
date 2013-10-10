
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


__all__ = ['Tracer']

from ilang.Samplers import *
from ilang.Graphs import * 
from ilang.exceptions import *
from ilang.verbose import * 


class Tracer(object):
    def __init__(self,sampler=None):
        self.sampler = None 
        if sampler!=None: 
            self.attach_to_sampler(sampler)

    def has_sampler(self): 
        return isinstance(self.sampler,Sampler)
      
    def get_sampler(self): 
        if not self.has_sampler(): 
            raise NotInitialized("The tracer is not attached to a sampler. ")
        return self.sampler
 
    def attach_to_sampler(self,sampler): 
        if not isinstance(sampler,Sampler): 
            raise UnexpectedParameterType("sampler must be an instance of Sampler. ")
        self.sampler = sampler
        


class RamTracer(Tracer):
    def __init__(self, *args, **kwds):
        super(RamTracer, self).__init__(*args, **kwds)       
    pass
