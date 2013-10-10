
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


from ilang.Graphs import Dependence, ProbabilisticGraphicalModel
from ilang.Models import Poisson, Smoothness 
from ilang.Samplers import Sampler
from ilang.Tracers import RamTracer
from ilang.Display import MatplotlibDisplay
import numpy



# Define the model components 
observation = Poisson('SPECT')
prior_activity = Smoothness('Smoothing_Activity') 
prior_attenuation = Smoothness('Smoothing_Attenuation')  

# Build the graph 
dag = ProbabilisticGraphicalModel(['activity','attenuation','counts','smoothing-activity','smoothing-attenuation']) 
dag.set_nodes_given(['counts','smoothing-activity','smoothing-attenuation'], True)
dag.add_dependence(observation,{'lambda':'activity','alpha':'attenuation','z':'counts'})
dag.add_dependence(prior_activity,{'x':'activity','beta':'smoothing-activity'}) 
dag.add_dependence(prior_attenuation,{'x':'attenuation','beta':'smoothing-attenuation'}) 

# Initialize the nodes of the graph   
dag.set_node_value('activity',numpy.ones((10,10)))

# Instantiate the sampler, tracer and display 
sampler = Sampler(dag)
tracer = RamTracer(sampler)  
display = MatplotlibDisplay(tracer) 

# Sample 
sampler.sample(1000,trace=False) 
display.imagesc_node('activity')



if __name__=="__main__": 
    dag.webdisplay(background=False) 


