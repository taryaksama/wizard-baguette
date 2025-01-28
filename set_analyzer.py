# set_analyzer.py
# author: @taryaksama

# All the functions necessary to analyze a set of Magic the Gathering

import numpy as np
import pandas as pd
import re

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

def analyzeSetSpeed(cards):
    """
    Analyzes the speed of a Magic: The Gathering set by focusing on creature cards.

    This function calculates key metrics related to the creatures in the set, such as:
    - Ratio of creatures in the set.
    - Average (mean) creature mana value.
    - Average (mean) power-to-mana value for creatures.

    The speed of a set can be characterized by several metrics, including:
    - **Ratio of creatures**: Percentage of creature cards in the set.
    - **Creature Mana Value**: The average mana value of creatures, which indicates how expensive creatures are to cast.
    - **Power to Mana Value**: The average ratio of a creature's power compared to its mana value. A higher ratio suggests creatures hit hard relative to their cost.

    Parameters:
    -----------
    cards : pandas.DataFrame
        A DataFrame containing Magic: The Gathering card data with columns such as 'types', 'manaValue', 'power', etc.

    Returns:
    --------
    tuple:
        - `limitedCreatureRatio` (float): Percentage of creature cards in the set.
        - `meanCreatureMV` (float): The average mana value of creatures.
        - `meanPowerToMV` (float): The average power-to-mana value ratio for creatures.

    Example:
    --------
    limitedCreatureRatio, meanCreatureMV, meanPowerToMV = analyzeSetSpeed(cards)
    """

    # Filter for 'Creature' only
    cardsCreatureFiltered = cards[cards['types'].apply(lambda x: 'Creature' in x)].copy()
    
    # Ratio of creatures
    limitedCreatureRatio = (len(cardsCreatureFiltered) / len(cards)) * 100  # in percentage
    
    # Creature Mana Value
    meanCreatureMV = cardsCreatureFiltered['manaValue'].mean()

    # Creature Power to ManaValue
    cardsCreatureFiltered['powerToManaValue'] = cardsCreatureFiltered['power'] / cardsCreatureFiltered['manaValue']
    meanPowerToMV = cardsCreatureFiltered['powerToManaValue'].mean()

    # Normalization
    #cardsCreatureFiltered = cardsCreatureFiltered.copy()    
    #cardsCreatureFiltered['normalizedCreatureManaValue'] = cardsCreatureFiltered['manaValue'] - meanCreatureMV # normalized columns
    #cardsCreatureFiltered['normalizedPowerToManaValue'] = cardsCreatureFiltered['power'] - meanPowerToMV # normalized columns

    return limitedCreatureRatio, meanCreatureMV, meanPowerToMV

def analyzeSetBoardState(cards):
    """
    Analyzes the board state of a Magic: The Gathering set by focusing on creature cards.

    This function calculates key metrics related to the creatures in the set, such as:
    - Mean creature power.
    - Mean creature toughness.
    - Mean power-to-toughness ratio.
    - Counts of keywords, particularly evasive keywords like 'Flying', 'Trample', and 'Menace'.

    The board state of a set can be characterized by:
    - **Mean Creature Power**: The average power of creatures, which indicates how much damage creatures can deal.
    - **Mean Creature Toughness**: The average toughness of creatures, which indicates how resistant they are to damage.
    - **Power-to-Toughness Ratio**: The average ratio of a creature's power to its toughness. A ratio above 1 suggests creatures that are likely to hit harder but defend poorly.
    - **Evasive Creatures**: The number of creatures with evasive keywords like 'Flying', 'Trample', and 'Menace', which are typically harder to block or deal with.

    Parameters:
    -----------
    cards : pandas.DataFrame
        A DataFrame containing Magic: The Gathering card data with columns such as 'types', 'power', 'toughness', 'keywords', etc.

    Returns:
    --------
    tuple:
        - `meanCreaturePower` (float): The average power of creatures.
        - `meanCreatureToughness` (float): The average toughness of creatures.
        - `meanPowerToToughness` (float): The average power-to-toughness ratio.
        - `KWCount` (dict): A dictionary of keyword counts for creature cards.
        - `evasiveKWCount` (dict): A dictionary of counts for evasive keywords ('Flying', 'Trample', 'Menace').

    Example:
    --------
    meanCreaturePower, meanCreatureToughness, meanPowerToToughness, KWCount, evasiveKWCount = analyzeSetBoardState(cards)
    """

    # Filter for 'Creature' only
    cardsCreatureFiltered = cards[cards['types'].apply(lambda x: 'Creature' in x)].copy()

    # Creature Power
    meanCreaturePower = cardsCreatureFiltered['power'].mean()

    # Creature Toughness
    meanCreatureToughness = cardsCreatureFiltered['toughness'].mean()
    
    # Creature Power to Toughness
    cardsCreatureFiltered['powerToToughness'] = cardsCreatureFiltered['power'] / cardsCreatureFiltered['toughness']
    meanPowerToToughness = cardsCreatureFiltered['powerToToughness'].mean()

    # Normalization
    #cardsCreatureFiltered['normalizedCreaturePower'] = cardsCreatureFiltered['power'] - meanCreaturePower
    #cardsCreatureFiltered['normalizedCreatureToughness'] = cardsCreatureFiltered['toughness'] - meanCreatureToughness
    #cardsCreatureFiltered['normalizedPowerToToughness'] = cardsCreatureFiltered['power'] - meanPowerToToughness  
    
    # Evasion
    def countKeywords(_cards):
        unique_keywords = list(_cards['keywords'].explode().unique())
        unique_keywords.remove(np.nan)
        exploded_data = _cards.explode('keywords')
        filtered_data = exploded_data[exploded_data['keywords'].isin(unique_keywords)]
        KW_count = exploded_data['keywords'].value_counts().to_dict()
        return KW_count
    
    KWCount = countKeywords(cardsCreatureFiltered)
    
    def countEvasiveKeywords(keyword_dict, keyword_list):
        evasiveCount = [keyword_dict[key] for key in keyword_list]
        return evasiveCount
    
    evasiveKW = ['Flying', 'Trample', 'Menace'] # @dev, could be set as an argument of the function
    evasiveKWCount = dict(zip(evasiveKW, countEvasiveKeywords(KWCount, evasiveKW)))

    # @dev, can be added a ratio of evasive creature

    return meanCreaturePower, meanCreatureToughness, meanPowerToToughness, KWCount, evasiveKWCount

def analyzeSetFixing(cards):
    """
    Analyzes the color fixing and mana production aspects of a Magic: The Gathering set.

    This function calculates several key metrics related to how well the set provides color fixing and mana generation:
    - Monocolor-to-multicolor ratio (lands excluded).
    - Multi-pip ratio: the ratio of cards with more than one colored pip in their mana cost.
    - Ratio of mana producers and the types of mana producers (lands, dorks, rocks, treasures).
    - The types of mana producers, categorized into specific types like lands, creatures (dorks), artifacts (rocks), and treasure-generating cards.

    The fixing aspects of a set can be characterized by:
    1. **Monocolor-to-Multicolor Ratio**: The proportion of multicolor cards (cards with more than one color identity) to monocolor cards, excluding lands.
    2. **Multi-pip Ratio**: The proportion of cards whose mana cost includes more than one colored mana symbol (i.e., "multi-pip" cards).
    3. **Mana Producer Ratio**: The proportion of cards that produce mana, including lands and various types of mana producers.
    4. **Types of Mana Producers**: Categorizing mana producers into:
        - **Lands**: Cards that are lands and produce mana.
        - **Dorks**: Creature cards that produce mana (but are not treasures).
        - **Rocks**: Artifact cards that produce mana (but are not creatures and do not produce treasures).
        - **Treasures**: Cards that create treasure tokens, which can be sacrificied for mana.

    Parameters:
    -----------
    cards : pandas.DataFrame
        A DataFrame containing Magic: The Gathering card data, with columns such as 'types', 'colorIdentity', 'manaCost', 'text', 'keywords', etc.

    Returns:
    --------
    tuple:
        - `monocolorToMulticolorRatio` (float): The ratio of monocolor to multicolor non-land cards, in percentage.
        - `multiPipRatio` (float): The ratio of cards with multi-colored pips in their mana cost, in percentage.
        - `manaProducerRatio` (float): The ratio of cards that produce mana, in percentage.
        - `nonLand_manaProducerRatio` (float): The ratio of non-land cards that produce mana, in percentage.
        - `manaProducerTypes` (dict): A dictionary detailing the counts of different types of mana producers: 'Lands', 'Dorks', 'Rocks', and 'Treasures'.

    Example:
    --------
    monocolorToMulticolorRatio, multiPipRatio, manaProducerRatio, nonLand_manaProducerRatio, manaProducerTypes = analyzeSetFixing(cards)
    """

    
    # Monocolor to multicolor ratio
    non_land_cards_total = len(cards[(cards['types'].apply(lambda x: 'Land' not in x))])
    multicolor_nonland_cards = len(
        cards[
            (cards['types'].apply(lambda x: 'Land' not in x)) 
            & (cards['colorIdentity'].apply(len) > 1)
        ])
    monocolorToMulticolorRatio = (multicolor_nonland_cards / non_land_cards_total) * 100
    
    # Multi-pip ratio
    def isMultiPip(s, letters_to_remove=None):
        """
        This function checks whether a card's mana cost contains more than one colored pip 
        (i.e., multiple colored mana symbols). It removes specified characters (such as `{`, `}`, `C`, `X`, and digits) 
        from the mana cost string to focus on the colored mana symbols. If the resulting string length is greater than 1, 
        it is considered a "multi-pip" mana cost.

        Parameters:
        - s: A string representing the card's mana cost.
        - letters_to_remove: A list of characters to remove from the mana cost string. Defaults to ['{', '}', 'C', 'X'].

        Returns:
        - True if the mana cost has more than one colored pip.
        - False otherwise.
        """
  
        if letters_to_remove is None:
            letters_to_remove = ['{', '}', 'C', 'X']  # Assign default list safely
    
        if not isinstance(s, str):  # Handle NaN or non-string values
            return False
        
        s = ''.join(c for c in s if c not in letters_to_remove and not c.isdigit())
        return len(s) > 1
    
    multiPipRatio = (len(cards[cards['manaCost'].apply(isMultiPip)]) / non_land_cards_total) * 100
    
    # Mana producers
    def producesMana(s): #@dev TO BE TESTED FOR FETCH
        """
        This function checks if a card has text indicating it produces mana. It looks for specific phrases such as 
        "add X mana" or "add {" to identify cards that produce mana. The function uses regular expressions to detect 
        the presence of these patterns in the card's text.

        Parameters:
        - s: A string representing the card's text description (specifically, its ability text).

        Returns:
        - True if the card produces mana, based on the specified patterns.
        - False otherwise.
        """
        if not isinstance(s, str):
            s = ""
        
        pattern1 = r'add (?:\d+|one|two|three|four|five) mana'
        match1 = re.search(pattern1, s, re.IGNORECASE)
    
        pattern2 = r'add {'
        match2 = re.search(pattern2, s, re.IGNORECASE)
        
        return bool(match1 or match2)
    
    # Ratio of mana producers
    n_manaProducer = len(cards[cards['text'].apply(producesMana)])
    n_nonLand_manaProducer = len(
        cards[
            cards['text'].apply(producesMana) 
            & (cards['types'].apply(lambda x: 'Land' not in x))
        ])
    manaProducerRatio = (n_manaProducer / len(cards)) * 100
    nonLand_manaProducerRatio = (n_nonLand_manaProducer / len(cards)) *100
    
    # Type of producer
    def countManaProducerTypes(data):
        """
        This function categorizes cards that produce mana into different types based on their characteristics:
        - Lands: Cards that are land types.
        - Dorks: Creature cards that produce mana but are not treasure-producing.
        - Rocks: Artifact cards that produce mana but are not creatures or treasure-generating.
        - Treasures: Cards that create treasure tokens.

        The function counts the number of cards in each category and returns the counts in a dictionary.

        Parameters:
        - data: A DataFrame containing cards that produce mana (filtered by the producesMana function).

        Returns:
        - A dictionary with the counts of different types of mana producers: 
          {'Lands': count, 'Dorks': count, 'Rocks': count, 'Treasures': count}.
        """
        
        df = data[data['text'].apply(producesMana)]
    
        # Non-basic Lands
        a = len(df[
                df['types'].apply(lambda x: 'Land' in str(x))
                ]) 
        # Dorks (that do not produces treasures)
        b = len(df[
                df['types'].apply(lambda x: 'Creature' in str(x)) 
                & df['keywords'].apply(lambda x: 'Treasure' not in str(x))
                ]) 
        # Rocks (artifacts that are not creatures and do not produce treasures)
        c = len(df[
                df['types'].apply(lambda x: 'Artifact' in str(x)) 
                & df['types'].apply(lambda x: 'Creature' not in str(x)) 
                & df['keywords'].apply(lambda x: 'Treasure' not in str(x))
                ]) 
        # Treasures
        d = len(df[
                df['keywords'].apply(lambda x: 'Treasure' in str(x))
                ])
    
        # here does not account for any other type of mana production (ie. Dark Ritual)
    
        producer_type = {
            'Lands': a,
            'Dorks': b,
            'Rocks': c,
            'Treasures': d
        }
        return producer_type
    
    manaProducerTypes = countManaProducerTypes(cards)
    
    # Type of mana produced
    # @dev, TBD in the future

    return monocolorToMulticolorRatio, multiPipRatio, manaProducerRatio, nonLand_manaProducerRatio, manaProducerTypes