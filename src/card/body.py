# src/card/body.py
# author: @taryaksama

"""
All code related to the class BodyFeatures()
Defines the main properties of what constitutes a body in a Magic: the Gathring printed card
- power
- toughness
- if there is evasion on the card
- what type of body it is : creature, token, permanent that becomes a body under certain conditions, instant/sorcery spell that generate a body
- condition : the condition of obtention of the body
"""

import pandas as pd

# Load all dependent features
from .mixin import *

class BodyFeatures(CardMixin):
    def __init__(self, card: pd.Series):
        # self.card = card
        super().__init__(card)
        self.body_features = pd.Series({
            'power': None,      #int
            'toughness': None,  #int
            'evasion': None,    #List[str]
            'body_type': None,  #List[str]
            'condition': None   #List[str]
        })