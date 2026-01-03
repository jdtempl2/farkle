import random
import time
import statistics

__version__ = "0.1.1"


def stringIsANumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"    


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


def endTurnOrRoll(ptype, first_roll, round_score):
    # Will return an empty string to indicate ROLL, or 'x' to indicate END TURN
    # Human players will simply use an input()
    # Computer players will have more rules
    #   ptype       - player type (human or otherwise)
    #   first_roll  - bool of whether it's the very first roll in a turn or not

    choice = 'x'

    if first_roll:
        choice = ''

    elif ptype == 'man':
        if first_roll:
            input('Press ENTER to roll die: ')
        else:
            # Player can choose to end their turn after they roll
            return input('Press ENTER to roll die, or \'x\' to end turn: ')

    elif ptype =='dumbAss':
        # dumbAss always quits after the first roll...
        if not first_roll:
            choice = 'x'

    # highRolla will always roll until he either busts or has some high number of points (1000+)
    elif ptype == 'highRolla':
        points_to_get = 1000  # amount of points that highRolla wants in one round
        if round_score >= points_to_get:
            choice = 'x'
        else:
            choice = ''

    return choice


def getHighestScoringOption(scores):
    point_vals = [scores[s][0] for s in scores]  # get List of points from the score dict
    highest_point_val = max(point_vals)
    choice = 0  # initialize

    # probably not the most elegant way to do this...
    # find the score[] index that matches the highest point val
    for s in scores:
        if highest_point_val in scores[s]:
            choice = s
    return choice


def chooseScoreToTake(ptype, scores, round_score, took_points):

    # Human player gets to pick what option to take
    if ptype == 'man':
        choice = ''
        while not (stringIsANumber(choice) or choice == 'x'):
            choice = input('Select one score to take, or press \'x\' to pass: ')
        return choice

    # dumbAss will take the highest available score ONCE, then cede their turn
    elif ptype == 'dumbAss':
        if took_points is False:
            return getHighestScoringOption(scores)
        else:
            return 'x'

    # highRolla will always roll until he either busts or has some high number of points (1000+)
    elif ptype == 'highRolla':
        if len(scores) > 0:
            return getHighestScoringOption(scores)
        else:
            return 'x'

    return 0


def playTurn(ptype, sleep_time=3, show_print=True):
    # This function plays one turn of Farkle. It sets up 6 dice, rolls them, and lets the player pick which dice to
    # use for scoring. Then the remaining dice can be rerolled. If there's a bust, the turn ends with 0 points scored.
    # Function returns the points scored for this turn.
    # p_type is a string representing the type of Player.
    # Will support either 'man', 'dumbAss', 'highRolla', or 'playItSafe'

    dice = [0 for d in range(6)]  # create 6 dice
    round_score = 0
    did_bust = False
    first_roll = True

    while True:
        # Check if the player wants to end their turn or roll the die
        end_turn = endTurnOrRoll(ptype, first_roll, round_score) == 'x'

        if first_roll:
            first_roll = False

        if not ptype == 'man' and end_turn:
            if show_print:
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

        if show_print:
            print('ROLLING THE DICE! ')

        turn_is_over = False
        took_points = False

        while not turn_is_over:
            # Show the dice rolled
            if show_print:
                print(f'Dice remaining:\n{dice}')

            # Get the list of scoring dice
            scores = scoreDice(dice)

            # Determine if there's a BUST!
            if len(scores) == 0:
                if not took_points:
                    if show_print:
                        print(f'{Color.RED}\nBUST!\n{Color.RESET}')
                    return 0
                else:  # have already taken points from this roll, and there's no more scores to take
                    turn_is_over = True

            # Otherwise points are able to be taken
            else:
                if show_print:
                    printScore(scores)  # print the available scores in a nice format

                # case where there's only one option right off the roll, so user HAS to take it
                if took_points is False and len(scores) == 1:
                    if ptype == 'man':
                        choice = ''
                        while choice != '0':
                            choice = input('Select \'0\' since it\'s the only score: ')
                    choice = 0
                else:
                    # case where there are multiple options for points
                    choice = chooseScoreToTake(ptype, scores, round_score, took_points)

                # Report what action the computer took, if needed
                if not ptype == 'man' and show_print:
                    if choice == 'x':
                        print(f'{ptype} is taking no more points...')
                    else:
                        print(f'{ptype} is selecting {choice} for {scores[choice][0]} points')
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
                    if show_print:
                        print(f'Score = {round_score}')


class Player:
    def __init__(self, name, ptype):
        self.name = name
        self.type = ptype
        self.points = 0
        self.victories = 0
                    
                    
def playGame(p1, p2, score_to_win):
    
    if not p1.type == 'man' and not p2.type == 'man':
        turn_delay = 0  # computers play FAST against each other
        show_print = False
    else:
        turn_delay = 3
        show_print = True

    p1.points = 0
    p2.points = 0

    player_1s_turn = bool(random.getrandbits(1))

    if show_print:
        while True:
            if player_1s_turn:
                print(f'{Color.GREEN}{p1.name}\'s Turn{Color.RESET}')
                p1.points += playTurn(p1.type, turn_delay, show_print)
                print(f'{Color.GREEN}{p1.name} SCORE = {p1.points}{Color.RESET}')
                print(f'{Color.BLUE}{p2.name} SCORE = {p2.points}{Color.RESET}')
                if p1.points >= score_to_win:
                    print(f'{p1.name} WINS')
                    p1.victories += 1
                    return p1.name
            else:
                print(f'{Color.BLUE}{p2.name}\'s Turn{Color.RESET}')
                p2.points += playTurn(p2.type, turn_delay, show_print)
                print(f'{Color.BLUE}{p2.name} SCORE = {p2.points}{Color.RESET}')
                print(f'{Color.GREEN}{p1.name} SCORE = {p1.points}{Color.RESET}')
                if p2.points >= score_to_win:
                    print(f'{p2.name} WINS')
                    p2.victories += 1
                    return p2.name
            player_1s_turn = not player_1s_turn
    else:
        while True:
            if player_1s_turn:
                p1.points += playTurn(p1.type, turn_delay, show_print)
                if p1.points >= score_to_win:
                    p1.victories += 1
                    return p1.name
            else:
                p2.points += playTurn(p2.type, turn_delay, show_print)
                if p2.points >= score_to_win:
                    p2.victories += 1
                    return p2.name
            player_1s_turn = not player_1s_turn


def main():
    print('Farkle!')

    default_score_thresh = 5000
    default_num_games = 10

    print('COMPUTER PLAYERS ARE')
    print('1. dumbAss (easy)')
    print('2. highRolla (med)')
    print('3. playItSafe (???)')

    print('\nEnter COMPUTER player name to play against \'AI\'')
    print('Enter HUMAN name to play against MAN')

    p1name = input('Enter name for PLAYER 1: ')
    p2name = input('Enter name for PLAYER 2: ')

    if p1name == '':
        p1name = 'highRolla'
    if p2name == '':
        p2name = 'dumbAss'

    computer_names = ['dumbAss', 'highRolla', 'playItSafe']

    if p1name not in computer_names:
        p1type = 'man'
    else:
        p1type = p1name

    if p2name not in computer_names:
        p2type = 'man'
    else:
        p2type = p2name

    play_again = True
    while play_again:

        score_threshold_str = input(f'Enter score to play to (leave blank for {default_score_thresh}): ')
        if score_threshold_str == '':
            score_threshold = default_score_thresh
        else:
            score_threshold = int(score_threshold_str)

        num_games_str = input(f'Enter # games to play (leave blank for {default_num_games}): ')
        if num_games_str == '':
            num_games = default_num_games
        else:
            num_games = int(num_games_str)

        player1 = Player(p1name, p1type)
        player2 = Player(p2name, p2type)

        players = [player1, player2]

        player1_points = []
        player2_points = []

        for n in range(num_games):
            playGame(player1, player2, score_threshold)
            player1_points.append(player1.points)
            player2_points.append(player2.points)

        # print the stats
        print('NUMBER OF WINS:')
        for p in players:
            print(f'{p.name}:\t\t{p.victories}')

        if num_games > 1:
            # calculate the stats
            avg1 = statistics.mean(player1_points)
            med1 = statistics.median(player1_points)
            dev1 = statistics.stdev(player1_points)
            avg2 = statistics.mean(player2_points)
            med2 = statistics.median(player2_points)
            dev2 = statistics.stdev(player2_points)

            print(f'POINTS\tAVG\t\t\tMED\t\t\tSTD DEV')
            print(f'P1:\t\t{avg1:.1f}\t\t{med1:.0f}\t\t{dev1:.1f}')
            print(f'P2:\t\t{avg2:.1f}\t\t{med2:.0f}\t\t{dev2:.1f}')

        play_again = input('Press ENTER to play again, \'x\' to quit: ') != 'x'

if __name__ == '__main__':
    main()