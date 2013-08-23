'''
The webserver module.

A Webserver registers the views it should display and starts the application.

Currently implemented using Flask (http://flask.pocoo.org/).

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
from flask import Flask
import pyprov.views as views
class Server(object):
    '''
    The Server-Class to handle configuration, registering views and run the webserver.
    '''

    def __init__(self, controller):
        self.app = None
        self.controller = controller
        self.running = False
    
    def create_app(self):
        """
        Setup for the flask server.
        
        First creates the so called app, then all views.
        """
        self.app = Flask(__name__)

        rest_view = views.RestView()
        grem_view = views.GremlinView()
        
        self.app.register_blueprint(rest_view)
        self.app.register_blueprint(grem_view)
        
        rest_view.server = self
    
    def write_prov(self, sdm_type, *args, **kwargs):
        """
        Take the raw provenance information and forward it to the factory.
        
        This method is mostly just for seperation of concerns.
        """
        return self.controller.dev_factory.create(sdm_type, *args, **kwargs)
    
    def run(self):
        self.app.debug = False
        self.app.run()
        self.running = True
        
