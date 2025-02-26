# src/utils.py
# author: @taryaksama

# All the functions necessary for analysis of Magic the Gathering cards and sets

import numpy as np
import pandas as pd
import re

def load_card():
    ...

def load_set(
        set_card_list:pd.DataFrame,
        set_code: str, 
        restriction='all'
        ) -> pd.DataFrame:
    
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

    # Load cards
    df = pd.DataFrame.from_dict(set_card_list.loc[set_code]['cards'])

    if restriction=='all':
        cards = df

    def get_base_set(d):
        # Remove card numbers after the first basic Land (a Plains)
        n_firstPlains = d.loc[d['name']=='Plains'].first_valid_index()
        if n_firstPlains == None: # case when there is no basic land in set (commander sets, MAT, ...)
            cards = d.loc[:set_card_list.loc[set_code]['baseSetSize']-1, FEATURES_ANALYZED]
        else: c = d.loc[:n_firstPlains-1, FEATURES_ANALYZED]

        # Clean duplicates
        c = c.drop_duplicates(subset=['name','text'], keep='first')
    
        # Clean numeric data
        c[['manaValue', 'power', 'toughness']] = c[['manaValue', 'power', 'toughness']].apply(pd.to_numeric, errors='coerce').fillna(0)

        return c
        
    if restriction=='base_set':
        cards = get_base_set(df)

    if restriction=='limited': # Keep only common and uncommon cards
        cards = get_base_set(df)
        cards = cards[cards['rarity'].isin(['common', 'uncommon'])]

    return cards