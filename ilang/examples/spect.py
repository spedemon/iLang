
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


from ilang.Graphs import Dependence, ProbabilisticGraphicalModel
from ilang.exceptions import *

# Define the observation model: 

class DependenceSpectPoisson(Dependence): 
    def init(self): 
        pass 

    def name(self):
        return "SPECT-Poisson"

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


class DependenceSmoothing(Dependence): 
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


# Define the graphical model: 

def define_graph(): 
    observation = DependenceSpectPoisson('SPECT-Poisson')
    prior = DependenceSmoothing('Smoothing_Activity')
    dag = ProbabilisticGraphicalModel(['activity','attenuation','counts','beta']) 
    dag.attach_dependence(observation,{'lambda':'activity','alpha':'attenuation','z':'counts'})
    dag.attach_dependence(prior,{'x':'lambda','beta':'beta'}) 
    return dag 
    
if __name__ == "__main__":
    dag = define_graph() 
    dag.webdisplay(background=False)

 

