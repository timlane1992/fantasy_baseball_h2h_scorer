#!/usr/bin/env python
from __future__ import print_function
import json
import logging
import os
import tempfile
from datetime import datetime

import scorer
from lineup import Lineup


DATE_FORMAT = '%m-%d-%Y'
#logging.basicConfig(level=logging.DEBUG)


def generate_report(data_path):
    try:
        lineup_only_file = tempfile.NamedTemporaryFile('w', delete=False)

        lineup_data = None
        with open(data_path) as lineup_data_file:
            lineup_data = json.load(lineup_data_file)

        # Get start date and end date
        start_date = datetime.strptime(lineup_data['start_date'], DATE_FORMAT)
        end_date = datetime.strptime(lineup_data['end_date'], DATE_FORMAT)

        # Dump actual lineup data to separate file because that's what Lineup.__init__ wants
        json.dump(lineup_data['lineup'], lineup_only_file)
        lineup_only_file.close()
        hth_lineup = Lineup(lineup_only_file.name)

        # Generate report
        print('##########  Generating report for team: {}'.format(lineup_data['team_name']))
        scorer.generate_lineup_report(hth_lineup, start_date, end_date)

    finally:
        os.unlink(lineup_only_file.name)


def main():
        my_team_path = '2018_week_19_lineup.json'
        oppponent_team_path = '2018_week_19_opponent_lineup.json'
        generate_report(my_team_path)
        generate_report(oppponent_team_path)


if __name__ == '__main__':
    main()
