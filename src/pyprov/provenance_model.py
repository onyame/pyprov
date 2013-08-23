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
import uuid
class Agent(object):
    def __init__(self):
        self.agent_id = uuid.uuid4()

class Entity(object):
    def __init__(self):
        self.entity_id = uuid.uuid4()
        
class Activity(object):
    def __init__(self):
        self.activity_id = uuid.uuid4()
        self.start_time = None
        self.end_time = None

class Usage(object):
    def __init__(self, activity, entity=None, usage_id=None, time=None):
        self.activity = activity
        self.entity = entity
        self.usage_id = usage_id
        self.time = time

class Generation(object):
    def __init__(self, entity, activity=None, generation_id=None, time=None):
        self.entity = entity
        self.activity = activity
        self.generation_id = generation_id
        self.time = time
        
class Communication(object):
    def __init__(self, informed, informant, communication_id=None):
        self.informed = informed
        self.informant = informant
        self.communication_id = communication_id
        
class Derivation(object):
    def __init__(self, generated_entity, used_entity, 
                    derivation_id=None, activity=None,
                    generation=None, usage=None):
        self.generated_entity = generated_entity
        self.used_entity = used_entity
        self.derivation_id = derivation_id
        self.activity = activity
        self.generation = generation
        self.usage = usage

class Attribution(object):
    def __init__(self, entity, agent, attribution_id=None):
        self.entity = entity
        self.agent = agent
        self.attribution_id = attribution_id

class Association(object):
    def __init__(self, activity, association_id=None, agent=None):
        self.activity = activity
        self.association_id = association_id
        self.agent = agent