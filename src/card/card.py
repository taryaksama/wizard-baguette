# src/card/card.py
# author: @taryaksama

"""
All code related to the class Card()
Defines the main properties of Magic: the Gathring printed card
"""

import pandas as pd
from typing import List, Dict

# Load all dependent features
from .mixin import *
from .body import *
from .interaction import *
from .manaprod import *

class Card(CardMixin):
    # Initialization
    def __init__(self, card: pd.Series) -> None:
        super().__init__(card)
        
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
   
def main() -> None:
    ...

if __name__=='___main__':
    main()