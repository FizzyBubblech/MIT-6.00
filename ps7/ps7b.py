# Problem Set 7: Monte Carlo simulation
# Denis Savenkov
# ps7b.py

import random

def roll():
    """
    Simulates a dice roll

    returns: a number between 1 and 6 (an integer)
    """
    dice = [1, 2, 3, 4, 5, 6]
    return random.choice(dice)

def Yahtzee(numTrials):
    """
    Monte Carlo simulation for Yahtzee problem.

    numTrials: number of trials

    returns: probability (a float)
    """
    numWins = 0.0
    for i in range(numTrials):
        d1 = roll()
        d2 = roll()
        d3 = roll()
        d4 = roll()
        d5 = roll()
        if d1 == d2 == d3 == d4 == d5:
            numWins += 1

    return numWins/numTrials
