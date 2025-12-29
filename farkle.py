import random


def scoreDice(dice):
    #  this function will take an arbitrary list of Dice values and return a Dictionary of possible scores
    #  dict will take the form of 'scores[idx] = [points, [list_of_dice]]'
    #  so a roll of [1, 1, 2, 5, 5, 6] will return {0: [100, [1]], 1: [200, [1, 1]], 2: [50, [5]], 3: [100, [5, 5]]}

    num_dice = len(dice)
    values = [0, 0, 0, 0, 0, 0]  # number of ones, twos, threes, etc
    scores = {}  # will store list of scores & their associated die
    sidx = 0  # index for scores
    for d in range(num_dice):
        val = dice[d] - 1  # since val is an index, and indices start at 0
        values[val] += 1
    # print(values)
    no_mults = True

    if max(values) >= 3:
        no_mults = False

    if values[0] == 0 and values[4] == 0 and no_mults is True:
        return {}  # no score if no 1s, 5s, or 3+ multiples

    # look for runs, either 1,2,3,4,5, 2,3,4,5,6, or 1,2,3,4,5,6
    runs_score = 0
    if values[0] > 0 and values[1] > 0 and values[2] > 0 and values[3] > 0 and values[4] > 0:
        scores[sidx] = [750, [1, 2, 3, 4, 5]]
        sidx += 1
    if values[5] > 0 and values[1] > 0 and values[2] > 0 and values[3] > 0 and values[4] > 0:
        scores[sidx] = [750, [2, 3, 4, 5, 6]]
        sidx += 1
    if len(scores) == 2:  # IE if both runs are present
        scores[sidx] = [1500, [1, 2, 3, 4, 5, 6]]
        sidx += 1

    for i in range(6):
        d = i + 1  # the number on the dice
        val = values[i]
        if d == 1:
            if val >= 1:
                scores[sidx] = [100, [d]]
                sidx += 1
            if val >= 2:
                scores[sidx] = [200, [d, d]]
                sidx += 1
            if val >= 3:
                scores[sidx] = [1000, [d, d, d]]
                sidx += 1
            if val >= 4:
                scores[sidx] = [2000, [d, d, d, d]]
                sidx += 1
            if val >= 5:
                scores[sidx] = [4000, [d, d, d, d, d]]
                sidx += 1
            if val == 6:
                scores[sidx] = [8000, [d, d, d, d, d, d]]
                sidx += 1
        elif d == 5:
            if val >= 1:
                scores[sidx] = [50, [d]]
                sidx += 1
            if val >= 2:
                scores[sidx] = [100, [d, d]]
                sidx += 1
            if val >= 3:
                scores[sidx] = [d*100, [d, d, d]]
                sidx += 1
            if val >= 4:
                scores[sidx] = [d*200, [d, d, d, d]]
                sidx += 1
            if val >= 5:
                scores[sidx] = [d*400, [d, d, d, d, d]]
                sidx += 1
            if val == 6:
                scores[sidx] = [d*800, [d, d, d, d, d, d]]
                sidx += 1
        else:
            if val >= 3:
                scores[sidx] = [d*100, [d, d, d]]
                sidx += 1
            if val >= 4:
                scores[sidx] = [d*200, [d, d, d, d]]
                sidx += 1
            if val >= 5:
                scores[sidx] = [d*400, [d, d, d, d, d]]
                sidx += 1
            if val == 6:
                scores[sidx] = [d*800, [d, d, d, d, d, d]]
                sidx += 1

    return scores


def scorePrint(scores):
    # function to nicely print the dictionary of scores returned by scoreDice
    s = 'Choice\tScore\tDice Used\n'
    for x in scores:
        points = scores[x][0]
        dice = scores[x][1]
        s += f'{x}\t\t{points}\t\t{dice}\n'
    print(s)


def playTurn():
    # This function plays one turn of Farkle. It sets up 6 dice, rolls them, and lets the player pick which dice to
    # use for scoring. Then the remaining dice can be rerolled. If there's a bust, the turn ends with 0 points scored.
    # Function returns the points scored for this turn.

    dice = [0 for d in range(6)]
    round_score = 0
    did_bust = False

    while True:
        s = input('Press ENTER to roll die, press x to end turn: ')

        if s == 'x':
            return round_score

        if did_bust:
            return 0
        else:
            if len(dice) == 0:  # covers case where all dice are used for score, and player gets to roll again
                num_dice = 6
            else:
                num_dice = len(dice)  # only roll remaining dice

        dice = [random.randrange(1, 7) for d in range(num_dice)]
        dice.sort()

        turn_not_over = True
        took_points = False

        while turn_not_over:
            print(f'Dice remaining:\n{dice}')

            scores = scoreDice(dice)

            if len(scores) == 0:
                if took_points is False:
                    print('BUST!')
                    return 0
                else:
                    turn_not_over = False

            else:
                scorePrint(scores)

                choice = input('Select one score to take (press x to take none): ')

                if choice == 'x':
                    turn_not_over = False

                else:
                    took_points = True
                    score = scores[int(choice)]  # get the score info from the choice selected
                    points = score[0]  # the number of points
                    round_score += points
                    die = score[1]  # the dice used to make those points
                    for d in die:
                        dice.remove(d)  # take the scoring dice out of play for now

                    print(f'Score = {round_score}')


def main():
    print('Farkle!')

    score_threshold = int(input('Enter score to play to: '))

    p1name = input('Enter name for PLAYER 1: ')
    p2name = input('Enter name for PLAYER 2: ')

    if p1name == '':
        p1name = 'Player 1'
    if p2name == '':
        p2name = 'Player 2'

    player_1_score = 0
    player_2_score = 0

    player_1s_turn = bool(random.getrandbits(1))

    while True:
        if player_1s_turn:
            print(f'{p1name}\'s Turn')
            player_1_score += playTurn()
            print(f'{p1name} SCORE = {player_1_score}')
            if player_1_score >= score_threshold:
                print(f'{p1name} WINS')
                return
        else:
            print(f'{p2name}\'s Turn')
            player_2_score += playTurn()
            print(f'{p2name} SCORE = {player_2_score}')
            if player_2_score >= score_threshold:
                print(f'{p2name} WINS')
                return

        player_1s_turn = not player_1s_turn


if __name__ == '__main__':
    main()