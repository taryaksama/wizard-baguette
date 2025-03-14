# src/card/card.py
# author: @taryaksama

"""
All code related to the class CardMixin()
Abstract class used to gather all common attributes and methods of child classes
"""

import pandas as pd
from typing import List, Dict

# Load configuration file
from .__config__ import FEATURES_ANALYZED, MANA_COLORS

# Load all dependent features
from .effects import *

class CardMixin():
    def __init__(self, card: pd.Series):
        self.card = card[FEATURES_ANALYZED]
        self.effects = Effects(self.card['text'])

    def is_type(self, typelist: List[str]) -> bool:
        return any(t in self.card['types'] for t in typelist)

    def is_permanent(self) -> bool:
        return self.is_type(['Land', 'Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Battle'])

    def is_multicolor(self) -> tuple[bool, dict]:
        ...

    def is_multipip(self) -> tuple[bool, int]: 
        ...

    def is_body(self) -> bool:
        return (
            # Filter 1 : is a creature
            (
                self.is_type(['Creature'])
            ) or
            # Filter 2 : creates creature tokens as ETB (for permanents)
            (
                self.is_permanent()
                and self.effects.is_ETB()
                and self.effects.creates_token()
            ) or
            # Filter 3 : creates creature token as instant or sorcery (for non-pemanents)
            (
                self.is_type(['Instant', 'Sorcery'])
                and self.effects.creates_token()
            )
        )
    
    def is_interaction(self) -> bool:
        return (
            self.effects.is_targeting() 
            and (
                self.effects.is_removal() or 
                self.effects.is_damage() or 
                self.effects.is_sacrifice() or 
                self.effects.is_counter() 
            )
        )
    
    def is_mana_producer(self) -> bool:
        return self.effects.produces_mana()