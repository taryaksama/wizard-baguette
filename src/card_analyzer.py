# src/card_analyzer.py
# author: @taryaksama

# All the functions necessary to analyze a card of Magic the Gathering
# Initial data should be a Pandas DataFrame extracted from the Card (Set) model of https://mtgjson.com/data-models/card/card-set/

import numpy as np
import pandas as pd
import re
from typing import List

class Effects():
    def __init__(self, card_text: str):
        self.card_text = card_text

    def creates_token(self) -> bool:
        pattern = r'creat(e|es) .*? creature token'
        return bool(re.search(pattern, self.card_text, re.IGNORECASE | re.DOTALL))
    
    def is_ETB(self) -> bool:
        pattern = r'when .*? ente(r|rs)'
        return bool(re.search(pattern, self.card_text, re.IGNORECASE | re.DOTALL))

class BodyFeatures():
    def __init__(self, card: pd.Series):
        self.card = card
        self.body_features = pd.Series({
            'power': None,      #int
            'toughness': None,  #int
            'evasion': None,    #List[str]
            'type': None,       #List[str]
            'condition': None   #List[str]
        })
    
class InteractionFeatures():
    ...

class ManaProductionFeatures():
    ...

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
    
    def activate_features(self) -> pd.Series:
        features = pd.Series()
        if self.is_body():
            body = Body()
            features['body'] = body.get_body_features()
        return features

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

"""
def isQuasiBody(cards: pd.DataFrame) -> None:
    # definition of a quasi-body : card that creates / becomes a body under certain conditions ('becomes a creature, ie. Crew'), should have identified power / toughness (for example, does not count recursion on targeted creatures)
# - when you pay a cost
# - creates tokens under conditions
    pass

def getBodyStats(card: pd.Series) -> Union[Tuple[str, int, int, int], None]:
    # pass the function it is not a body
    if not (isBody(card) | isQuasiBody(card)):
        print("Not a body")
        return None
        
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

# def isEvasive() #check if a card is evasive and returns a list of keywords

# def isMulticolor() #check if a card is multicolor, if yes, return the number and color of pips (beware of : / hybrid mana)

# def isInteraction #check if a card can interact with another + classify the type of interaction (hard removal, reversible/soft removal, stun, counter)

# ---FROM card_analyzer.py---
# isMultiPip()
# isManaProducer() ex- producesMana()


"""    

def main() -> None: # TBD
    ...

if __name__ == "__main__":
    main()