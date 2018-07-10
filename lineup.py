'''
This module contains the implementation for the Lineup class
'''

from __future__ import print_function
import json
import os

from player import Player

class Lineup(object):
    '''
    This class provides an abstraction for a fantasy baseball H2H
    lineup. Valid lineups contain the following:
        * 1 C
        * 1 1B
        * 1 2B
        * 1 3B
        * 1 SS
        * 3 OFs
        * 1 DH
        * 2 SPs
        * 3 RPs
    '''
    def __init__(self, lineup_cfg_path):
        '''
        :param lineup_cfg_path: str; path to lineup config file
        '''
        if not os.path.isfile(lineup_cfg_path):
            raise ValueError('{} does not exist'.format(lineup_cfg_path))

        with open(lineup_cfg_path) as lineup_file:
            lineup_d = json.load(lineup_file)

        self.catcher = Player(lineup_d['c'])
        self.firstbase = Player(lineup_d['1b'])
        self.secondbase = Player(lineup_d['2b'])
        self.thirdbase = Player(lineup_d['3b'])
        self.shortstop = Player(lineup_d['ss'])
        self.outfielders = [Player(outfielder) for outfielder in lineup_d['of']]
        self.dh = Player(lineup_d['dh'])
        self.starting_pitchers = [Player(starter) for starter in lineup_d['sp']]
        self.relief_pitchers = [Player(reliever) for reliever in lineup_d['rp']]

        self.iterator_list = [
            self.catcher,
            self.firstbase,
            self.secondbase,
            self.thirdbase,
            self.shortstop,
            self.dh
        ]
        self.iterator_list.extend(self.outfielders)
        self.iterator_list.extend(self.starting_pitchers)
        self.iterator_list.extend(self.relief_pitchers)

        # Verify correct number of outfielders, starters, and relievers
        if len(self.starting_pitchers) != 2:
            raise ValueError('There are {num_starters} starting pitchers specified '
                             'in config file {cfg}, when there should be 2.'
                             .format(num_starters=len(self.starting_pitchers),
                                     cfg=lineup_cfg_path))
        if len(self.relief_pitchers) != 3:
            raise ValueError('There are {num_relievers} relievers specified '
                             'in config file {cfg}, when there should be 3.'
                             .format(num_relievers=len(self.relief_pitchers),
                                     cfg=lineup_cfg_path))
        if len(self.outfielders) != 3:
            raise ValueError('There are {num_outfielders} outfielders specified '
                             'in config file {cfg}, when there should be 3.'
                             .format(num_outfielders=len(self.outfielders),
                                     cfg=lineup_cfg_path))

    def __str__(self):
        '''
        :return: str; a "lineup card" of sorts
        '''
        return  'c  | {}\n'.format(self.catcher) +\
                '1b | {}\n'.format(self.firstbase) +\
                '2b | {}\n'.format(self.secondbase) +\
                '3b | {}\n'.format(self.thirdbase) +\
                'ss | {}\n'.format(self.shortstop) +\
                'of | {}\n'.format(self.outfielders[0]) +\
                'of | {}\n'.format(self.outfielders[1]) +\
                'of | {}\n'.format(self.outfielders[2]) +\
                'dh | {}\n'.format(self.dh) +\
                'sp | {}\n'.format(self.starting_pitchers[0]) +\
                'sp | {}\n'.format(self.starting_pitchers[1]) +\
                'rp | {}\n'.format(self.relief_pitchers[0]) +\
                'rp | {}\n'.format(self.relief_pitchers[1]) +\
                'rp | {}'.format(self.relief_pitchers[2])


    def __iter__(self):
        return self


    def next(self):
        if not self.iterator_list:
            raise StopIteration
        return self.iterator_list.pop(0)


    def get_hitters(self):
        '''
        Return a list containing the Player objects for all of the
        position players in the lineup.
        :return: list of Player objects
        '''
        return [
            self.catcher,
            self.firstbase,
            self.secondbase,
            self.thirdbase,
            self.shortstop,
            self.outfielders[0],
            self.outfielders[1],
            self.outfielders[2],
            self.dh
        ]


    def get_pitchers(self):
        '''
        Return a list containing the Player objects for all of the
        pitchers in the lineup
        :return: list of Player objects
        '''
        pitchers = list()
        pitchers.extend(self.starting_pitchers)
        pitchers.extend(self.relief_pitchers)
        return pitchers
