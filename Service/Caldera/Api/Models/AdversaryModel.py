"""
Author: 	Gari Arellano
Date:		21-03-2025
Project: 	Caldera
Filename:	AdversaryModel.py
Description:
  This class represent and adversary in the Caldera server. It is used to create an adversary
  object and send it to the Caldera server. 

"""


class AdversaryModel:
    def __init__(self, adversary_id="", name="", description="", atomic_ordering="", objetive="", tags=[], 
                 plugin="null"):
        self.adversary_id = adversary_id
        self.name = name
        self.description = description
        self.atomic_ordering = atomic_ordering
        self.objetive = objetive
        self.tags = tags
        self.plugin = plugin

    # Setters
    def set_adversary_id(self, adversary_id):
        self.adversary_id = adversary_id
    def set_name(self, name):
        self.name = name
    def set_description(self, description):
        self.description = description
    def set_atomic_ordering(self, atomic_ordering):
        self.atomic_ordering = atomic_ordering
    def set_objetive(self, objetive):
        self.objetive = objetive
    def set_tags(self, tags):
        self.tags = tags
    def set_plugin(self, plugin):
        self.plugin = plugin

    # Getters
    def get_adversary_id(self):
        return self.adversary_id
    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def get_atomic_ordering(self):  
        return self.atomic_ordering
    def get_objetive(self):
        return self.objetive
    def get_tags(self):
        return self.tags
    def get_plugin(self):
        return self.plugin
    
    # PRE: None
    # POST: Returns a dictionary with the adversary information
    def to_dict(self):
        return {
            "adversary_id": self.adversary_id,
            "name": self.name,
            "description": self.description,
            "atomic_ordering": self.atomic_ordering,
            "objetive": self.objetive,
            "tags": self.tags,
            "plugin": self.plugin
        }