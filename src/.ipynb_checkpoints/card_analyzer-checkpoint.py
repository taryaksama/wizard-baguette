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

# def isEvasive() #check if a card is evasive and returns a list of keywords

# def isMulticolor() #check if a card is multicolor, if yes, return the number and color of pips (beware of phyrexian / hybrid mana)

# def isInteraction #check if a card can interact with another + classify the type of interaction (hard removal, reversible/soft removal, stun, counter)

# ---FROM card_analyzer.py---
# isMultiPip()
# isManaProducer() ex- producesMana()

