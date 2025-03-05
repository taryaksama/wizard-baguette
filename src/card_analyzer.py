# src/card_analyzer.py
# author: @taryaksama

# All the functions necessary to analyze a card of Magic the Gathering
# Initial data should be a Pandas DataFrame extracted from the Card (Set) model of https://mtgjson.com/data-models/card/card-set/

import numpy as np
import pandas as pd
import re
from typing import List

class ManaProductionFeatures():
    ...

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