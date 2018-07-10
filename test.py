#!/usr/bin/env python

import logging
import sys
from datetime import datetime, timedelta

import bref_scraper
import scorer
from lineup import Lineup


# Set beginning and end times
DATE_FORMAT = '%m-%d-%Y'
START_DATE = datetime.strptime('04-30-2018', DATE_FORMAT)
END_DATE = datetime.strptime('05-06-2018', DATE_FORMAT)

# Load head-to-head lineup
logging.basicConfig(level=logging.DEBUG)
hth_lineup = Lineup('lineup_cfg_file.json')
hitters = hth_lineup.get_hitters()
pitchers = hth_lineup.get_pitchers()
print hth_lineup

# Get game logs for every player in the lineup
game_log_holder = dict()
for player in hth_lineup:
    game_log_holder[player.baseball_ref_id] = bref_scraper.get_game_logs(player.baseball_ref_id,
                                                                         START_DATE,
                                                                         END_DATE,
                                                                         player in hitters)

# Get h2h scores for hitters
hitter_sum = 0
print '-' * 30, 'HITTER SCORES', '-' * 30
for hitter in hitters:
    game_log_list = game_log_holder[hitter.baseball_ref_id]
    score = scorer.get_hitter_score(game_log_list)
    print 'Hitter: {player}, score: {score}'.format(player=hitter, score=score)
    hitter_sum += score
print 'TOTAL SCORE - HITTERS:', hitter_sum

# Get h2h scores for pitchers
pitcher_sum = 0
print '-' * 30, 'PITCHER SCORES', '-' * 30
for pitcher in pitchers:
    game_log_list = game_log_holder[pitcher.baseball_ref_id]
    score = scorer.get_pitcher_score(game_log_list)
    print 'Pitcher: {player}, score: {score}'.format(player=pitcher, score=score)
    pitcher_sum += score
print 'TOTAL SCORE - PITCHERS:', pitcher_sum
print 'TOTAL SCORE - ALL:', pitcher_sum + hitter_sum
