# src/card_analyzer.py
# author: @taryaksama

# All the functions necessary to analyze a card of Magic the Gathering
# Initial data should be a Pandas DataFrame extracted from the Card (Set) model of https://mtgjson.com/data-models/card/card-set/

import numpy as np
import pandas as pd
import re

#check if a card is or can be a body that impact the board state
# def isBody(cards):
# what is a body ? (pure body)
# - Creatures
# - cards that creates creatures token immediatly
# - cards that put creatures on the battlefield **without any conditions**
# 
# definition of a quasi-body : card that creates / becomes a body under certain conditions ('becomes a creature, ie. Crew'), should have identified power / toughness (for example, does not count recursion on targeted creatures)
# - when you pay a cost
# - creates tokens under conditions


# Filtering functions @dev, s should be a Pandas Series

## Bodies
def isType(s, typelist):
    return any(t in s for t in typelist)

def isPermanent(s):
    return isType(s, ['Land', 'Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Battle'])

def isBody(cards):

    # Filter 1 : is a creature
    # .apply(isType, args(,'Creature'))
    # type of body = creature

    # Filter 2 : creates creature tokens as ETB (for permanents)
    # isPermanent x isETB x createsToken
    # type of body = ETB token

    # Filter 3 : creates creature token as instant or sorcery (for non-pemanents)
    # ~isPermanent x createsToken
    # type of body = non-permanent spell token

def isQuasiBody(cards):
    # Filter 1 : becomes a body when you pay a cost ('becomes')
    # return the cost of becoming a body
    
    # Filter 2 : creates token under certain conditions (LTB (when/whenever dies), attacks, === 'whenever')
    
    # Filter 3 : put another body card on the battlefield (example : Manifest, Cascade, Discover, recursion, etc)
    # putOnBF
    pass

# Effects

def createsToken(s):
    pattern = r'creat(e|es) .*? creature token'
    return bool(re.search(pattern, s, re.IGNORECASE | re.DOTALL))

def isETB(s):
    pattern = r'when .*? ente(r|rs)'
    return bool(re.search(pattern, s, re.IGNORECASE | re.DOTALL))

# def isLTB
# def putOnBF



# getBodyStats(cards)
    # isBody
    # if type == 
    # returns effManaValue, effPower, effToughness
    



# def isEvasive() #check if a card is evasive and returns a list of keywords

# def isMulticolor() #check if a card is multicolor, if yes, return the number and color of pips (beware of : / hybrid mana)

# def isInteraction #check if a card can interact with another + classify the type of interaction (hard removal, reversible/soft removal, stun, counter)

# ---FROM card_analyzer.py---
# isMultiPip()
# isManaProducer() ex- producesMana()

