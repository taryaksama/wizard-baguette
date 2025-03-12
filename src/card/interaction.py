# src/card/interaction.py
# author: @taryaksama

"""
All code related to the class InteractionFeatures()
Describes the interaction effects of a of Magic: the Gathring printed card
"""

import pandas as pd

from .card import *

class InteractionFeatures(CardMixin):
    def __init__(self, card: pd.Series):
        self.card = card
