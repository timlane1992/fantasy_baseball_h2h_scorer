'''
This module provides functions for scraping data from
baseballreference.com
'''

import numpy
import pandas as pd
import urllib2
from bs4 import BeautifulSoup

def get_game_logs(bref_id, start, end):
    '''
    :param bref_id: str; baseball reference player ID
    :param start: datetime.datetime object; start date for desired
                  game logs
    :param start: datetime.datetime object; end date for desired game
                  logs
    '''
    # Make sure that the start year and the end year are the same
    # TODO: modify logic to accept ranges that span multiple years
    if start.year != end.year:
        raise ValueError('start and end dates must occur in the same year '
                         '(start year: {startyear}, end year: {endyear})'
                         .format(startyear=start.year, endyear=end.year))

    # Get the HTML
    bref_url = 'https://www.baseball-reference.com/players/gl.fcgi?id={bref_id}&t=b&year={year}'\
               .format(bref_id=bref_id, year=start.year)
    print bref_url
    page = urllib2.urlopen(bref_url)
    soup = BeautifulSoup(page, 'html.parser')

    # Get the game logs table
    def is_parseable_table(tag):
        if not tag.has_attr('class'):
            return False
        return tag.name == 'table' and 'stats_table' in tag['class'] and 'sortable' in tag['class']
    try:
        table = soup.find_all(is_parseable_table)[0]
    except IndexError:
        raise RuntimeError('Unable to find game log table for player '
                           'with bref ID: {}'.format(bref_id))

    # Use pandas to turn html string into dataframe, then to dict
    try:
        gamelogs_dict = pd.read_html(str(table))[0].to_dict()
    except IndexError:
        raise RuntimeError('Unable to turn extracted html table into '
                           'dataframe for player with bref ID {}'
                           .format(bref_id))

    # Verify that every field in the game logs is of the same length
    num_game_logs = len(gamelogs_dict[gamelogs_dict.keys()[0]])
    for field in gamelogs_dict:
        if len(gamelogs_dict[field]) != num_game_logs:
            raise RuntimeError('Uneven number of data points in game logs columns')

    # Make dict for each game represented in logs
    game_dicts_list = list()
    for index in xrange(num_game_logs):
        game_dicts_list.append({field: gamelogs_dict[field][index] for field in gamelogs_dict})

    # remove 'label row' entries
    # identified by the number of walks column not being a digit
    game_dicts_list = [game_dict for game_dict in game_dicts_list if type(game_dict['Gcar']) not in [float, int, numpy.float64] and game_dict['Gcar'].isdigit()]

    return game_dicts_list
