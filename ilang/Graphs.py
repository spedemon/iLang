
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 


__all__ = ['Node','Dependence','ProbabilisticGraphicalModel']

from exceptions import UnexpectedParameterType, ParameterError
from verbose import print_important, print_runtime, print_debug
import numpy
        
data_types = ['continuous','discrete']

def set_data_type(self,node,data_type): 
    if data_type in data_types: 
        node.data_type = data_type
    else: 
        raise ParameterError("Unknown data_type %s. Known data types are %s."%(str(data_type),data_types)) 





class NodeContainer(): 
    """Represents the node of a Dependence. It contains the information relative to a node, 
    necessary in order to define the Dependence. The NodeContainer is then attached to a 
    Node when the Dependence is associated to a ProbabilisticGraphicalModel. """
    
    def __init__(self, name): 
        self.name = name 
        self.parents = [] 
        self.children = [] 
        self.neighbours = [] 
        self.attached_node = None
        self.data_type = None

    def get_attached_node(self): 
        """Returns the name of the Node attached to the node container 
        (this can be None or a Node instance). """
        return self.attached_node 
    
    def get_name(self): 
        """Returns the name of the node container. This is defined in the Dependence object 
        of which the node container is part. (see Dependence - expecially the method 
        variables() ). """
        return self.name
    
    def has_attached_node(self): 
        """Returns True if there is a node in the node container. This can be True only if 
        the Dependence object of which the node container is part is attached to a 
        ProbabilisticGraphicalModel. """
        return isinstance(self.attached_node, Node)

    def set_data_type(self,data_type): 
        """Sets the data type associated to the node container. """
        set_data_type(self,data_type) 
        return True

    def attach_to_node(self,node): 
        """Attaches the node container to a node. This method is called by the Dependence object. 
        If the data types associated to the node and to the node container differ then if the data 
        type of one of the two is not defined, the data type is passed along. If the data types are 
        defined and discordant, the attachment fails. """
        # verify if the node and the container represent the same data type
        # if the data type of one of the two is not defined, share. 
        if not isinstance(node, Node): 
            raise UnexpectedParameterType("Expected an instance of Node") 
        if node.data_type == self.data_type: 
            self.__attach_to_node(node) 
        elif node.data_type == None: 
            node.set_data_type(self.data_type)
            self.__attach_to_node(node) 
        elif self.data_type == None: 
            self.set_data_type(node.data_type)
            self.__attach_to_node(node) 
        else:
            raise InconsistentGraph("Data type mismatch: node %s and node container %s have different data types (%s and %s). "%(repr(node),repr(self),node.data_type,self.data_type) )
        return True

    def __attach_to_node(self,node): 
        if self.has_attached_node(): 
            print_important("Detaching node container from node %s and attaching to node %s. "%(repr(self.attached_node),repr(node)) )
        self.attached_node = node

    def detach_from_node(self): 
        """Detaches the node container from the attached node. This method is called by the Dependence object. """
        self.attached_node = None




class Dependence(): 
    def __init__(self,name): 
        self.nodes_containers = []  
        self._make_nodes_containers() 
        self.init() 
        self.name = name
    
    def _make_nodes_containers(self): 
        """Instantiate a node container for each variable. """
        for variable_name in self.get_variables_names(): 
            nodeph = NodeContainer(variable_name) 
            self.nodes_containers.append(nodeph)

    def init(self): 
        """Subclass this method to define a new dependence. This method is called right 
        after the instantiation of the Dependence object, enabling the insertion of 
        initialization code. """
        return True 
        
    def dependencies(self): 
        """Subclass this method to define a new dependence. This method must return a 
        dictionary describing the dependencies between variables. """
        return [] 
        
    def variables(self): 
        """Subclass this method to define a new dependence. This method must return a 
        dictionary of the variables involved in the dependence object. """
        return {} 

    def attach_to_nodes(self,links): 
        """Attach the dependence object to the nodes of a ProbabilisticGraphicalModel. """
        for variable_name in links.keys(): 
            if not self.has_variable_named(variable_name): 
                raise ParameterError("Dependence does not have a variable with name %s. (The variables are %s). "%(variable_name,self.get_variables_names()))
            if not isinstance(links[variable_name], Node): 
                raise UnexpectedParameterType("Expected an instance of Node. ")
        for variable_name in links.keys(): 
            container = self.get_node_container(variable_name)
            container.attach_to_node(links[variable_name]) 

    def is_fully_attached(self): 
        """Returns True if all the variables are attached to the nodes of a graph. """
        pass 
        
    def get_nodes_containers(self): 
        """Returns a list of all the nodes containers. """
        return self.nodes_containers
      
    def get_node_container(self,variable_name): 
        """Returns the node container corresponding to the variable with the given name. """
        if not self.has_variable_named(variable_name): 
            raise InconsistentGraph("The requested variable (%s) does not exist. The variables are %s."%(variable_name,self.get_variables_names())) 
        for nodeph in self.get_nodes_containers(): 
            if nodeph.name == variable_name: 
                return nodeph  
         
    def get_node_from_variable_name(self,variable_name): 
        """Returns the node attached to the given variable. """
        if not self.has_variable_named(variable_name): 
            raise ParameterError("The requested variable (%s) does not exist. The variables are %s."%(variable_name,self.get_variables_names()))
        node_container = self.get_node_container(variable_name)
        if not node_container.has_attached_node(): 
            raise ParameterError("Variable %s is not attached to a node. "%variable_name)
        return node_container.get_attached_node() 
        
    def get_variable_name_from_node(self,node): 
        """Returns the name of the node container attached to the given node. """
        for container in self.get_nodes_containers(): 
            if isinstance(node,Node): 
                if container.get_attached_node() == node: 
                    return container.get_name() 
            elif isinstance(node,'str'): 
                if container.get_attached_node().name == node: 
                    return container.get_name() 
        raise ParameterError("Node %s is not attached to any of the node containers. "%str(node)) 
        
    def has_variable_named(self,variable_name): 
        """Returns True if one of the variables of the dependence object has the given name. """
        return variable_name in self.variables().keys()
        
    def get_variables_names(self): 
        """Returns a list of the names of all the variables. """
        return self.variables().keys()

    def get_attached_nodes(self): 
        """Returns a list of the nodes attached to the node containers. """
        # scan all node containers
        nodes = []
        for node_container in self.get_nodes_containers():
            node = node_container.get_attached_node()
            if isinstance(node, Node): 
                nodes.append(node)
        return nodes 
        
    def get_attached_nodes_names(self): 
        """Returns a list of the names of the nodes attached to the node containers. """
        names = []
        for node in self.get_attached_nodes(): 
            names.append(node.name)
        return names
        
    def get_attached_node(self,name): 
        """Returns the attached node with the given name. """
        for node in self.get_attached_nodes(): 
            if node.name == name: 
                return node
        return None
        
    def has_attached_node(self,node): 
        """Returns True if the given node (given by name or instance) is attached to one of the node containers. """
        for container in self.get_nodes_containers(): 
            if isinstance(node,Node): 
                if container.get_attached_node() == node: 
                    return True
            elif isinstance(node,'str'): 
                if container.get_attached_node().name == node: 
                    return True 
        return False 

    def set_name(self,name): 
        """Sets the name of the dependence object. """
        self.name = name
        
    def get_name(self): 
        """Returns the name of the dependence object. """
        return self.name

        
    # private

    def has_log_conditional_probability_gradient_variable(self,variable): 
        """Returns True if a method to compute the gradient of the log of the conditional 
        probability distribution associated to the given variable is defined. """
        if not self.has_variable(variable): 
            raise ParameterError("Variable %s does not exist. The variables are: %s. "%(variable,self.get_variables_names()))
        return hasattr(self,"log_conditional_probability_gradient_"+variable)
       
    def has_log_conditional_probability_hessian_variable(self,variable): 
        """Returns True if a method to compute the Hessian of the log of the conditional 
        probability distribution associated to the given variable is defined. """
        if not self.has_variable(variable): 
            raise ParameterError("Variable %s does not exist. The variables are: %s. "%(variable,self.get_variables_names()))
        return hasattr(self,"log_conditional_probability_hessian_"+variable)

    def has_log_conditional_probability_diagonal_hessian_variable(self,variable): 
        """Returns True if a method to compute the diagonal of the Hessian of the log of the conditional 
        probability distribution associated to the given variable is defined. """
        if not self.has_variable(variable): 
            raise ParameterError("Variable %s does not exist. The variables are: %s. "%(variable,self.get_variables_names()))
        return hasattr(self,"log_conditional_probability_diagonal_hessian_"+variable)
        
    def has_log_conditional_probability_variable(self,variable): 
        """Returns True if a method to compute the log of the conditional probability distribution 
        associated to the given variable is defined. """
        if not self.has_variable(variable): 
            raise ParameterError("Variable %s does not exist. The variables are: %s. "%(variable,self.get_variables_names()))
        return hasattr(self,"log_conditional_probability_"+variable) 

    def has_sample_conditional_probability_variable(self,variable): 
        """Returns True if a method to sample from the conditional probability of the given variable is defined. """ 
        if not self.has_variable(variable): 
            raise ParameterError("Variable %s does not exist. The variables are: %s. "%(variable,self.get_variables_names()))
        return hasattr(self,"sample_conditional_probability_"+variable)
           
    def get_log_conditional_probability_gradient_variable(self,variable): 
        """Returns the gradient of the log of the conditional probability distribution 
        associated to the given variable. """
        if not self.has_variable(variable): 
            raise ParameterError("Variable %s does not exist. The variables are: %s. "%(variable,self.get_variables_names()))
        if not hasattr(self,"log_conditional_probability_gradient_"+variable): 
            raise ModelUndefined("The method to compute the gradient of the log conditional probability of %s is not defined. "%variable) 
        return eval("log_conditional_probability_gradient_"+variable+"()") #FIXME: eventually pass parameters

    def get_log_conditional_probability_hessian_variable(self,variable): 
        """Returns the Hessian of the log of the conditional probability distribution 
        associated to the given variable. """
        if not self.has_variable(variable): 
            raise ParameterError("Variable %s does not exist. The variables are: %s. "%(variable,self.get_variables_names()))
        if not hasattr(self,"log_conditional_probability_hessian_"+variable): 
            raise ModelUndefined("The method to compute the Hessian of the log conditional probability of %s is not defined. "%variable) 
        return eval("log_conditional_probability_hessian_"+variable+"()") #FIXME: eventually pass parameters
       
    def get_log_conditional_probability_hessian_variable(self,variable): 
        """Returns the diagonal of the Hessian of the log of the conditional probability distribution 
        associated to the given variable. """
        if not self.has_variable(variable): 
            raise ParameterError("Variable %s does not exist. The variables are: %s. "%(variable,self.get_variables_names()))
        if not hasattr(self,"log_conditional_probability_diagonal_hessian_"+variable): 
            raise ModelUndefined("The method to compute the diagonal of the Hessian of the log conditional probability of %s is not defined. "%variable) 
        return eval("log_conditional_probability_diagonal_hessian_"+variable+"()") #FIXME: eventually pass parameters
              
    def get_log_conditional_probability_variable(self,variable): 
        """Returns the log of the conditional probability distribution 
        associated to the given variable. """
        if not self.has_variable(variable): 
            raise ParameterError("Variable %s does not exist. The variables are: %s. "%(variable,self.get_variables_names()))
        if not hasattr(self,"log_conditional_probability_"+variable): 
            raise ModelUndefined("The method to compute the log conditional probability of %s is not defined. "%variable) 
        return eval("log_conditional_probability_"+variable+"()") #FIXME: eventually pass parameters
        
    def sample_conditional_probability_variable(self,variable): 
        """Samples from the conditional probability distribution of the given variable. """
        if not self.has_variable(variable): 
            raise ParameterError("Variable %s does not exist. The variables are: %s. "%(variable,self.get_variables_names()))
        if not hasattr(self,"sample_conditional_probability_"+variable): 
            raise ModelUndefined("The method to sample from the log conditional probability of %s is not defined. "%variable) 
        return eval("sample_conditional_probability_"+variable+"()") #FIXME: eventually pass parameters
        

    # Inference interface 
    def has_log_conditional_probability_gradient_node(self,node): 
        """Returns True if a method to compute the gradient of the log of the conditional 
        probability distribution associated to the given node is defined. """
        if not self.has_node(node): 
            raise ParameterError("node %s does not exist. The nodes are: %s. "%(str(node),self.get_nodes_names()))        
        return self.has_log_conditional_probability_gradient_variable(self.variable_name_from_node(node)) 
       
    def has_log_conditional_probability_hessian_node(self,node): 
        """Returns True if a method to compute the Hessian of the log of the conditional 
        probability distribution associated to the given node is defined. """
        if not self.has_node(node): 
            raise ParameterError("node %s does not exist. The nodes are: %s. "%(str(node),self.get_nodes_names()))
        return self.has_log_conditional_probability_hessian_variable(self.variable_name_from_node(node)) 

    def has_log_conditional_probability_diagonal_hessian_node(self,node): 
        """Returns True if a method to compute the diagonal of the Hessian of the log of the conditional 
        probability distribution associated to the given node is defined. """
        if not self.has_node(node): 
            raise ParameterError("node %s does not exist. The nodes are: %s. "%(str(node),self.get_nodes_names()))
        return self.has_log_conditional_probability_diagonal_hessian_variable(self.variable_name_from_node(node)) 
        
    def has_log_conditional_probability_node(self,node): 
        """Returns True if a method to compute the log of the conditional probability distribution 
        associated to the given node is defined. """
        if not self.has_node(node): 
            raise ParameterError("node %s does not exist. The nodes are: %s. "%(str(node),self.get_nodes_names()))
        return self.has_log_conditional_probability_variable(self.variable_name_from_node(node)) 

    def has_sample_conditional_probability_node(self,node): 
        """Returns True if a method to sample from the conditional probability of the given node is defined. """ 
        if not self.has_node(node): 
            raise ParameterError("Variable %s does not exist. The nodes are: %s. "%(str(node),self.get_nodes_names()))
        return self.has_sample_conditional_probability_variable(self.variable_name_from_node(node)) 
        
    def get_log_conditional_probability_gradient_node(self,node): 
        """Returns the gradient of the log of the conditional probability distribution 
        associated to the given node (given by name or instance) - if possible. """
        # get the name of the variable (node container) attached to the given node (if any). 
        variable_name = sefl.get_variable_name_from_node(node) 
        return self.get_log_conditional_probability_gradient_variable(self,variable_name)

    def get_log_conditional_probability_hessian_node(self,node): 
        """Returns the Hessian of the log of the conditional probability distribution 
        associated to the given node (given by name or instance) - if possible. """
        # get the name of the variable (node container) attached to the given node (if any). 
        variable_name = sefl.get_variable_name_from_node(node) 
        return self.get_log_conditional_probability_hessian_variable(self,variable_name)

    def get_log_conditional_probability_diagonal_hessian_node(self,node): 
        """Returns the diagonal of the Hessian of the log of the conditional probability distribution 
        associated to the given node (given by name or instance) - if possible. """
        # get the name of the variable (node container) attached to the given node (if any). 
        variable_name = sefl.get_variable_name_from_node(node) 
        return self.get_log_conditional_probability_diagonal_hessian_variable(self,variable_name)
                   
    def get_log_conditional_probability_node(self,node): 
        """Returns the log of the conditional probability distribution 
        associated to the given node (given by name or instance) - if possible. . """
        # get the name of the variable (node container) attached to the given node (if any). 
        variable_name = sefl.get_variable_name_from_node(node) 
        return self.get_log_conditional_probability_variable(self,variable_name)
        
    def sample_node(self,node):
        """Sample from the given node - if possible). """
        # get the name of the variable (node container) attached to the given node (if any). 
        variable_name = sefl.get_variable_name_from_node(node) 
        return self.sample_variable(self,variable_name)




class Node(): 
    """Node of a graphical model. A node represents a variable or set of variables. 
    The node is characterized by name, value, and by the given flag. The flag is True if 
    the variable is considered a given quantity, False if it considered unknown (uncertain). """
    def __init__(self,name,value=None,given=False): 
        self.name = name
        if not value == None: 
            self.value = value
        self.given = given
        self.dependencies_attached = []
        self.data_type = None
        
    def set_given(self,is_given): 
        """Sets the state of the given flag. """
        self.given = bool(is_given)
        return True
        
    def is_given(self):
        """Returns the state of the given flag""" 
        return self.given
        
    def set_value(self,value):
        """Sets the value associated to the node. The value must be an instance of numpy.ndarray"""
        try: 
            value = numpy.asarray(value)
        except: 
            raise UnexpectedParameterType("'value' is expected to be an instance of numpy.ndarray") 
        self.value = value
        return True
        
    def set_name(self,name): 
        """Sets the name of the node. """
        self.name = str(name)
        return True

    def get_value(self):
        """Returns the value associated to the node. """
        return self.value
        
    def get_name(self):
        """Returns the name of the node. """
        return self.name
    
    def get_dependencies_attached(self): 
        """Returns a list of the Dependence objects associated to the node 
        (it's an empty list if the node is not inserted in a Probabilistic Graphical Model). """    
        return self.dependencies_attached

    def set_data_type(self,data_type): 
        """Sets the data type associated with the node. """
        set_data_type(self,data_type) 
        return True
    
    def zeros(self): 
        """Return an array of zeros of the same size and shape as the value of the node. """
        return numpy.zeros(self.value.shape)



        
class ProbabilisticGraphicalModel():
    """Probabilistic Graphical Model. This is the central object of ilang. It represents a probabilistic 
    model. A specific model is constructed by setting Nodes and Dependencies. """
    def __init__(self,node_names=[]):
        if not isinstance(node_names,type([])): 
            raise UnexpectedParameterType("Optional list_of_names must be a list. ")
        self.nodes = {}  
        self.dependencies = {} 
        self.add_nodes(node_names) 
        
    # Handling of nodes
    def add_node(self,node,value=None,given=None): 
        "Add single node to the Probabilistic Graphical Model. Optionally specify value and given flag" 
        # check parameter type:  
        if not (isinstance(node,Node) or isinstance(node,str)):
            raise UnexpectedParameterType("node %s is not an instance of Node or a string identifying the name of a new node"%str(node)) 
        # check if node is already in the dag
        if isinstance(node,str): 
            name = node
        else: 
            name = node.name
        if self.has_node(node) or self.has_node(name): 
            raise ParameterError("The graphical model already has the given node (node name: %s) "%str(name))
        # modify the node value and flag if specified: 
        if isinstance(node,Node): 
            if value != None:
                node.set_value(value)
            if given != None: 
                node.set_given(given)
        else: 
            node = Node(name,value,given)
        self.nodes[name] = node
        return True
            
        
    def add_nodes(self,list_of_nodes):
        """Add multiple nodes to the Probabilistic Graphical Model. """
        # check for correct parameter type
        if not isinstance(list_of_nodes,type([])): 
            list_of_nodes = [list_of_nodes,]
        for node in list_of_nodes: 
            if not (isinstance(node,Node) or isinstance(node,str)): 
                raise UnexpectedParameterType("node % is not an instance of Node or a string identifying the name of a new node. "%str(node))            
        names = [] 
        # verify if the given names are unique
        for node in list_of_nodes: 
            if isinstance(node,str): 
                names.append(node)
            else: 
                names.append(node.name)
        if len(names)!=len(set(names)): 
            raise ParameterError("There are nodes with identical names in the list. Each node of a Probabilistic Graphical Model must have a unique name. ")
        # verify if the nodes are unique (this applies in case nodes are Node instances)
        if len(list_of_nodes)!=len(set(list_of_nodes)): 
            raise ParameterError("There are identical nodes in the list. Each node must appear only once in the graph. ")
        # check if any of the given nodes or node names already exist 
        for node in list_of_nodes: 
            if isinstance(node,str): 
                name = node
            else: 
                name = node.name
            # check if node with same name exists
            if self.has_node(node) or self.has_node(name): 
                raise ParameterError("The graphical model already has the given node (node name: %s) "%str(name))
        # add the nodes to the graph
        for node in list_of_nodes: 
            self.add_node(node)
        return True
 
    def get_node(self,name): 
        """Returns the node with given name. """
        if not self.has_node(name): 
            raise ParameterError("Node with name %s does not exist. "%name)
        return self.nodes[name]
        
    def get_nodes(self): 
        """Returns a list of all nodes. """
        return self.nodes.values() 
        
    def get_nodes_names(self): 
        """Returns a list of the names of all nodes. """
        return self.nodes.keys() 

    def is_node_given(self,node): 
        """Returns True is the node represents a given quantity. See the properties of Node. """
        if isinstance(node,Node): 
            name = node.name 
        elif isinstance(node,str): 
            name = node
        else: 
            raise UnexpectedParameterType("node must be an instance of Node or a valid node name. ")
        node = self.get_node(name) 
        if not isinstance(node,Node): 
            raise ParameterError ("Probabilistic Graphical Model does not have a node named "+str(name))
        return node.is_given() 
        
    def set_nodes_given(self,list_of_nodes,is_given): 
        """Sets the state of the 'given' flag of the nodes in the list. """
        if not isinstance(list_of_nodes,type([])): 
            list_of_nodes = [list_of_nodes,]
        for node in list_of_nodes: 
            if isinstance(node,Node): 
                name = node.name 
            elif isinstance(node,str): 
                name = node
            else: 
                raise UnexpectedParameterType("node must be an instance of Node or a valid node name. ")
            node = self.get_node(name) 
            if not isinstance(node,Node): 
                raise ParameterError ("Probabilistic Graphical Model does not have a node named "+str(name))
        for node in list_of_nodes: 
            node = self.get_node(node) 
            node.set_given(is_given) 
        return True 
        
    def get_node_value(self, node): 
        """Returns the value of the node. """
        if isinstance(node,Node): 
            name = node.name 
        elif isinstance(node,str): 
            name = node
        else: 
            raise UnexpectedParameterType("node must be an instance of Node or a valid node name. ")
        node = self.get_node(name) 
        if not isinstance(node,Node): 
            raise ParameterError ("Probabilistic Graphical Model does not have a node named "+str(name))
        return node.get_value() 
            
    def set_node_value(self, node, value): 
        """Sets the value of the node. """
        if isinstance(node,Node): 
            name = node.name 
        elif isinstance(node,str): 
            name = node
        else: 
            raise UnexpectedParameterType("node must be an instance of Node or a valid node name. ")
        node = self.get_node(name) 
        if not isinstance(node,Node): 
            raise ParameterError ("Probabilistic Graphical Model does not have a node named "+str(name))
        node.set_value(value) 
        return True 

    def has_node(self,node):
        """Returns True if the Probabilistic Graphical Model includes a given node (given by name or node instance). """
        if isinstance(node,Node): 
            name = node.name
        else: 
            name = node 
        return name in self.nodes.keys() 

    def remove_node(self,node): 
        """Removes from the Probabilistic Graphical Model the given node (given by name or node instance)"""
        if isinstance(node,Node): 
            name = node.name
        else: 
            name = node    
        if not self.has_node(node): 
            raise ParameterError ("Probabilistic Graphical Model does not have a node named "+str(name))      
        return self.nodes.pop(name)


        
    # Handling of dependencies
    def add_dependence(self,dependence,links=None): 
        """Adds a probabilistic dependence between nodes (or amongst the variables of a single - milti-dimensional - node). 
        'dependence' must be an instance of Dependence. 'links' is optional and specifies how the variables of object 'dependence' 
        must be attached to the nodes. 'attach_dependence' can be used alternatively (at a later stage).  """ 
        # check for correct parameter type
        if not isinstance(dependence,Dependence): 
            raise UnexpectedParameterType("dependence must be an instance of Dependence")
        if links != None:
            if not isinstance(links, type({})):
                raise UnexpectedParameterType("links must be a dictionary") 
        # check if the dependence has been already added to the graph  
        if self.has_dependence(dependence): 
            raise ParameterError("The graphical model already has the dependence %s. "%str(dependence.get_name()))
        # add the dependence 
        self.dependencies[dependence.get_name()] = dependence 
        # optionally attach dependence
        if links != None: 
            self.attach_dependence_to_nodes(dependence,links)
        return True

    def remove_dependence(self,dependence): 
        """Removes the dependence (given by name or instance) from the Probabilistic Graphical. """
        if isinstance(dependence,Dependence): 
            name = dependence.get_name()
        else: 
            name = dependence  
        if not self.has_dependence(dependence): 
            raise ParameterError ("The dependence %s is not attached to the Probabilistic Graphical Model. "+name)      
        #FIXME: tell the nodes and tell the dependence (returned by the current function, though detached)  
        return self.dependencies.pop(name)
        
    def get_dependence(self,name): 
        """Returns the dependence with given name. """
        if not self.has_dependence(name): 
            raise ParameterError("Dependence with name %s does not exist. "%name)
        return self.dependencies[name]

    def get_dependencies(self): 
        """Returns a list of all the dependencies attached to the graph. """
        return self.dependencies.values() 

    def get_dependencies_names(self): 
        """Returns a list of the names of all the dependencies attached to the graph. """
        return self.dependencies.keys() 

    def has_dependence(self,dependence):
        """Returns True if the Probabilistic Graphical Model includes the dependence (given by name or instance). """
        if isinstance(dependence,Dependence): 
            name = dependence.get_name()
        else: 
            name = dependence
        return name in self.dependencies.keys() 

    def attach_dependence_to_nodes(self,dependence,links): 
        """Attach the variables of the given dependence to the nodes of the graph. 
        The links between variables and nodes must be specified in a dictionary: 
        {'variable_name1':'node_name1','variable_name2':'node_name2'} """
        # make sure that the dependence object is one of the dependencies of the graph
        if not self.has_dependence(dependence): 
            raise ParameterError("The specified dependence is not one of the dependencies of the graph. Add the dependence first: add_dependence()") 
        # verify that all the variables specified in the links dictionary exist
        for variable_name in links.keys(): 
            if not dependence.has_variable_named(variable_name): 
                raise ParameterError("One of the specified variables (%s) does not exist. The variables are %s. "%(variable_name,dependence.get_variables_names()))
        # verify that all the nodes specified in the links dictionary exist
        for node in links.values(): 
            if not self.has_node(node): 
                raise ParameterError("One of the specified nodes (%s) does not exist. The nodes are %s. "%(node,self.get_nodes_names()))
        # replace nodes names with nodes if nodes were specified by name 
        for variable_name in links.keys(): 
            node = links[variable_name]
            if isinstance(node,str): 
                node = self.get_node(node) 
                links[variable_name] = node
        # tell dependence to which nodes it is now attached (dependence will tell each of the nodes about it) 
        dependence.attach_to_nodes(links) 

    def is_dependence_fully_attached(self,dependence): 
        """Returns True if all the variables of the dependence object are attached to a node. """
        return dependence.is_fully_attached() 


    # Properties of the graph
    def d_separation(self, nodeA, nodeB, given_node): 
        """Checks if nodeA is independent from nodeB given node given_node. """
        pass
    
    def markov_blanket(self, node): 
        """Return the list of nodes that form the Markov Blanket of the given node. """
        pass 

    def get_parents(self, node): 
        """Returns the list of parents of the given node. """
        pass
            
    def get_children(self, node): 
        """Returns the list of children of the given node. """
        pass 
        
    def get_node_dependencies(self, node): 
        """Returns the list of dependencies attached to the given node. """
        # scan all the dependencies of the probabilistic graphical model 
        dependencies = []
        for d in self.get_dependencies():
            if d.has_attached_node(node): 
                dependencies.append(d)
        return dependencies 
                       
    def is_complete(self): 
        """Returns True if for every dependence attached to the graph all variables are attached to a node. 
        Therefore it returns False if there are variables of at least of Dependence object not attached to a node of the graph. """
        # check if all the attached dependencies are fully attached: 
        for dependence in self.get_dependencies(): 
            if not self.is_dependence_fully_attached(dependence): 
                return False
        # verify if there are unattached nodes: 
        for node in self.get_nodes(): 
            if self.get_node_dependencies(node) == []: 
                return False
        return True 



    # Inference
    def get_log_conditional_probability(node): 
        """Returns the log of the conditional probability of the given node. """
        # sum over the dependencies associated to the given node 
        log_p = 0 
        for dependence in self.get_node_dependencies(node): 
            if not self.dependence.has_log_conditional_probability_node(node): 
                raise UndefinedModelProperty("Dependence %s does not have a method to compute the log probability of the conditional probability of %s ( -> %s). "%(dependence.get_name(),node.get_name(),dependence.get_variable_name_from_node(node)))
        for dependence in self.get_node_dependencies(node): 
            log_p += dependence.get_log_conditional_probability(node)
        return log_p

    def get_log_conditional_probability_gradient(node): 
        """Returns the gradient of the log of the conditional probability of the given node. """
        # sum over the dependencies associated to the given node 
        gradient = node.zeros() 
        for dependence in self.get_node_dependencies(node): 
            if not self.dependence.has_log_conditional_probability_gradient_node(node): 
                raise UndefinedModelProperty("Dependence %s does not have a method to compute the gradient of the log probability of the conditional probability of %s ( -> %s). "%(dependence.get_name(),node.get_name(),dependence.get_variable_name_from_node(node)))
        for dependence in self.get_node_dependencies(node): 
            gradient += dependence.get_log_conditional_probability_gradient(node)
        return gradient 
        
    def get_log_conditional_probability_hessian(node): 
        """Returns the Hessian of the log of the conditional probability of the given node. """
        # sum over the dependencies associated to the given node 
        hessian = node.zeros() 
        for dependence in self.get_node_dependencies(node): 
            if not self.dependence.has_log_conditional_probability_hessian_node(node): 
                raise UndefinedModelProperty("Dependence %s does not have a method to compute the Hessian of the log probability of the conditional probability of %s ( -> %s). "%(dependence.get_name(),node.get_name(),dependence.get_variable_name_from_node(node)))
        for dependence in self.get_node_dependencies(node): 
            hessian += dependence.get_log_conditional_probability_hessian(node)
        return hessian 

    def get_log_conditional_probability_diagonal_hessian(node): 
        """Returns the Hessian of the log of the conditional probability of the given node. """
        # sum over the dependencies associated to the given node 
        diaghessian = node.zeros() 
        for dependence in self.get_node_dependencies(node): 
            if not self.dependence.has_log_conditional_probability_diagonal_hessian_node(node): 
                raise UndefinedModelProperty("Dependence %s does not have a method to compute the diagonal of the Hessian of the log probability of the conditional probability of %s ( -> %s). "%(dependence.get_name(),node.get_name(),dependence.get_variable_name_from_node(node)))
        for dependence in self.get_node_dependencies(node): 
            diaghessian += dependence.get_log_conditional_probability_diagonal_hessian(node)
        return diaghessian 


    # Export graph    
    def export_dictionary(self): 
        """Export a dictionary that describes the graph. """
        graph = {}
        # list the nodes 
        nodes = []
        for node in self.get_nodes(): 
            if node.is_given(): 
                node_type = 1
            else: 
                node_type = 0
            nodes.append({'name':node.name,'type':node_type})
        graph['nodes'] = nodes
        # walk through the dependence objects and list all the (inner) dependencies 
        links = []
        for dependence in self.get_dependencies(): 
            dependencies = dependence.dependencies() 
            for link in dependencies: 
                if link[2] == 'directed': 
                    link_type = 't1'
                else: 
                    link_type = 't2'
                link_source = dependence.get_node_from_variable_name(link[0]).name
                link_target = dependence.get_node_from_variable_name(link[1]).name
                links.append({'source':link_source,'target':link_target,'type':link_type}) 
        graph['links'] = links
        return graph

    def export_pickle(self): 
        """Export a pickled representation of the graph. """
        from pickle import dumps
        return dumps(self.export_dictionary())
 
    def export_json(self): 
        """Export a json representation of the graph. """
        from json import dumps
        return dumps(self.export_dictionary())


    # Visualisation 
    def webdisplay(self,background=True): 
        #try: 
        from webgui.QuickDisplay import display_graph
        display_graph(self,background)


