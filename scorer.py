import re

# TODO: allow user to specify scoring formula via some external configuration?
# TODO: combine hitter and pitcher scoring functions if possible?


def get_hitter_score(game_logs):
    '''
    :param game_logs:
    :return: int; score calculated from game log data
    '''
    num_stolen_bases = 0
    num_bb_or_hp = 0
    num_singles = 0
    num_doubles = 0
    num_triples = 0
    num_hrs = 0
    num_outs = 0
    num_cs = 0

    for game_log in game_logs:
        num_stolen_bases += int(game_log['SB'])
        num_bb_or_hp += int(game_log['HBP'])
        num_bb_or_hp += int(game_log['BB'])
        num_singles += int(game_log['H']) - int(game_log['2B']) - int(game_log['3B']) - int(game_log['HR'])
        num_doubles += int(game_log['2B'])
        num_triples += int(game_log['3B'])
        num_hrs += int(game_log['HR'])
        num_outs += int(game_log['AB']) - int(game_log['H'])
        num_cs += int(game_log['CS'])

    # Could probably replace this block with a function supplied by the user
    final_score = 0
    final_score += num_stolen_bases
    final_score += 2 * num_bb_or_hp
    final_score += 3 * num_singles
    final_score += 4 * num_doubles
    final_score += 5 * num_triples
    final_score += 6 * num_hrs
    final_score -= num_outs
    final_score -= 2 * num_cs

    return final_score


def get_pitcher_score(game_logs):
    '''
    :param game_logs:
    :return: int; score calculated from game log data
    '''
    num_outs = 0
    num_wins = 0
    num_saves = 0
    num_game_finishes = 0
    num_bb_or_hbp = 0
    num_hits = 0
    num_hrs_allowed = 0
    num_losses = 0

    for game_log in game_logs:

        # If a pitcher finished a game, the 'Inngs' field will have a
        # trailing '-GF'
        if type(game_log['Inngs']) != str:
            pass  # Just to make sure there's no type errors
        elif re.search(r'-GF(\(\d+\))?$', game_log['Inngs']):
            num_game_finishes += 1

        # Getting number of outs requires parsing IP field
        innings_pitched_fields = str(game_log['IP']).split('.')
        num_outs += 3 * int(innings_pitched_fields[0])
        num_outs += int(innings_pitched_fields[1])

        # 'Dec' field tells us if the pitcher won, lost, or got a save
        if type(game_log['Dec']) != str:
            pass  # No-decision
        elif re.search(r'^W', game_log['Dec']):
            num_wins += 1
        elif re.search(r'^L', game_log['Dec']):
            num_losses += 1
        elif re.search(r'^S', game_log['Dec']):
            num_saves += 1

        num_bb_or_hbp += int(game_log['BB'])
        num_bb_or_hbp += int(game_log['HBP'])
        num_hrs_allowed += int(game_log['HR'])
        num_hits += int(game_log['H'])

    # Get number of full innings and number of "remaining outs"
    num_full_innings = num_outs // 3
    remaining_outs = num_outs % 3

    final_score = 0
    final_score += (4 * num_full_innings) + remaining_outs
    final_score += 3 * num_wins
    final_score += 2 * num_saves
    final_score += num_game_finishes
    final_score -= num_bb_or_hbp
    final_score -= 2 * num_hits
    final_score -= 3 * num_hrs_allowed
    final_score -= 4 * num_losses

    return final_score
