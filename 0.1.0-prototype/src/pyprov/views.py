'''
This is the main view module.

Every view for the REST and Gremlin interface is defined here with its parameters.

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
from flask import Blueprint, request, make_response

class View(Blueprint):
    def __init__(self, name, import_name, url_prefix=None):
        super(View, self).__init__(name, import_name, url_prefix=url_prefix)
        self.server = None

class RestView(View):
    """
    Set up path to save provenance informations about software development processes
    """
    def __init__(self):
        #TODO: add version number in uri
        super(RestView, self).__init__('rest', __name__, url_prefix='/prov')
        self.add_url_rule('/', 'rest_index', self.rest_index)
        self.add_url_rule('/general', 'general', self.general, methods=['GET', 'POST'])
        
    def rest_index(self):
        """
        Provide an Introduction to the REST-Interface.
        """
        return 'Welcome to PyPROVs REST-Interface!'
    
    def general(self):
        """Save Build information.
        
        required params:
            revision - the number of the corresponding revision (int)
            result   - the return code of the build (int)
            maven    - the used version of maven for the build (string)
            
        optional params:
            None
        """
        if request.method == 'POST':
            try:
                process = request.json['process']
                inp = request.json['input']
                outp = request.json['output']
                actor = request.json['actor']
                self.server.write_prov('general', process, inp, outp, actor)
                return 'True'
            except (TypeError, ValueError) as e:
                return make_response(''+e.message, 400)
        #TODO: GET must return the provenance data
        else:
            return self.general.__doc__

class GremlinView(View):
    """Set up path to the gremlin query interface"""
    def __init__(self):
        super(GremlinView, self).__init__('gremlin', __name__, url_prefix='/gremlin')
        self.add_url_rule('/', 'gremlin_index', self.gremlin_index)
        self.add_url_rule('/query', 'query', self.query, methods=['GET', 'POST'])
        
    def gremlin_index(self):
        """
        Provide an Introduction to the Gremlin-Interface.
        """
        return 'Gremlin Interface'
    
    def query(self):
        if request.method == 'POST':
            pass
        else:
            return 'Query!'
    