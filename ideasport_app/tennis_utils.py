def is_set_result_correct(player1, player2, third_set):
    if player1 == None and player2 == None:
        return True
    if player1 == None and (not player2 == None):
        return False
    if player2 == None and (not player1 == None):
        return False
    if player1 == 0 and player2 == 0:
        return True
    if player1 < 0 or player2 < 0:
        return False
    if third_set:
        if player1 == 10 and player2 <= 8:
            return True
        if player2 == 10 and player1 <= 8:
            return True
        if player1 > 10 and player1 == player2 + 2:
            return True
        if player2 > 10 and player2 == player1 + 2:
            return True
    else:
        if player1 == 6 and player2 <= 4:
            return True
        if player2 == 6 and player1 <= 4:
            return True
        if player1 == 7 and (player2 == 6 or player2 == 5):
            return True
        if player2 == 7 and (player1 == 6 or player1 == 5):
            return True
    return False

def who_win_set(player1, player2):
    if player1 == None and player2 == None:
        return 0
    if player1 == 0 and player2 == 0:
        return 0
    if player1 > player2:
        return 1
    if player2 > player1:
        return 2
    return 0

def compare_by_points_sets_gems(score1, score2):
    if score1['points'] > score2['points']:
        return 1
    if score2['points'] > score1['points']:
        return -1
    if score1['sets'] > score2['sets']:
        return 1
    if score2['sets'] > score1['sets']:
        return -1
    if score1['gems'] > score2['gems']:
        return 1
    if score2['gems'] > score1['gems']:
        return -1
    return 0
