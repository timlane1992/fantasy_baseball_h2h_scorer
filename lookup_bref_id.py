#!/usr/bin/env python3
'''
This script is used to find a player's baseball reference ID given his
name. If multiple names match the one provided, all of the
various alternatives are printed to stdout.
'''

import argparse
import os
import sys

import pandas as pd


def get_bref_id_for_player(name):
    '''
    :param name: str; name of player whose baseball ref id is desired
    :return: str; baseball ref id for specified player
    '''
    try:
        logging.debug('Baseball Ref ID for player {name} is {id}'
                      .format(name=name, id=baseball_ref_id))
        return baseball_ref_id
    except (IndexError, KeyError):
        logging.warn('Unable to find baseball reference ID for '
                     'player {}'
                     .format(name))
        raise


if __name__ == '__main__':

    # Get name of player whose ID to lookup
    parser = argparse.ArgumentParser(description='Get the baseball reference ID for a player based on his name')
    parser.add_argument('NAME')
    cl_args = parser.parse_args()

    # Read in data that maps names to baseball ref IDs
    data_file_path = os.path.join('data', 'player_id_map.csv')
    player_id_df = pd.read_csv(data_file_path, encoding='latin-1')

    # replace dashes with spaces in player's name, convert letters to lowercase
    mod_name = cl_args.NAME.lower().replace('-', ' ')

    # Figure out which entries have names that match
    bool_series = player_id_df['mlb_name'].apply(lambda x: x.lower()) == mod_name

    # If there were no matching entires, 
    if not any(bool_series):
        sys.exit('Unable to find baseball reference ID for name: {}'.format(cl_args.NAME))
    else:
        baseball_ref_ids = player_id_df[bool_series]['bref_id'].values
        print('Baseball reference IDs corresponding to players with the name: {}'.format(cl_args.NAME))
        for baseball_ref_id in baseball_ref_ids:
            print('    {}'.format(baseball_ref_id))
