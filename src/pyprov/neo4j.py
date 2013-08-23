'''
Created on 27.03.2013

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
import time
import abc
from py2neo import neo4j, rest

URL = 'http://localhost:7474/db/data/'

class ProvenanceStore(object):
    """The abstract basis class for all provenance stores.
    
    All implemented stores should inherit from this class to ensure correct interface usage.
    
    parameters:
    controller -- the managing controller class (Controller)
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, controller):
        self.controller = controller
    
    def create_process(self, name):
        return self.create_node('ACTIVITY', 'PROCESS', name=name, timestamp=str(time.time()))
    
    def create_input(self, inp):
        return self.create_node('ENTITY', 'INPUT', identifier=inp.identifier, version=inp.version)
    
    def create_output(self, outp):
        return self.create_node('ENTITY', 'OUTPUT', identifier=outp.identifier, version=outp.version)
    
    def create_actor(self, actor):
        return self.create_node('AGENT', 'ACTOR', identifier=actor.identifier)
 
    @abc.abstractmethod
    def create_node(self, prov_type, sdm_type, **properties):
        """abstract method to create a node in the database
        
        arguments:
        prov_type -- an uppercase string to determine the provenance node type (ENTITY, ACTIVITY or AGENT).
        sdm_type -- an uppercase string to determine the type from the software development model.
        **properties -- list of keyword arguments which is completely added to the node.
        """
        pass
    
    @abc.abstractmethod
    def create_relationship(self, rel_type, start_node, end_node, **properties):
        """abstract method to create a releationship in the database
        
        arguments:
        rel_type -- an uppercase string to determine the type of relationship between the two nodes, i.e. the predicate
        start_node -- the outgoing node, from where the relationship starts, i.e. the subject 
        end_node -- the incoming node, to where the relationship end, i.e the object
        **properties -- list of keyword arguments which is completely added to the relationship.
        """
        pass

    @abc.abstractmethod
    def find_node(self, key, value):
        """abstract method to find a node in the database
        
        arguments:
        key -- what key/identifier should be searched (string)
        value -- what value has should that key have (type specified by key)
        """
        pass
    
    @abc.abstractmethod
    def find_relationship(self, rel_type=None, start_node=None, end_node=None, bidirectional=None, limit=None):
        """abstract method to find a relationship in the database
        
        keyword arguments:
        rel_type -- type of relationships to find (None if any
        start_node -- concrete start node (None if any)
        end_node -- concrete end node to find (None if any)
        bidirectional --  True if reversed relationships should also be included
        limit -- maximum number of relationships to match or None if no limit
        """
        pass
    
class Neo4JServer(ProvenanceStore):
    """The Neo4J-Provenance Store.
    
    parameters:
    graph_db -- connection to Neo4J backend (GraphDatabaseService)    
    """
    def __init__(self, controller):
        super(Neo4JServer, self).__init__(controller)
        self.graph_db = None
        self.running = False
        self.node_index = None
        
    def setup_database(self):
        """Connect to the database and get or create the indexes"""
        try:
            self.graph_db = neo4j.GraphDatabaseService(URL)
        except rest.ResourceNotFound:
            print 'Database service not found'
        self.node_index = self.graph_db.get_or_create_index(neo4j.Node, 'Nodes')
                
    def find_node(self, key, value):
        """Find a node with a given key-value pair.
        
        First search the node index for the key and value.
        Then return the node with the highest identifier.
        
        arguments:
        key -- what key/identifier should be searched (string).
        value -- what value has should that key have (type specified by key)    .    
        """
        results = self.node_index.get(key, str(value))
        result = None
        ident = 0
        for node in results:
            if node.id > ident:
                result = node
                ident = node.id
        return result
     
    def find_relationship(self, rel_type=None, start_node=None, end_node=None, bidirectional=None, limit=None):
        """Find a relationship with possible specifications.
        
        First match the database for the given keyword arguments.
        Then return the relationship with the highest identifier.
        
        keyword arguments:
        rel_type -- type of relationships to find (None if any
        start_node -- concrete start node (None if any)
        end_node -- concrete end node to find (None if any)
        bidirectional --  True if reversed relationships should also be included
        limit -- maximum number of relationships to match or None if no limit    
        """
        results = self.graph_db.match(start_node=start_node, rel_type=rel_type, end_node=end_node, bidirectional=bidirectional, limit=limit)
        result = None
        ident = 0
        for rel in results:
            if rel.id > ident:
                result = rel
                ident = rel.id
        return result   
        
    def create_node(self, prov_type, sdm_type, **properties):
        """Create a new node with its properties.
        
        A node is created using the prov_type and sdm_type.
        Then all given keyword arguments within 'properties' are added to the node.
        After the node was added to the index, it's returned
        
        arguments:
        prov_type -- an uppercase string to determine the provenance node type (ENTITY, ACTIVITY or AGENT).
        sdm_type -- an uppercase string to determine the type from the software development model.
        **properties -- list of key-value-pairs to add more properties to the node
        """
        node, = self.graph_db.create({'prov_type':prov_type, 'type':sdm_type})
        node.update_properties(properties)
        for key, value in properties.iteritems():
            if value:
                self.node_index.add(key, value, node)
        return node
        
    def create_relationship(self, rel_type, start_node, end_node, **properties):
        """Create a new relationship between two nodes
        
        arguments:
        rel_type -- an uppercase string to determine the type of relationship between the two nodes, i.e. the predicate
        start_node -- the outgoing node, from where the relationship starts, i.e. the subject 
        end_node -- the incoming node, to where the relationship end, i.e the object
        **properties -- list of keyword arguments which is completely added to the relationship.
        """
        relationship, = self.graph_db.create((start_node, rel_type, end_node))
        relationship.update_properties(properties)
        
    def run(self):
        """starting the database service"""
        if not self.graph_db:
            self.setup_database()
        self.running = True