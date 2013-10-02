
from core import *
from scanners import SPECT, GE_Infinia


class BaseModel(): 
    def __init__(self): 
          pass 


class Model_SPECT(BaseModel): 
    def __init__(self,scanner=None): 
        BaseModel.__init__(self)
        if scanner == None:
            self.scanner=SPECT() 
        else: 
            if not isinstance(scanner,SPECT): 
                raise BadParameter("scanner must be an instance of SPECT")
            self.scanner=scanner 

    def set_node_activity(self,activity):
        pass 

    def set_node_counts(self,counts):
        pass 



class Model_PET(BaseModel): 
    def __init__(self): 
        BaseModel.__init__(self)


class Model_XRay_CT(BaseModel): 
    def __init__(self): 
        BaseModel.__init__(self)

class Model_SPECT_Dynamic(BaseModel): 
    def __init__(self): 
        BaseModel.__init__(self)

class Model_SPECT_Dynamic(BaseModel): 
    def __init__(self): 
        BaseModel.__init__(self)



class Model_MRF(BaseModel): 
    def __init__(self): 
        BaseModel.__init__(self)




class DAG():
    def __init__(self,variables_names=[]):  
        self.add_variables(variables_names) 
 
    def add_variable(self,variable_name):
        if not isinstance(variable_name,type('')): 
            raise BadParameter("Variable name must be a string. ")
        print_low_verbose("Adding variable "+variable_name+" to DAG.")
        pass

    def add_variables(self,variables_names): 
        if not isinstance(variables_names,type([])): 
            raise BadParameter("Parameter must be a list. See also 'add_variable()'.")
        for var in variables_names: 
            self.add_variable(var)


