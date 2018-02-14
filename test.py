#!/usr/bin/env python

import logging
from datetime import datetime, timedelta
import bref_scraper
from lineup import Lineup


logging.basicConfig(level=logging.DEBUG)
hth_lineup = Lineup('lineup_cfg_file.json')
print hth_lineup
for player in hth_lineup:
    bref_scraper.get_game_logs(player.baseball_ref_id, datetime.now() - timedelta(days=365), datetime.now() - timedelta(days=365))
