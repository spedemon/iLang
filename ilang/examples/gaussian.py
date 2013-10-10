
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


from ilang.Graphs import Dependence, ProbabilisticGraphicalModel
from ilang.Models import MultivariateGaussian 
from ilang.Samplers import Sampler
from ilang.Tracers import RamTracer
from ilang.Display import MatplotlibDisplay
import numpy




# Define the model 
ndim = 10
model = MultivariateGaussian('gaussian') 

# Build the graph 
dag = ProbabilisticGraphicalModel(['x','mu','cov']) 
dag.set_nodes_given(['mu','cov'], True) 
dag.add_dependence(model,{'x':'x','mu':'mu','cov':'cov'}) 

# Initialize the nodes of the graph
dag.set_node_value('x',numpy.ones((1,ndim))) 
dag.set_node_value('mu',numpy.zeros((1,ndim)))
dag.set_node_value('cov',numpy.eye(ndim)) 

# Initialise sampler, tracer, display 
sampler = Sampler(dag) 
tracer = RamTracer(sampler)   
display = MatplotlibDisplay(tracer) 

# Sample 
sampler.sample(1000,trace=False) 
#display.plot('mu') 
#display.plot('sigma') 


if __name__=="__main__": 
    dag.webdisplay(background=False) 


