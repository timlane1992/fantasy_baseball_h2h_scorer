'''
This module houses the Player class
'''

import logging
import pandas as pd


player_id_df = pd.read_csv('player_id_map.csv')


def get_bref_id_for_player(name):
    '''
    :param name: str; name of player whose baseball ref id is desired
    :return: str; baseball ref id for specified player
    '''
    # replace dashes with spaces in player's name, convert letters to lowercase
    mod_name = name.lower().replace('-', ' ')
    bool_series = player_id_df['mlb_name'].apply(lambda x: x.lower()) == mod_name
    try:
        baseball_ref_id = player_id_df[bool_series]['bref_id'].values[0]  # TODO: handle errors better
        logging.debug('Baseball Ref ID for player {name} is {id}'
                      .format(name=name, id=baseball_ref_id))
        return baseball_ref_id
    except (IndexError, KeyError):
        logging.warn('Unable to find baseball reference ID for '
                     'player {}'
                     .format(name))
        raise


class Player(object):
    '''
    This class is primarily used to encapsulate operations that obtain
    a player's statistics
    '''
    def __init__(self, name):
        '''
        :param name: str; name of MLB player
        '''
        self.name = name
        self.baseball_ref_id = get_bref_id_for_player(name)


    def __str__(self):
        return self.name
