
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


from ilang.Graphs import Dependence, ProbabilisticGraphicalModel
from ilang.Samplers import AutoSampler
from ilang.Tracers import RamTracer
from ilang.Display import MatplotlibDisplay
import numpy

# Define the model: 

class Gaussian(Dependence): 
    def init(self): 
        pass 

    def variables(self): 
        return {'x':'continuous','mu':'continuous','cov':'continuous'} 

    def dependencies(self): 
        return [['mu','x','directed'],['cov','x','directed']] 

    def log_conditional_probability_x(self): 
        return 0 

    def log_conditional_probability_gradient_x(self): 
        return numpy.zeros([100,1])

    def log_conditional_probability_mu(self): 
        return 0 

    def log_conditional_probability_gradient_mu(self): 
        return numpy.zeros([100,1])
        
    def sample_conditional_probability_sigma(self): 
        return 0


# Define the probabilistic graphical model: 


if __name__ == "__main__": 
    # Define the model 
    model = Gaussian('Gaussian')
    dag = ProbabilisticGraphicalModel(['x','mu','cov']) 
    dag.set_nodes_given(['mu','cov'], True) 
    dag.add_dependence(model,{'x':'x','mu':'mu','cov':'cov'}) 
    dag.webdisplay(background=True) 

    # Initialise sampler
    dag.set_node_value('x',numpy.ones((1,ndim))) 
    dag.set_node_value('mu',numpy.zeros(1,ndim))
    dag.set_node_value('cov',numpy.eye(numpy.ones(1,ndim)))  
    sampler = AutoSampler(dag) 
    tracer = RamTracer(sampler)   
    display = MatplotlibDisplay(sampler) 
    
    # Sample 
    sampler.sample(1000,trace=False) 
#    display.plot('mu') 
#    display.plot('sigma') 
    
    import time; time.sleep(5) 