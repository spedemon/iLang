
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


from ilang.Graphs import Dependence, ProbabilisticGraphicalModel
from ilang.Samplers import AutoSampler
from ilang.Tracers import RamTracer
from ilang.Display import MatplotlibDisplay


# Define the observation model: 

class SpectPoisson(Dependence): 
    def init(self): 
        pass 

    def variables(self): 
        return {'lambda':'continuous','alpha':'continuous','z':'discrete'} 

    def dependencies(self): 
        return [['lambda','z','directed'],['alpha','z','directed']]

    def log_conditional_probability_lambda(self): 
        return 0 

    def log_conditional_probability_gradient_lambda(self): 
        return numpy.zeros([100,1])

    def log_conditional_probability_alpha(self): 
        return 0 

    def log_conditional_probability_gradient_alpha(self): 
        return numpy.zeros([100,1])
        
    def sample_conditional_probability_counts(self): 
        return 0


# Define the prior models

class Smoothing(Dependence): 
    def init(self): 
        pass

    def variables(self): 
        return {'x':'continuous','beta':'continuous'}
        
    def dependencies(self): 
        return [['beta','x','directed']] 

    def log_conditional_probability_x(self): 
        return 0

    def log_conditional_probability_gradient_x(self): 
        return 0

    def log_conditional_probability_beta(self): 
        return 0

    def log_conditional_probability_gradient_beta(self): 
        return 0



# Define the probabilistic graphical model: 

def define_graph(): 
    observation = SpectPoisson('SPECT-Poisson')
    prior_activity = Smoothing('Smoothing_Activity') 
    prior_attenuation = Smoothing('Smoothing_Attenuation')  
    dag = ProbabilisticGraphicalModel(['activity','attenuation','counts','smoothing-activity','smoothing-attenuation']) 
    dag.set_nodes_given(['counts','smoothing-activity','smoothing-attenuation'], True)
    dag.add_dependence(observation,{'lambda':'activity','alpha':'attenuation','z':'counts'})
    dag.add_dependence(prior_activity,{'x':'activity','beta':'smoothing-activity'}) 
    dag.add_dependence(prior_attenuation,{'x':'attenuation','beta':'smoothing-attenuation'}) 
    return dag 


if __name__ == "__main__": 
    dag = define_graph() 
    dag.webdisplay(background=False) 
    
    sampler = AutoSampler(dag)
    tracer = RamTracer(sampler)  
    display = MatplotlibDisplay(sampler) 
    
    sampler.sample(1000,trace=False) 
    display.imagesc('activity')
     
