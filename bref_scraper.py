'''
This module provides functions for scraping data from
baseballreference.com
'''

import logging
import re
import string
from datetime import datetime as datetime

import numpy
import pandas as pd
import urllib2
from bs4 import BeautifulSoup


def sub_spaces_for_non_ascii(some_string):
    '''
    :param some_string: string from which to strip non-ascii characters
    :return: some_string, but with non-ascii characters replaced with spaces
    '''
    # TODO: this is hacky. is there a better way to handle it?
    new_str = ''
    just_subbed_space = False
    for character in some_string:
        if character in string.printable:
            new_str += character
            just_subbed_space = False
        elif not just_subbed_space:
            new_str += ' '
            just_subbed_space = True
    return new_str


def get_game_logs(bref_id, start, end, is_batter):
    '''
    :param bref_id: str; baseball reference player ID
    :param start: datetime.datetime object; start date for desired
                  game logs
    :param start: datetime.datetime object; end date for desired game
                  logs
    :param is_batter: bool; if true, get hitting game logs, otherwise
                      get pitching game logs
    '''
    logging.debug('Scraping game logs for player with bref ID {id} '
                  'starting from the day of {start} and ending on the '
                  'the day of {end}'
                  .format(id=bref_id,
                          start=start,
                          end=end))
    # Make sure that the start year and the end year are the same
    # TODO: modify logic to accept ranges that span multiple years
    if start.year != end.year:
        raise ValueError('start and end dates must occur in the same year '
                         '(start year: {startyear}, end year: {endyear})'
                         .format(startyear=start.year, endyear=end.year))

    # Construcst URL, get the HTML
    if is_batter:
        bref_url = 'https://www.baseball-reference.com/players/gl.fcgi?id={bref_id}&t=b&year={year}'\
                   .format(bref_id=bref_id, year=start.year)
    else:
        bref_url = 'https://www.baseball-reference.com/players/gl.fcgi?id={bref_id}&t=p&year={year}'\
                   .format(bref_id=bref_id, year=start.year)
    logging.debug('baseball ref game log URL for player {bref_id} is {url}'
                  .format(bref_id=bref_id,url=bref_url))
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
    game_dicts_list = [game_dict for game_dict in game_dicts_list
                       if type(game_dict['Gcar']) in [float, int, numpy.float64] or game_dict['Gcar'].isdigit()]

    # remove entries that don't take place during desired time frame
    clean_game_dicts_list = list()
    for game_dict in game_dicts_list:

        # Probably a header row
        if type(game_dict['Date']) in [float, int, numpy.float64]:
            continue

        # Get date string
        # Handle weird format for days where doubleheaders were played: <date> (<game number>)
        # Also handle weird format for suspended games
        year = start.year
        game_date = sub_spaces_for_non_ascii(game_dict['Date'])
        doubleheader_match = re.search(r'([A-Za-z]+\s+\d+).*\((1|2)\)', game_date)
	suspended_match = re.search(r'([A-Za-z]+\s+\d+).*susp', game_date)
        if doubleheader_match:
            date_string = ' '.join([doubleheader_match.group(1).rstrip(), str(year)])
	elif suspended_match:
            date_string = ' '.join([suspended_match.group(1).rstrip(), str(year)])
        else:
            date_string = ' '.join([game_date, str(year)])

        # Outside of time interval of interest
        if start > datetime.strptime(date_string, '%b %d %Y'):
            continue
        elif end < datetime.strptime(date_string, '%b %d %Y'):
            continue
        else:
            clean_game_dicts_list.append(game_dict)
    game_dicts_list = clean_game_dicts_list

    return game_dicts_list
