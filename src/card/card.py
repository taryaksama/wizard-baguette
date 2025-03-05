# src/card/card.py
# author: @taryaksama

"""
All code related to the class Card()
Defines the main properties of Magic: the Gathring printed card
"""

import pandas as pd

# Load all dependent features
from .descriptor import *
from .effects import *
from .body import *
from .interaction import *

class Card():
    def __init__(self, card: pd.Series) -> None:
        # Define cards features to be analyzed
        FEATURES_ANALYZED = [
            'name',
            'keywords',
            'manaValue',
            'manaCost',
            'colorIdentity',
            'power',
            'toughness',
            'rarity',
            'types',
            'text']
        self.card = card[FEATURES_ANALYZED]
        self.descriptor = Descriptor(card)

    def __repr__(self) -> str:
        return f"Card({self.card})"
    
    def show(self) -> pd.Series:
        return self.card
    
    def show_details(self) -> pd.Series:
        details = self.card.copy()
        for feature_series in self.features.values():
            details = pd.concat([details, feature_series])
        return details
    
def main() -> None:
    ...

if __name__=='___main__':
    main()