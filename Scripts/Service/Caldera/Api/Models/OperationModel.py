"""
Author: 	Gari Arellano
Date:		21-03-2025
Project: 	Atlassian
Filename:	OperationModel.py
Description:
  This file contains the Operation class which is used to create an operation in the MITRE Caldera.
"""

class OperationModel:
    def __init__(self, name="", adversary="", group="", obfuscator="", jitter="", planner="", state="", autonomous="0", 
                 auto_close="true", visibility="0", objective="", use_learning_parsers="true", source="", id=""):
        self.name = name
        self.adversary = adversary
        self.jitter = jitter
        self.planner = planner
        self.state = state
        self.obfuscator = obfuscator
        self.autonomous = autonomous
        self.auto_close = auto_close
        self.visibility = visibility
        self.objective = objective
        self.use_learning_parsers = use_learning_parsers
        self.group = group
        self.source = source
        self.id = id
    
    # Setters
    def set_name(self, name):
        self.name = name
    def set_adversary(self, adversary):
        self.adversary = adversary
    def set_jitter(self, jitter):
        self.jitter = jitter
    def set_planner(self, planner):
        self.planner = planner
    def set_state(self, state):
        self.state = state
    def set_obfuscator(self, obfuscator):
        self.obfuscator = obfuscator
    def set_autonomous(self, autonomous):
        self.autonomous = autonomous
    def set_auto_close(self, auto_close):
        self.auto_close = auto_close
    def set_visibility(self, visibility):
        self.visibility = visibility
    def set_objective(self, objective):
        self.objective = objective
    def set_use_learning_parsers(self, use_learning_parsers):
        self.use_learning_parsers = use_learning_parsers  
    def set_group(self, group):
        self.group = group
    def set_source(self, source):
        self.source = source
    def set_id(self, id):
        self.id = id

    # Getters
    def get_name(self):
        return self.name  
    def get_adversary(self):
        return self.adversary
    def get_jitter(self):
        return self.jitter
    def get_planner(self):
        return self.planner
    def get_state(self):
        return self.state
    def get_obfuscator(self):
        return self.obfuscator        
    def get_autonomous(self):
        return self.autonomous
    def get_auto_close(self):
        return self.auto_close
    def get_visibility(self):
        return self.visibility
    def get_objective(self):
        return self.objective 
    def get_use_learning_parsers(self):
        return self.use_learning_parsers
    def get_group(self):  
        return self.group
    def get_source(self):
        return self.source  
    
    # PRE: None
    # POST: Returns a dictionary with the operation information
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "adversary": self.adversary.to_dict(),
            "jitter": self.jitter,
            "planner": self.planner,
            "state": self.state,
            "obfuscator": self.obfuscator,
            "autonomous": self.autonomous,
            "auto_close": self.auto_close,
            "visibility": self.visibility,
            "objective": self.objective,
            "use_learning_parsers": self.use_learning_parsers,
            "group": self.group,
            "source": self.source
        }
    