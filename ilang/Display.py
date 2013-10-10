
# ilang - Inference Language 
# Stefano Pedemonte
# Oct. 2013, Alessandria, Italy



__all__ = ['MatplotlibDisplay'] 

from ilang.Tracers import *
from ilang.Samplers import *
from ilang.Graphs import * 
from ilang.exceptions import *
from ilang.verbose import * 


class Display(object):
    def __init__(self,tracer=None):
        self.tracer = None 
        if tracer!=None: 
            self.attach_to_tracer(tracer)

    def has_tracer(self): 
        return isinstance(self.tracer,Tracer)
      
    def get_tracer(self): 
        if not self.has_tracer(): 
            raise NotInitialized("display is not attached to a tracer. ")
        return self.tracer 
 
    def attach_to_tracer(self,tracer): 
        if not isinstance(tracer,Tracer):
            raise UnexpectedParameterType("tracer must be an instance of Tracer. ")
        self.tracer = tracer



class MatplotlibDisplay(Display): 
    def __init__(self, *args, **kwds):
        super(MatplotlibDisplay, self).__init__(*args, **kwds) 

    def imagesc_node(self,node,sample_index=None): 
        if not self.tracer.get_sampler().get_graph().has_node(node):  
            raise ParameterError("The graph does not have node '%s'."%str(node)) 
    