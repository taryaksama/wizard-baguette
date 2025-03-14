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
        super().__init__(card)
        self.body_features = pd.Series({
            'power': None,      #int
            'toughness': None,  #int
            'evasion': [],      #List[str]
            'body_type': None,  #List[str]
            'condition': None   #List[str]
        })

    def is_evasive(self):
        EVASION_KEYWORDS = [
            "Flying",
            "Menace",
            "Trample"
        ]
        for keyword in EVASION_KEYWORDS:
            if keyword in self.card['keywords']:
                self.body_features['evasion'].append(keyword)
                return True
        
        # add unblockables ('can't be blocked')
    
        return False
    
    """
    def getBodyStats(self):
        def findTokenPowerToughness(text: str) -> Tuple[int, int]:
            pattern = r'creat(e|es).*?(\b(?:\d+|X)/(?:\d+|X)\b).*?creature token'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            
            if match:
                # Extract the power/toughness string (e.g., "2/2" or "X/3")
                power, toughness = match.group(2).split('/')
                
                # Convert to integer if possible, or return 0 if 'X' is found
                power_int = int(power) if power.isdigit() else 0
                toughness_int = int(toughness) if toughness.isdigit() else 0
                
                return power_int, toughness_int
            else:
                return 0, 0  # Return (0, 0) if no match is found
        
        # --- CASES ---
        ## - 1. Creature only -
        filter1 = (
            isType(card['types'], ['Creature']) 
            & (not createsToken(card['text'])) 
        )

        if filter1==True:
            bdType = 'Creature'
            bdManaValue = card['manaValue']
            bdPower = card['power']
            bdToughness = card['toughness']
        
        ## - 2. creature that creates a creature token on ETB -
        filter2 = (
            isType(card['types'], ['Creature']) 
            & createsToken(card['text']) 
            & isETB(card['text'])
        ) 
        
        if filter2==True:
            bdType = 'Creature with ETB creature token'
            bdManaValue = card['manaValue']

            p, t = findTokenPowerToughness(card['text'])
            bdPower = card['power'] + p
            bdToughness = card['toughness'] + t

        ## - 3. permanent that creates a creature token on ETB -
        filter3 = (
            isPermanent(card['types']) 
            & createsToken(card['text']) 
            & isETB(card['text'])
        ) 

        if filter3==True:
            bdType = 'Non-creature with ETB creature token'
            bdManaValue = card['manaValue']
            
            p, t = findTokenPowerToughness(card['text'])
            bdPower = card['power'] + p
            bdToughness = card['toughness'] + t

        ## - 4. instant / sorcery spell that creates a creature token -
        filter4 = (
            isType(card['types'], ['Instant', 'Sorcery']) 
            & createsToken(card['text']) 
        ) 

        if filter4==True:
            bdType = 'Non-permanent with creature token'
            bdManaValue = card['manaValue']
            
            p, t = findTokenPowerToughness(card['text'])
            bdPower = p
            bdToughness = t

        return bdType, bdManaValue, bdPower, bdToughness 
        """