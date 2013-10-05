
# ilang - Inference Language 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# Oct 2013, Helsinki 

__all__ = ['display_graph']

import thread
from webserver import serve 
from webbrowser import open_new_tab
import json 
from ilang.exceptions import *
from ilang.verbose import print_runtime, print_debug 
import os, shutil
import urllib2
from random import random
from time import sleep 


def setup_local_files(): 
    cwd = os.getcwd()+"/"
    webgui_dir = os.path.dirname(__file__)+"/" 
    for f in os.listdir(webgui_dir): 
        if f.endswith('.html') or f.endswith('.js'): 
            shutil.copyfile(webgui_dir+f,cwd+f)

def save_json(graph):
    s = 'var graph = '+graph
    cwd = os.getcwd() 
    fid = open(cwd+'/ilang_graph_data.js','w')
    fid.write(s)
    fid.close()
        
def display_graph(graph,background=False): 
    # if not a json string, see if the given object has a .export_json() method. 
    if not isinstance(graph,str): 
        if hasattr(graph,'export_json'): 
            graph = graph.export_json() 
        else: 
            raise UnexpectedParameterType("The given object does not seem to be a graph. ") 
    setup_local_files()
    save_json(graph)
    address = "127.0.0.1" 
    port = 8080 
    open_new_tab('http://%s:%s/ilang_graph.html'%(address,str(port))) 
    
    # check if server is running, serving the files in the current working directory: 
    s = str(random())
    cwd = os.getcwd() 
    fid = open(cwd+'/a_random_number.txt','w')
    fid.write(s)
    fid.close() 
    server_ok = False
    try:
        data = urllib2.urlopen('http://%s:%s/a_random_number.txt'%(address,str(port)))
        if str(data.read()) == s: 
            server_ok = True
    except: 
        pass
    # start server
    if not server_ok: 
        if background:
            thread.start_new_thread(serve,((address,port)))
        else: 
            serve(address,port)
    else: 
        print_debug("Display server already running. ")
        if not background: 
            while(1): 
                sleep(0.5)



def test(): 
    graph = json.dumps({'nodes': [{"name":"A","type": 0}, {"name":"B","type": 1}, 
                                  {"name":"C","type": 0}, {"name":"D","type": 2}],
                        'links': [{"source": "A", "type": "t0", "target": "C"}, 
                                  {"source": "B", "type": "t1", "target": "C"},
                                  {"source": "D", "type": "t2", "target": "C"}] }) 
    display_graph(graph)
        
if __name__ == "__main__":
    test()


