# src/utils.py
# author: @taryaksama

# All the functions necessary for analysis of Magic the Gathering cards and sets

import numpy as np
import pandas as pd
import re

def loadSet(allSets, set_code, restriction='all'):
    
    # Define cards features to be analyzed
    features_analyzed = [
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

    # Load cards
    df = pd.DataFrame.from_dict(allSets.loc[set_code]['cards'])

    if restriction=='all':
        cards = df

    def getBaseSet(d):
        n_firstPlains = d.loc[d['name']=='Plains'].first_valid_index()
        if n_firstPlains == None: # case when there is no basic land in set (commander sets, MAT, ...)
            cards = d.loc[:allSets.loc[set_code]['baseSetSize']-1, features_analyzed]
        else: c = d.loc[:n_firstPlains-1, features_analyzed]

        # Clean duplicates
        c = c.drop_duplicates(subset=['name','text'], keep='first')
    
        # Clean numeric data
        c[['manaValue', 'power', 'toughness']] = c[['manaValue', 'power', 'toughness']].apply(pd.to_numeric, errors='coerce')

        return c
        
    if restriction=='baseSet':
        cards = getBaseSet(df)

    if restriction=='limited':
        cards = getBaseSet(df)
        
        # Keep only common and uncommon cards
        cards = cards[cards['rarity'].isin(['common', 'uncommon'])]

    
        #n_firstPlains = df.loc[df['name']=='Plains'].first_valid_index()
        #if n_firstPlains == None: # case when there is no basic land in set (commander sets, MAT, ...)
        #    cards = df.loc[:allSets.loc[set_code]['baseSetSize']-1, features_analyzed]
        #else: cards = df.loc[:n_firstPlains-1, features_analyzed]

    # Clean duplicates
    #cards = cards.drop_duplicates(subset=['name','text'], keep='first')
    
    # Clean numeric data
    #cards[['manaValue', 'power', 'toughness']] = cards[['manaValue', 'power', 'toughness']].apply(pd.to_numeric, errors='coerce')
    
    # Keep only common and uncommon cards
    #cards = cards[cards['rarity'].isin(['common', 'uncommon'])]
    
    return cards