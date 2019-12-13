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
        if player2 == 6 and player2 <= 4:
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
