# set_analyzer.py
# author: @taryaksama

# All the functions necessary to analyze a set of Magic the Gathering

import pandas as pd

def loadLimitedSet(allSets, set_code):
    """
    Loads and processes a set of Magic: The Gathering cards for limited play.

    This function extracts and cleans the card data from a given set, removing basic lands 
    and filtering only common and uncommon cards.

    Parameters:
    -----------
    allSets : pandas.DataFrame
        A DataFrame containing multiple sets of Magic: The Gathering cards.
    set_code : str
        The code of the set to be processed.

    Returns:
    --------
    pandas.DataFrame
        A cleaned DataFrame containing only common and uncommon cards with relevant features.

    Steps:
    ------
    1. Selects relevant card attributes such as name, mana cost, color identity, power, etc.
    2. Extracts the cards from the given set (`set_code`).
    3. Removes all basic lands by selecting only cards before the first occurrence of 'Plains'.
    4. Drops duplicate cards based on name and text.
    5. Converts numeric columns (`manaValue`, `power`, `toughness`) to proper numeric types.
    6. Filters the dataset to keep only common and uncommon cards.
    """
    
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
    #cards = df.loc[:allSets.loc[set_code]['baseSetSize']-1-5, features_analyzed] # remove the last 5 cards that are always basic lands
    n_firstPlains = df.loc[df['name']=='Plains'].first_valid_index()
    cards = df.loc[:n_firstPlains-1, features_analyzed]

    # Clean duplicates
    cards = cards.drop_duplicates(subset=['name','text'], keep='first')
    
    # Clean numeric data
    cards[['manaValue', 'power', 'toughness']] = cards[['manaValue', 'power', 'toughness']].apply(pd.to_numeric, errors='coerce')
    
    # Keep only common and uncommon cards
    cards = cards[cards['rarity'].isin(['common', 'uncommon'])]
    
    return cards

