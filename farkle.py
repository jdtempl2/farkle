import random


def scoreDice(dice):
    #                1  2  3  4   5  6
    dice_values = [100, 0, 0, 0, 50, 0]  # scores for individual dice
    # dice is a List of up to 6 ints
    num_dice = len(dice)
    values = [0,0,0,0,0,0]  # number of ones, twos, threes, etc
    scores = [0,0,0,0,0,0]  # scores for ones, twos, threes, etc
    for d in range(num_dice):
        val = dice[d] - 1  # since val is an index, and indices start at 0
        values[val] += 1
    print(values)
    no_mults = True

    if max(values) >= 3:
        no_mults = False

    if values[0] == 0 and values[4] == 0 and no_mults is True:
        return 0  # no score if no 1s, 5s, or 3+ multiples

    # look for runs, either 1,2,3,4,5, 2,3,4,5,6, or 1,2,3,4,5,6
    runs_score = 0
    if values[0] > 0 and values[1] > 0 and values[2] > 0 and values[3] > 0 and values[4] > 0:
        runs_score = 750
    if values[5] > 0 and values[1] > 0 and values[2] > 0 and values[3] > 0 and values[4] > 0:
        runs_score += 750

    for i in range(6):
        val = values[i]
        dice_score = dice_values[i]
        if val < 3:
            scores[i] = dice_score * val
        else:
            if i == 0:
                scores[i] = 1000
            else:
                scores[i] = (i+1) * 100

        if val == 4:
            scores[i] *= 2
        elif val == 5:
            scores[i] *= 4
        elif val == 6:
            scores[i] *= 8

    return sum(scores) + runs_score


def main():
    print('Farkle!')

    dice = [1, 1, 1, 1, 1, 1]

    while True:
        input('Press ENTER to roll die')
        for d in range(6):
            dice[d] = random.randrange(1, 7)
        dice.sort()

        print(dice)
        print(scoreDice(dice))


if __name__ == '__main__':
    main()