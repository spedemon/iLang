
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


__all__ = ['Sampler'] 

from ilang.Graphs import Node,ProbabilisticGraphicalModel,name
from ilang.exceptions import *
from ilang.verbose import * 
import numpy
import inspect, sys




# Sampling strategies 
class SamplingStrategy(object): 
    def __init__(self,graph): 
        self.graph = graph 

    def next_node(self): 
        pass 

        
class RandomNodesStrategy(SamplingStrategy): 
    def __init__(self, *args, **kwds):
        super(RandomNodesStrategy, self).__init__(*args, **kwds)       

    def next_node(self): 
        nodes = self.graph.get_nodes()
        index = numpy.random.randint(len(nodes)) 
        return nodes[index]





# Sampling methods
class SamplingMethod(object): 
    def __init__(self): 
        self._requires_log_probability = False
        self._requires_log_probability_gradient = False
        self._requires_log_probability_hessian = False
        self._requires_log_probability_diagonal_hessian = False
        self._requires_own_sampler = False 
        self._is_optimizer = True 

    def requires_log_probability(self): 
        return self._requires_log_probability 
        
    def requires_log_probability_gradient(self): 
        return self._requires_log_probability_gradient 
        
    def requires_log_probability_hessian(self): 
        return self._requires_log_probability_hessian 
        
    def requires_log_probability_diagonal_hessian(self): 
        return self._requires_log_probability_diagonal_hessian 

    def requires_own_sampler(self): 
        return self._requires_own_sampler 
        
    def can_be_used_with_node(self,node): 
        if self.requires_own_sampler(): 
            if not node.can_sample_conditional_probability(): 
                return False 
        if not isinstance(node,Node): 
            raise UnexpectedParameterType("node must be an instance of Node.") 
        if self.requires_log_probability(): 
            if not node.has_log_conditional_probability(): 
                return False
        if self.requires_log_probability_gradient(): 
            if not node.has_log_conditional_probability_gradient(): 
                return False 
        if self.requires_log_probability_hessian(): 
            if not node.has_log_conditional_probability_hessian(): 
                return False   
        if self.requires_log_probability_diagonal_hessian(): 
            if not node.has_log_conditional_probability_diagonal_hessian(): 
                return False    
        return True

    def get_name(self): 
        if hasattr(self,"__name__"): 
            return self.__name__
        elif hasattr(self,"__class__"): 
            return self.__class__.__name__ 
        else: 
            raise Exception("This should never ever happen. ") 

    def is_optimizer(self): 
        return self._is_optimizer 

    # Subclass:
    def sample(self,node,parameters): 
        return None

    def default_parameters(self): 
        return {}


class DirectSampling(SamplingMethod): 
    def __init__(self, *args, **kwds):
        super(DirectSampling, self).__init__(*args, **kwds) 
        self._requires_own_sampler = True

    def sample(self,graph,node,parameters): 
        return graph.sample_conditional_probability_node(node)

    def default_parameters(self): 
        return {}
        
class MetropolisHastingsMCMC(SamplingMethod): 
    def __init__(self, *args, **kwds):
        super(MetropolisHastingsMCMC, self).__init__(*args, **kwds) 
        self._requires_log_probability = True

    def sample(self,graph,node,parameters): 
        return graph.get_node_value(node)

    def default_parameters(self): 
        return {'step_size':0.1}
        
class GradientDescent(SamplingMethod): 
    def __init__(self, *args, **kwds):
        super(GradientDescent, self).__init__(*args, **kwds) 
        self._requires_log_probability = True
        self._requires_log_probability_gradient = True
        self._is_optimizer = True

    def sample(self,graph,node,parameters): 
        return graph.get_node_value(node)

    def default_parameters(self): 
        return {'step_size':0.1}
        
class ExpectationMaximization(SamplingMethod): 
    def __init__(self, *args, **kwds):
        super(ExpectationMaximization, self).__init__(*args, **kwds) 
        self._requires_log_probability = True
        self._requires_log_probability_gradient = True
        self._is_optimizer = True

    def sample(self,graph,node,parameters): 
        return graph.get_node_value(node)

    def default_parameters(self): 
        return {'step_size':0.1}

class LBFGS_L(SamplingMethod): 
    def __init__(self, *args, **kwds):
        super(ExpectationMaximization, self).__init__(*args, **kwds) 
        self._requires_log_probability = True
        self._requires_log_probability_gradient = True
        self._is_optimizer = True

    def sample(self,graph,node,parameters): 
        return graph.get_node_value(node)

    def default_parameters(self): 
        return {'step_size':0.1}

class HamiltonianMCMC(SamplingMethod): 
    def __init__(self, *args, **kwds):
        super(HamiltonianMCMC, self).__init__(*args, **kwds) 
        self._requires_log_probability = True
        self._requires_log_probability_gradient = True
        self._requires_log_probability_hessian = True

    def sample(self,graph,node,parameters): 
        return graph.get_node_value(node)

    def default_parameters(self): 
        return {'step_size':0.1}

class LangevinAdjustedMetropolisHastingsMCMC(SamplingMethod): 
    def __init__(self, *args, **kwds):
        super(LangevinAdjustedMetropolisHastingsMCMC, self).__init__(*args, **kwds) 
        self._requires_log_probability = True
        self._requires_log_probability_gradient = True
        self._requires_log_probability_hessian = True

    def sample(self,graph,node,parameters): 
        return graph.get_node_value(node)

    def default_parameters(self): 
        return {'step_size':0.1}
        



def best_sampling_method(graph,node,sampling_methods): 
    """Select the best sampling method out of a list of sampling methods. """
    # FIXME: implement - use the preference expressed by the node and the properties of the node (gradient, ..) and of the sampling methods. 
    return sampling_methods[0]

        
# Sampler 
class Sampler(object):
    def __init__(self,graph=None,optimization_only=False): 
        self.nodes_compatible_sampling_methods = {}
        self.nodes_active_sampling_method = {}
        self.nodes_sampling_parameters = {}
        self.sampling_methods = [] 
        self._load_sampling_methods() 
        self.graph = None
        if graph!=None: 
            self.attach_to_graph(graph,optimization_only) 
            
    def has_graph(self): 
        return isinstance(self.graph,ProbabilisticGraphicalModel) 

    def get_graph(self): 
        if not self.has_graph(): 
            raise NotInitialized("The sampler is not attached to a graph. ")
        return self.graph 
 
    def attach_to_graph(self,graph,optimization_only=False): 
        if not isinstance(graph,ProbabilisticGraphicalModel):
            raise UnexpectedParameterType("graph must be an instance of ProbabilisticGraphicalModel. ") 
        self.graph = graph 
        # for each node, determine which sampling methods can be used  
        for node in self.graph.get_nodes(): 
            sampling_methods = []
            for sampling_method in self.get_sampling_methods(): 
                if sampling_method.can_be_used_with_node(node): 
                    if not optimization_only: 
                        sampling_methods.append(sampling_method) 
                    else: 
                        if sampling_method.is_optimizer(): 
                            sampling_methods.append(sampling_method) 
            self.nodes_compatible_sampling_methods[name(node)] = sampling_methods
            if sampling_methods == []: 
                print_important('None of the sampling methods is able to sample from node %s.'%str(node.name) ) 
        # by default set the sampling method automatically for all nodes
        self.set_sampling_method_auto(optimization_only) 

    def set_node_sampling_method_auto(self,node,optimization_only=False):  
        if not self.get_graph().has_node(node): 
            raise ParameterError("The graph does not contain node '%s'."%name(node)) 
        # filter the methods if only optimization is requested
        if optimization_only: 
            sampling_methods = []
            for sampling_method in self.nodes_compatible_sampling_methods[name(node)]: 
                if sampling_method.is_optimization(): 
                    sampling_mehtods.append(sampling_methods)
        else: 
            sampling_methods = self.nodes_compatible_sampling_methods[name(node)]
        print_debug("The samplers compatible with are: %s"%str(self.nodes_compatible_sampling_methods[name(node)]))
        # choose the best sampler 
        self.nodes_active_sampling_method[name(node)] = best_sampling_method(graph,node,sampling_methods)  
        # use the default parameters for the sampling method 
        self.nodes_sampling_parameters[name(node)] = self.nodes_active_sampling_method[name(node)].default_parameters()
        print_runtime("Selected sampling method '%s' for node '%s'. "%( name(self.nodes_active_sampling_method[name(node)]),name(node)) )
        return self.nodes_active_sampling_method[name(node)] 

    def set_sampling_method_auto(self,optimization_only=False): 
        for node in self.get_graph().get_nodes(): 
            self.set_node_sampling_method_auto(node,optimization_only) 

    def set_node_sampling_method_manual(self,node,sampling_method_name,parameters=None): 
        if not self.get_graph().has_node(node): 
            raise ParameterError("The graph does not contain node '%s'."%name(node)) 
        if not sampling_method in self.nodes_compatible_sampling_methods[name(node)]: 
            raise ParameterError("Sampling method '%s' is not compatible with node '%s'."%(name(sampling_method),name(node)))
        self.nodes_active_sampling_method[name(node)] = sampling_method #FIXME: use name all the time 
        if parameters != None: 
            parameters = self.nodes_active_sampling_method[name(node)].default_parameters()
        self.nodes_sampling_parameters[name(node)] = parameters 

    def sample_node(self, node, nsamples, parameters=None, trace=True): 
        node = name(node) 
        if not self.get_graph().has_node(node): 
            raise ParameterError("The graph does not contain node '%s'."%node) 
        if not self.nodes_active_sampling_method.has_key(node): 
            raise NotInitialized("The sampling strategy for node '%s' has not beel selected. "%node) 
        active_sampling_method = self.nodes_active_sampling_method[node] 
        for i in range(nsamples): 
            sample = active_sampling_method.sample(self.graph,node,parameters) 
        if trace: 
            pass     
        return sample 

    def sample(self,nsamples,trace=True): 
        pass 

    def set_sampling_strategy(self,sampling_strategy): 
        if not isinstance(sampling_strategy,SamplingStrategy): 
            raise UnexpectedParameterType("sampling_strategy must be an instance of SamplingStrategy. ")
        self.sampling_strategy = sampling_strategy 
        
    def get_sampling_methods(self): 
        return self.sampling_methods

    def _load_sampling_methods(self): 
        self.sampling_methods = []   
        for name,obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
           if issubclass(obj,SamplingMethod): 
               if not 'SamplingMethod' in str(obj): 
                   self.sampling_methods.append(obj()) 

