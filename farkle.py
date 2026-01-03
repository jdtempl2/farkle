import random
import time


def addScore(score_dict, points, dice):
    score_dict[len(score_dict)] = [points, dice]
    return score_dict


def scoreDice(dice):
    #  this function will take an arbitrary list of Dice values and return a Dictionary of possible scores
    #  dict will take the form of 'scores[idx] = [points, [list_of_dice]]'
    #  so a roll of [1, 1, 2, 5, 5, 6] will return {0: [100, [1]], 1: [200, [1, 1]], 2: [50, [5]], 3: [100, [5, 5]]}

    num_dice = len(dice)
    values = [0, 0, 0, 0, 0, 0]  # number of ones, twos, threes, etc
    scores = {}  # will store list of scores & their associated die

    # count the number of 1s, 2s, 3s, etc
    for d in range(num_dice):
        val = dice[d] - 1  # since val is an index, and indices start at 0
        values[val] += 1
    # print(values)

    no_multiples = True  # check for multiples of three or more
    if max(values) >= 3:
        no_multiples = False

    # no score if no 1s, 5s, or 3+ multiples
    if values[0] == 0 and values[4] == 0 and no_multiples is True:
        return {}

    # Scoring for runs, either 1,2,3,4,5, 2,3,4,5,6, or 1,2,3,4,5,6
    if values[0] > 0 and values[1] > 0 and values[2] > 0 and values[3] > 0 and values[4] > 0:
        addScore(scores, 750, [1, 2, 3, 4, 5])
    if values[1] > 0 and values[2] > 0 and values[3] > 0 and values[4] > 0 and values[5] > 0:
        addScore(scores, 750, [2, 3, 4, 5, 6])
    if len(scores) == 2:  # IE if both runs are present
        addScore(scores, 1500, [1, 2, 3, 4, 5, 6])

    for i in range(6):
        d = i + 1  # the number on the dice (add one since index starts at 0)
        val = values[i]  # the number of dice with that value

        # Scoring conditions if '1's are rolled
        if d == 1:
            if val >= 1:
                addScore(scores, 100, [d])
            if val >= 2:
                addScore(scores, 200, [d, d])
            if val >= 3:
                addScore(scores, 1000, [d, d, d])
            if val >= 4:
                addScore(scores, 2000, [d, d, d, d])
            if val >= 5:
                addScore(scores, 4000, [d, d, d, d, d])
            if val == 6:
                addScore(scores, 8000, [d, d, d, d, d, d])

        # Scoring conditions if one or two '5's are rolled
        elif d == 5 and val < 3:
            if val >= 1:
                addScore(scores, 50, [d])
            if val >= 2:
                addScore(scores, 100, [d, d])

        # Scoring conditions for all other combos
        else:
            if val >= 3:
                addScore(scores, d*100, [d, d, d])
            if val >= 4:
                addScore(scores, d*200, [d, d, d, d])
            if val >= 5:
                addScore(scores, d*400, [d, d, d, d, d])
            if val == 6:
                addScore(scores, d*800, [d, d, d, d, d, d])

    return scores


def printScore(scores):
    # function to nicely print the dictionary of scores returned by scoreDice
    # Choice    Score   Dice Used
    # 0         100     [1]
    # 1         200     [1, 1]
    # 2         50      [5]
    s = 'Choice\tScore\tDice Used\n'
    for x in scores:
        points = scores[x][0]
        dice = scores[x][1]
        if points > 999:
            s += f'{x}\t\t{points}\t{dice}\n'
        else:
            s += f'{x}\t\t{points}\t\t{dice}\n'
    print(s)


def endTurnOrRoll(ptype, first_roll):
    # Will return an empty string to indicate ROLL, or 'x' to indicate END TURN
    # Human players will simply use an input()
    # Computer players will have more rules
    #   ptype       - player type (human or otherwise)
    #   first_roll  - bool of whether it's the very first roll in a turn or not

    if ptype == 'man':
        if first_roll:
            return input('Press ENTER to roll die: ')
        else:
            # Player can choose to end their turn after they roll
            return input('Press ENTER to roll die, or \'x\' to end turn: ')

    elif ptype =='dumbAss':
        # dumbAss always quits after the first roll...
        if not first_roll:
            return 'x'
        else:
            return ''
    return '???'  # deliberately weird string to catch missed cases


def playTurn(ptype, sleep_time=3):
    # This function plays one turn of Farkle. It sets up 6 dice, rolls them, and lets the player pick which dice to
    # use for scoring. Then the remaining dice can be rerolled. If there's a bust, the turn ends with 0 points scored.
    # Function returns the points scored for this turn.
    # p_type is a string representing the type of Player.
    # Will support either 'man', 'dumbAss', 'allIn', or 'playItSafe'

    dice = [0 for d in range(6)]  # create 6 dice
    round_score = 0
    did_bust = False
    first_roll = True

    while True:
        # Check if the player wants to end their turn or roll the die
        end_turn = endTurnOrRoll(ptype, first_roll) == 'x'

        if first_roll:
            first_roll = False

        if not ptype == 'man' and end_turn:
            print(f'{ptype} is ending their turn...')
            time.sleep(sleep_time)

        # User chose to end the round
        if end_turn:
            return round_score

        # User got NO points on their roll & busted
        if did_bust:
            return 0

        else:
            if len(dice) == 0:  # covers case where all dice are used for score, and player gets to roll again
                num_dice = 6  # reset to using 6 dice
            else:
                num_dice = len(dice)  # only roll remaining dice

        # roll the dice & sort ascending (not needed but looks nice)
        dice = [random.randrange(1, 7) for d in range(num_dice)]
        dice.sort()

        turn_is_over = False
        took_points = False

        while not turn_is_over:
            # Show the dice rolled
            print(f'Dice remaining:\n{dice}')

            # Get the list of scoring dice
            scores = scoreDice(dice)

            # Determine if there's a BUST!
            if len(scores) == 0:
                if took_points is False:
                    print('BUST!')
                    return 0
                else:  # have already taken points from this roll, and there's no more scores to take
                    turn_is_over = True

            # Otherwise points are able to be taken
            else:
                printScore(scores)  # print the available scores in a nice format

                choice = 0  # choice of dice combo to take, or to skip turn

                # case where there's only one option right off the roll, so user HAS to take it
                if took_points is False and len(scores) == 1:
                    if ptype == 'man':
                        input('Selecting \'0\' since it\'s the only score (ENTER to continue) ')
                    else:  # computer doesn't have to enter input
                        print('Selecting \'0\' since it\'s the only score')
                        time.sleep(sleep_time)

                # case where there are multiple options for points
                else:
                    # Human player gets to pick what option to take
                    if ptype == 'man':
                        choice = input('Select one score to take, or press \'x\' to pass: ')

                    # dumbAss will take the highest available score ONCE, then cede their turn
                    elif ptype == 'dumbAss':
                        if took_points is False:
                            # find out which score is highest
                            point_vals = [scores[s][0] for s in scores]  # get list of points from the score dict
                            highest_point_val = max(point_vals)
                            choice = 0

                            # probably not the most elegant way to do this...
                            # find the score[] index that matches the highest point val
                            for s in scores:
                                if highest_point_val in scores[s]:
                                    choice = s
                            print(f'{ptype} is selecting {choice} for {highest_point_val} points')
                        else:
                            print(f'{ptype} is taking no more points...')
                            choice = 'x'
                        time.sleep(sleep_time)

                if choice == 'x':
                    turn_is_over = True

                # Player has picked a scoring option
                else:
                    took_points = True
                    score = scores[int(choice)]  # get the score info from the choice selected
                    # score = [number_of_points, [die_1, die_2, ..., die_N]]
                    points = score[0]  # the number of points for that score
                    die = score[1]  # the dice used to make those points\

                    # take the scoring dice out of play
                    for d in die:
                        dice.remove(d)

                    # Add the scoring points to the running round total
                    round_score += points
                    print(f'Score = {round_score}')


def main():
    print('Farkle!')

    score_threshold_str = input('Enter score to play to (leave blank for 5000): ')
    if score_threshold_str == '':
        score_threshold = 5000
    else:
        score_threshold = int(score_threshold_str)

    print('COMPUTER PLAYERS ARE')
    print('1. dumbAss (easy)')
    print('2. allIn (med)')
    print('3. playItSafe (???)')

    print('\nEnter COMPUTER player name to play against \'AI\'')
    print('Enter HUMAN name to play against MAN')

    p1name = input('Enter name for PLAYER 1: ')
    p2name = input('Enter name for PLAYER 2: ')

    if p1name == '':
        p1name = 'Player 1'
    if p2name == '':
        p2name = 'dumbAss'

    computer_names = ['dumbAss', 'allIn', 'playItSafe']

    if p1name not in computer_names:
        p1type = 'man'
    else:
        p1type = p1name

    if p2name not in computer_names:
        p2type = 'man'
    else:
        p2type = p2name

    if not p1type == 'man' and not p2type == 'man':
        turn_delay = 0  # computers play FAST against each other
    else:
        turn_delay = 3

    player_1_score = 0
    player_2_score = 0

    player_1s_turn = bool(random.getrandbits(1))

    while True:
        if player_1s_turn:
            print(f'{p1name}\'s Turn')
            player_1_score += playTurn(p1type, turn_delay)
            print(f'{p1name} SCORE = {player_1_score}')
            print(f'{p2name} SCORE = {player_2_score}')
            if player_1_score >= score_threshold:
                print(f'{p1name} WINS')
                return
        else:
            print(f'{p2name}\'s Turn')
            player_2_score += playTurn(p2type, turn_delay)
            print(f'{p2name} SCORE = {player_2_score}')
            print(f'{p1name} SCORE = {player_1_score}')
            if player_2_score >= score_threshold:
                print(f'{p2name} WINS')
                return

        player_1s_turn = not player_1s_turn


if __name__ == '__main__':
    main()