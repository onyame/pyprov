'''
Created on 05.04.2013

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

import provenance_model as pm
   
class Process(pm.Activity):
    def __init__(self, name, inps, outps, actor):
        self.name = name
        self.actor = Actor(actor)
        
        self.inp = []
        self.outp = []
        for inp in inps:
            self.inp.append(Inp(inp['identifier'], inp['version']))
        for outp in outps:
            self.outp.append(Outp(outp['identifier'], outp['version']))

class Inp(pm.Entity):
    def __init__(self, identifier, version):
        self.identifier = identifier
        self.version = version

class Outp(pm.Entity):
    def __init__(self, identifier, version):
        self.identifier = identifier
        self.version = version
        
class Actor(pm.Agent):
    def __init__(self, identifier):
        self.identifier = identifier
