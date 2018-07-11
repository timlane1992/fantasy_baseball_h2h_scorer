#!/usr/bin/env python

import json
import os
import tempfile
import unittest
from datetime import datetime

import bref_scraper
import scorer
from lineup import Lineup

# Date format used for test data
DATE_FORMAT = '%m-%d-%Y'



class WeekOne2018TestCase(unittest.TestCase):
    def setUp(self):
        self.lineup_file = None
        self.start_date = None
        self.end_date = None
        self.exp_hit_score = None
        self.exp_pitch_score = None
        self.exp_total_score = None

        # Load in test data
        test_data = None
        with open(os.path.join('test_lineups/2018_week_1_test_data.json')) as test_data_file:
            test_data = json.load(test_data_file)

        # Create file containing lineup JSON data
        self.lineup_file = tempfile.NamedTemporaryFile('w', delete=False)
        json.dump(test_data['lineup'], self.lineup_file)
        self.lineup_file.close()

        # Get start/end dates and expected scores
        self.start_date = datetime.strptime(test_data['start_date'], DATE_FORMAT)
        self.end_date = datetime.strptime(test_data['end_date'], DATE_FORMAT)
        self.exp_hit_score = test_data['expected_hitters_score']
        self.exp_pitch_score = test_data['expected_pitchers_score']
        self.exp_total_score = self.exp_hit_score + self.exp_pitch_score


    def test_scoring(self):

        # Load H2H lineup
        hth_lineup = Lineup(self.lineup_file.name)
        hitters = hth_lineup.get_hitters()
        pitchers = hth_lineup.get_pitchers()

        # Get game logs for every player in the lineup
        game_log_holder = dict()
        for player in hth_lineup:
            game_log_holder[player.baseball_ref_id] = bref_scraper.get_game_logs(player.baseball_ref_id,
                                                                                 self.start_date,
                                                                                 self.end_date,
                                                                                 player in hitters)

        # Get h2h scores for hitters
        hitter_sum = 0
        for hitter in hitters:
            game_log_list = game_log_holder[hitter.baseball_ref_id]
            score = scorer.get_hitter_score(game_log_list)
            hitter_sum += score

        # Get h2h scores for pitchers
        pitcher_sum = 0
        for pitcher in pitchers:
            game_log_list = game_log_holder[pitcher.baseball_ref_id]
            score = scorer.get_pitcher_score(game_log_list)
            pitcher_sum += score

        self.assertEqual(self.exp_hit_score, hitter_sum)
        self.assertEqual(self.exp_pitch_score, pitcher_sum)
        self.assertEqual(self.exp_total_score, pitcher_sum + hitter_sum)


    def tearDown(self):
        os.unlink(self.lineup_file.name)


class WeekTwo2018TestCase(unittest.TestCase):
    def setUp(self):
        self.lineup_file = None
        self.start_date = None
        self.end_date = None
        self.exp_hit_score = None
        self.exp_pitch_score = None
        self.exp_total_score = None

        # Load in test data
        test_data = None
        with open(os.path.join('test_lineups/2018_week_2_test_data.json')) as test_data_file:
            test_data = json.load(test_data_file)

        # Create file containing lineup JSON data
        self.lineup_file = tempfile.NamedTemporaryFile('w', delete=False)
        json.dump(test_data['lineup'], self.lineup_file)
        self.lineup_file.close()

        # Get start/end dates and expected scores
        self.start_date = datetime.strptime(test_data['start_date'], DATE_FORMAT)
        self.end_date = datetime.strptime(test_data['end_date'], DATE_FORMAT)
        self.exp_hit_score = test_data['expected_hitters_score']
        self.exp_pitch_score = test_data['expected_pitchers_score']
        self.exp_total_score = self.exp_hit_score + self.exp_pitch_score


    def test_scoring(self):

        # Load H2H lineup
        hth_lineup = Lineup(self.lineup_file.name)
        hitters = hth_lineup.get_hitters()
        pitchers = hth_lineup.get_pitchers()

        # Get game logs for every player in the lineup
        game_log_holder = dict()
        for player in hth_lineup:
            game_log_holder[player.baseball_ref_id] = bref_scraper.get_game_logs(player.baseball_ref_id,
                                                                                 self.start_date,
                                                                                 self.end_date,
                                                                                 player in hitters)

        # Get h2h scores for hitters
        hitter_sum = 0
        for hitter in hitters:
            game_log_list = game_log_holder[hitter.baseball_ref_id]
            score = scorer.get_hitter_score(game_log_list)
            hitter_sum += score

        # Get h2h scores for pitchers
        pitcher_sum = 0
        for pitcher in pitchers:
            game_log_list = game_log_holder[pitcher.baseball_ref_id]
            score = scorer.get_pitcher_score(game_log_list)
            pitcher_sum += score

        self.assertEqual(self.exp_hit_score, hitter_sum)
        self.assertEqual(self.exp_pitch_score, pitcher_sum)
        self.assertEqual(self.exp_total_score, pitcher_sum + hitter_sum)


    def tearDown(self):
        os.unlink(self.lineup_file.name)


class WeekThree2018TestCase(unittest.TestCase):
    def setUp(self):
        self.lineup_file = None
        self.start_date = None
        self.end_date = None
        self.exp_hit_score = None
        self.exp_pitch_score = None
        self.exp_total_score = None

        # Load in test data
        test_data = None
        with open(os.path.join('test_lineups/2018_week_3_test_data.json')) as test_data_file:
            test_data = json.load(test_data_file)

        # Create file containing lineup JSON data
        self.lineup_file = tempfile.NamedTemporaryFile('w', delete=False)
        json.dump(test_data['lineup'], self.lineup_file)
        self.lineup_file.close()

        # Get start/end dates and expected scores
        self.start_date = datetime.strptime(test_data['start_date'], DATE_FORMAT)
        self.end_date = datetime.strptime(test_data['end_date'], DATE_FORMAT)
        self.exp_hit_score = test_data['expected_hitters_score']
        self.exp_pitch_score = test_data['expected_pitchers_score']
        self.exp_total_score = self.exp_hit_score + self.exp_pitch_score


    def test_scoring(self):

        # Load H2H lineup
        hth_lineup = Lineup(self.lineup_file.name)
        hitters = hth_lineup.get_hitters()
        pitchers = hth_lineup.get_pitchers()

        # Get game logs for every player in the lineup
        game_log_holder = dict()
        for player in hth_lineup:
            game_log_holder[player.baseball_ref_id] = bref_scraper.get_game_logs(player.baseball_ref_id,
                                                                                 self.start_date,
                                                                                 self.end_date,
                                                                                 player in hitters)

        # Get h2h scores for hitters
        hitter_sum = 0
        for hitter in hitters:
            game_log_list = game_log_holder[hitter.baseball_ref_id]
            score = scorer.get_hitter_score(game_log_list)
            hitter_sum += score

        # Get h2h scores for pitchers
        pitcher_sum = 0
        for pitcher in pitchers:
            game_log_list = game_log_holder[pitcher.baseball_ref_id]
            score = scorer.get_pitcher_score(game_log_list)
            pitcher_sum += score

        self.assertEqual(self.exp_hit_score, hitter_sum)
        self.assertEqual(self.exp_pitch_score, pitcher_sum)
        self.assertEqual(self.exp_total_score, pitcher_sum + hitter_sum)


    def tearDown(self):
        os.unlink(self.lineup_file.name)


class WeekFour2018TestCase(unittest.TestCase):
    def setUp(self):
        self.lineup_file = None
        self.start_date = None
        self.end_date = None
        self.exp_hit_score = None
        self.exp_pitch_score = None
        self.exp_total_score = None

        # Load in test data
        test_data = None
        with open(os.path.join('test_lineups/2018_week_3_test_data.json')) as test_data_file:
            test_data = json.load(test_data_file)

        # Create file containing lineup JSON data
        self.lineup_file = tempfile.NamedTemporaryFile('w', delete=False)
        json.dump(test_data['lineup'], self.lineup_file)
        self.lineup_file.close()

        # Get start/end dates and expected scores
        self.start_date = datetime.strptime(test_data['start_date'], DATE_FORMAT)
        self.end_date = datetime.strptime(test_data['end_date'], DATE_FORMAT)
        self.exp_hit_score = test_data['expected_hitters_score']
        self.exp_pitch_score = test_data['expected_pitchers_score']
        self.exp_total_score = self.exp_hit_score + self.exp_pitch_score


    def test_scoring(self):

        # Load H2H lineup
        hth_lineup = Lineup(self.lineup_file.name)
        hitters = hth_lineup.get_hitters()
        pitchers = hth_lineup.get_pitchers()

        # Get game logs for every player in the lineup
        game_log_holder = dict()
        for player in hth_lineup:
            game_log_holder[player.baseball_ref_id] = bref_scraper.get_game_logs(player.baseball_ref_id,
                                                                                 self.start_date,
                                                                                 self.end_date,
                                                                                 player in hitters)

        # Get h2h scores for hitters
        hitter_sum = 0
        for hitter in hitters:
            game_log_list = game_log_holder[hitter.baseball_ref_id]
            score = scorer.get_hitter_score(game_log_list)
            hitter_sum += score

        # Get h2h scores for pitchers
        pitcher_sum = 0
        for pitcher in pitchers:
            game_log_list = game_log_holder[pitcher.baseball_ref_id]
            score = scorer.get_pitcher_score(game_log_list)
            pitcher_sum += score

        self.assertEqual(self.exp_hit_score, hitter_sum)
        self.assertEqual(self.exp_pitch_score, pitcher_sum)
        self.assertEqual(self.exp_total_score, pitcher_sum + hitter_sum)


    def tearDown(self):
        os.unlink(self.lineup_file.name)


class WeekFive2018TestCase(unittest.TestCase):
    def setUp(self):
        self.lineup_file = None
        self.start_date = None
        self.end_date = None
        self.exp_hit_score = None
        self.exp_pitch_score = None
        self.exp_total_score = None

        # Load in test data
        test_data = None
        with open(os.path.join('test_lineups/2018_week_5_test_data.json')) as test_data_file:
            test_data = json.load(test_data_file)

        # Create file containing lineup JSON data
        self.lineup_file = tempfile.NamedTemporaryFile('w', delete=False)
        json.dump(test_data['lineup'], self.lineup_file)
        self.lineup_file.close()

        # Get start/end dates and expected scores
        self.start_date = datetime.strptime(test_data['start_date'], DATE_FORMAT)
        self.end_date = datetime.strptime(test_data['end_date'], DATE_FORMAT)
        self.exp_hit_score = test_data['expected_hitters_score']
        self.exp_pitch_score = test_data['expected_pitchers_score']
        self.exp_total_score = self.exp_hit_score + self.exp_pitch_score


    def test_scoring(self):

        # Load H2H lineup
        hth_lineup = Lineup(self.lineup_file.name)
        hitters = hth_lineup.get_hitters()
        pitchers = hth_lineup.get_pitchers()

        # Get game logs for every player in the lineup
        game_log_holder = dict()
        for player in hth_lineup:
            game_log_holder[player.baseball_ref_id] = bref_scraper.get_game_logs(player.baseball_ref_id,
                                                                                 self.start_date,
                                                                                 self.end_date,
                                                                                 player in hitters)

        # Get h2h scores for hitters
        hitter_sum = 0
        for hitter in hitters:
            game_log_list = game_log_holder[hitter.baseball_ref_id]
            score = scorer.get_hitter_score(game_log_list)
            hitter_sum += score

        # Get h2h scores for pitchers
        pitcher_sum = 0
        for pitcher in pitchers:
            game_log_list = game_log_holder[pitcher.baseball_ref_id]
            score = scorer.get_pitcher_score(game_log_list)
            pitcher_sum += score

        self.assertEqual(self.exp_hit_score, hitter_sum)
        self.assertEqual(self.exp_pitch_score, pitcher_sum)
        self.assertEqual(self.exp_total_score, pitcher_sum + hitter_sum)


    def tearDown(self):
        os.unlink(self.lineup_file.name)


class WeekSix2018TestCase(unittest.TestCase):
    def setUp(self):
        self.lineup_file = None
        self.start_date = None
        self.end_date = None
        self.exp_hit_score = None
        self.exp_pitch_score = None
        self.exp_total_score = None

        # Load in test data
        test_data = None
        with open(os.path.join('test_lineups/2018_week_6_test_data.json')) as test_data_file:
            test_data = json.load(test_data_file)

        # Create file containing lineup JSON data
        self.lineup_file = tempfile.NamedTemporaryFile('w', delete=False)
        json.dump(test_data['lineup'], self.lineup_file)
        self.lineup_file.close()

        # Get start/end dates and expected scores
        self.start_date = datetime.strptime(test_data['start_date'], DATE_FORMAT)
        self.end_date = datetime.strptime(test_data['end_date'], DATE_FORMAT)
        self.exp_hit_score = test_data['expected_hitters_score']
        self.exp_pitch_score = test_data['expected_pitchers_score']
        self.exp_total_score = self.exp_hit_score + self.exp_pitch_score


    def test_scoring(self):

        # Load H2H lineup
        hth_lineup = Lineup(self.lineup_file.name)
        hitters = hth_lineup.get_hitters()
        pitchers = hth_lineup.get_pitchers()

        # Get game logs for every player in the lineup
        game_log_holder = dict()
        for player in hth_lineup:
            game_log_holder[player.baseball_ref_id] = bref_scraper.get_game_logs(player.baseball_ref_id,
                                                                                 self.start_date,
                                                                                 self.end_date,
                                                                                 player in hitters)

        # Get h2h scores for hitters
        hitter_sum = 0
        for hitter in hitters:
            game_log_list = game_log_holder[hitter.baseball_ref_id]
            score = scorer.get_hitter_score(game_log_list)
            hitter_sum += score

        # Get h2h scores for pitchers
        pitcher_sum = 0
        for pitcher in pitchers:
            game_log_list = game_log_holder[pitcher.baseball_ref_id]
            score = scorer.get_pitcher_score(game_log_list)
            pitcher_sum += score

        self.assertEqual(self.exp_hit_score, hitter_sum)
        self.assertEqual(self.exp_pitch_score, pitcher_sum)
        self.assertEqual(self.exp_total_score, pitcher_sum + hitter_sum)


    def tearDown(self):
        os.unlink(self.lineup_file.name)


if __name__ == '__main__':
    unittest.main()
