'''
Main module to start the application and the Controller class

Created on 26.03.2013

@author: Clemens.Teichmann@dlr.de

   Copyright [2013] [Clemens.Teichmann@dlr.de]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
import pyprov.server, pyprov.neo4j
import pyprov.general_model as genm

class Controller(object):
    """Control the entire program (data flow, process chain etc.)
    
    parameters:
    server -- the webserver for the REST-Interface
    graph_db -- the (graph) database to store provenance information
    dev_factory -- interface between server (provenance input) and database (provenance store)
    """
    def __init__(self):
        self.server = pyprov.server.Server(self)
        self.graph_db = pyprov.neo4j.Neo4JServer(self)
        self.dev_factory = DevFactory(self.graph_db)
        self.running = False
    
    def start(self):
        self.server.create_app()
        
        self.graph_db.run()
        self.server.run()
        if self.graph_db.running and self.server.running:
            self.running = True
            

        
class DevFactory(object):
    """Transform input data to internal objects and store them into the database
    
    parameters:
    graph_db -- the underlying database to provide 'write' or 'create'-methods    
    """
    def __init__(self, graph_db):
        self.graph_db = graph_db
    
    def create(self, model_type, *args, **kwargs):
        """Determine process type and start storing
        
        This method is the main external interface to write provenance data.
        All views from the webserver write their information with this method
        using the 'model_type' to define the type of information and 
        the arguments and keyword arguments to hand over the data.
        
        arguments:
        model_type -- determine which method to call
        """
        if model_type == 'general':
            return self._create_general(*args, **kwargs)
    
    def _create_general(self, *args, **kwargs):
        """Create a general process and all associated nodes and relationships  
        
        arguments:
        process
        input
        output
        actor
        
        keyword arguments:
        None
        """
        process = genm.Process(*args, **kwargs)
        process_node = self.graph_db.create_process(process.name)
        
        actor_node = self.graph_db.find_node('identifier', process.actor.identifier)
        if not actor_node:
            actor_node = self.graph_db.create_actor(process.actor)
        
        for inp in process.inp:
            input_node = self.graph_db.create_input(inp)
            self.graph_db.create_relationship('USED', process_node, input_node)
            
        for outp in process.outp:
            output_node = self.graph_db.create_output(outp)
            self.graph_db.create_relationship('WAS_GENERATED_BY', output_node, process_node)
        
        self.graph_db.create_relationship('WAS_ASSOCIATED_WITH', process_node, actor_node)
        
        
        return True

if __name__ == '__main__':
    controller = Controller()
    controller.start()