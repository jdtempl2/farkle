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
    print(values)
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


def main():
    print('Farkle!')

    num_dice = int(input('Enter # of dice: '))
    dice = []
    for d in range(num_dice):
        dice.append(0)

    while True:
        input('Press ENTER to roll die')
        for d in range(num_dice):
            dice[d] = random.randrange(1, 7)
        dice.sort()

        print(dice)
        scores = scoreDice(dice)

        print(scores)


if __name__ == '__main__':
    main()