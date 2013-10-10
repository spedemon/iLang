
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


from ilang.Graphs import Dependence 
from ilang.exceptions import *
from ilang.verbose import *  



class Model(Dependence,object): 
    def __init__(self, *args, **kwds):
        super(Model, self).__init__(*args, **kwds)       
    pass



class MultivariateGaussian(Model): 
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



class Poisson(Model): 
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



class Smoothness(Model): 
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


