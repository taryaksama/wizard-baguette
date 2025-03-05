# src/card/descriptor.py
# author: @taryaksama

"""
All code related to the class Descriptor()
Calculates advanced properties of a Magic: the Gathring printed card, those
that are not explicitly on the card
- permanent
- is a body or generate a body
- is an interaction
"""

import pandas as pd
import re
from typing import List

# Load all dependent features
from .effects import *
from .body import *

class Descriptor():
    def __init__(self, card:pd.Series):
        self.card = card
        self.effects = Effects(self.card['text'])

    def is_type(self, typelist: List[str]) -> bool:
        return any(t in self.card['types'] for t in typelist)

    def is_permanent(self) -> bool:
        return self.is_type(['Land', 'Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Battle'])

    def is_body(self) -> bool:
        return (
            # Filter 1 : is a creature
            (
                self.is_type(['Creature'])
            ) |
            # Filter 2 : creates creature tokens as ETB (for permanents)
            (
                self.is_permanent()
                & self.effects.is_ETB()
                & self.effects.creates_token()
            ) |
            # Filter 3 : creates creature token as instant or sorcery (for non-pemanents)
            (
                self.is_type(['Instant', 'Sorcery'])
                & self.effects.creates_token()
            )
        )
    
    def is_interaction(self) -> bool:
        return (
            self.effects.is_targeting() 
            & (
                self.effects.is_removal() | 
                self.effects.is_damage() | 
                self.effects.is_sacrifice() | 
                self.effects.is_counter() 
            )
        )
    
    def activate_features(self) -> pd.Series:
        features = pd.Series()
        if self.is_body():
            body = Body()
            features['body'] = body.get_body_features()
        return features
    
def main():
    ...

if __name__ == '__main__':
    main()