# src/card/manaprod.py
# author: @taryaksama

"""
All code related to the class ManaProduction()
Calculates properties of cards that can produce mana with the following properties
- manaprod_type of producer
- manaprod_type, color and amount of mana produced
"""

import pandas as pd
import re
from typing import List, Dict

# Load configuration file
from .__config__ import MANA_COLORS

# Load all dependent features
from .mixin import *

class ManaProducerFeatures(CardMixin):
    def __init__(self, card:pd.Series):
        super().__init__(card)
        # self.card = card
        #self.effects = Effects(self.card['text'])
        self.manaprod_features = pd.Series({
            'manaprod_type': None,                   #List[str]
            'mana_produced': MANA_COLORS.copy(),   #Dict[str, int]
        })

    def producer_type(self) -> None:
        # Non-basic Lands
        if self.is_type(['Land']):
            self.manaprod_features['manaprod_type'] = 'Lands'

        # Dorks (that do not produces treasures)
        if (
            self.is_type(['Creature']) 
            and 'Treasure' not in self.card['keywords']
        ):
            self.manaprod_features['manaprod_type'] = 'Dorks'

        # Rocks (artifacts that are not creatures and do not produce treasures)
        if (
            self.is_type(['Artifact'])
            and (not self.is_manaprod_type(['Creature']))
            and 'Treasure' not in self.card['keywords']       
        ):
            self.manaprod_features['manaprod_type'] = 'Rocks'
        
        # Treasures
        if 'Treasure' in self.card['keywords']:
            self.manaprod_features['manaprod_type'] = 'Treasures'
    
        # /!\ Here does not account for any other manaprod_type of mana production (ie. Dark Ritual)

    def mana_produced(self) -> None:
        card_text = self.card['text']

        matches = re.findall(r'add\s*\{([^{}]+)\}', card_text)
        if matches:
            for mana_color in matches:
                if mana_color.isdigit():
                    mana_color = "C"  # Map numeric mana symbols to colorless mana
                if mana_color in self.manaprod_features['mana_produced']:
                    self.manaprod_features['mana_produced'][mana_color] += 1
        
        matches = re.findall(r"add (\d+|one|two|three|four|five) mana", card_text, re.IGNORECASE | re.DOTALL)
        if matches:
            try: 
                self.manaprod_features['mana_produced']["ALL"] = int(matches[0])
            except ValueError:
                WORD_TO_INT = {
                    'one': 1, 
                    'two': 2, 
                    'three': 3, 
                    'four': 4, 
                    'five': 5,
                    }
                self.manaprod_features['mana_produced']["ALL"] += WORD_TO_INT[matches[0]]