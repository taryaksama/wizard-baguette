# src/card/card.py
# author: @taryaksama

"""
All code related to the class Card()
Defines the main properties of Magic: the Gathring printed card
"""

import pandas as pd
from typing import List, Dict

# Load configuration file
from .__config__ import FEATURES_ANALYZED

# Load all dependent features
from .effects import *
from .body import *
from .interaction import *
from .manaprod import *

class CardMixin():
    def is_type(self, typelist: List[str]) -> bool:
        return any(t in self.card['types'] for t in typelist)

    def is_permanent(self) -> bool:
        return self.is_type(['Land', 'Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Battle'])

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

class Card(CardMixin):
    # Initialization
    def __init__(self, card: pd.Series) -> None:
        self.card = card[FEATURES_ANALYZED]
        self.effects = Effects(self.card['text'])

        # Composed features
        if self.is_body():
            self.body = BodyFeatures(self.card)
        if self.is_interaction():
            self.interaction = InteractionFeatures(self.card)
        if self.is_mana_producer():
            self.manaprod = ManaProducerFeatures(self.card)

    # Dunder and general methods
    def __repr__(self) -> str:
        return f"Card({self.card})"
    
    def show(self) -> pd.Series:
        return self.card
    
    #    details = self.card.copy()
    #    for feature_series in self.features.values():
    #        details = pd.concat([details, feature_series])
    #    return details
   
def main() -> None:
    ...

if __name__=='___main__':
    main()