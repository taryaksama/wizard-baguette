# src/card/manaprod.py
# author: @taryaksama

"""
All code related to the class ManaProduction()
Calculates properties of cards that can produce mana with the following properties
- type of producer
- type, color and amount of mana produced
"""

import pandas as pd
import re
from typing import List, Dict

# Load all dependent features
from .card import *
#from .descriptor import *
from .effects import *

MANA_COLORS = {
    "W": 0,
    "U": 0,
    "B": 0,
    "R": 0,
    "G": 0,
    "C": 0,
    "ALL": 0,
}

class ManaProducerFeatures(CardMixin):
    def __init__(self, card:pd.Series):
        self.card = card
        self.manaprod_features = pd.Series({
            'type': None,                   #List[str]
            'mana_produced': MANA_COLORS,   #Dict[str, int]
        })
        self.descriptor = Descriptor(card)
        self.effects = Effects(self.card['text'])
    
    def producer_type(self) -> None:
        # Non-basic Lands
        if self.card.descriptor.is_type(['Land']):
            self.manaprod_features['type'] = 'Lands'

        # Dorks (that do not produces treasures)
        if (
            self.card.descriptor.is_type(['Creature']) 
            & bool('Treasure' not in self.card['keywords'])
        ):
            self.manaprod_features['type'] = 'Dorks'

        # Rocks (artifacts that are not creatures and do not produce treasures)
        if (
            self.card.descriptor.is_type(['Artifact'])
            & 'Creature' not in self.card.descriptor.is_type(['Creature'])
            & 'Treasure' not in self.card['keywords']       
        ):
            self.manaprod_features['type'] = 'Rocks'
        
        # Treasures
        if 'Treasure' in self.card['keywords']:
            self.manaprod_features['type'] = 'Treasures'
    
        # /!\ Here does not account for any other type of mana production (ie. Dark Ritual)
