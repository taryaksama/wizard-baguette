# src/card/manaprod.py.py
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
from .effects import *

class ManaProducer():
    def __init__(self, card: pd.Series):
        self.card = card
        self.manaprod_features = pd.Series({
            'type': None,           #List[str]
            'mana_produced': None,  #Dict[str, int]
        })