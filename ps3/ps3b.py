# 6.00 Problem Set 3b
# The 6.00 Word Game
# Denis Savenkov
# ps3b.py

from ps3a import *
import time
from perm import *


# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    # MY CODE
    #create a list of all possible permutations of length 1 to HAND_SIZE 
    perms = []
    for i in range(1, len(hand)+1):
        perms += get_perms(hand, i)

    #create a list of all possible words from all permutations
    words = []
    for seq in perms: 
        if seq in word_list:
            words.append(seq)

    #if there are no possible words, return "."
    if len(words) == 0:
        return "."

    #create a list of words scores
    word_score = []
    for word in words:
        word_score.append(get_word_score(word, HAND_SIZE))

    #find max score and an index for that word
    max_score = max(word_score)
    index = word_score.index(max_score)

    #return the word with max score
    return words[index]
   
#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # MY CODE    
    total_score = 0
    while sum(hand.values()) > 0:
        print
        print "Current Hand:",
        display_hand(hand)
        word = comp_choose_word(hand, word_list)
        print "The computer has chosen word:", word
        if word == ".":
            break
        else:
            point = get_word_score(word, HAND_SIZE)
            total_score += point
            print '"%s" earned %d points. Total: %d points' % (word, point, total_score)  
            hand = update_hand(hand, word)

    print "Total score: "+str(total_score)+" points."
    print
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # MY CODE
    hand = deal_hand(HAND_SIZE)
    
    while True:
        user_input1 = raw_input("Enter 'n' to play new hand, 'r' to play last hand, 'e' to exit: ")
        while user_input1 != "n" and user_input1 != "r" and user_input1 != "e":
            print "Invalid input."
            user_input1 = raw_input("Enter 'n' to play new hand, 'r' to play last hand, 'e' to exit: ")
        if user_input1 == 'e':
            return

        user_input2 = raw_input("Enter 'u' to play yourself, or 'c' for computer to play: ")
        while user_input2 != "u" and user_input2 != "c":
            print "Invalid input."
            user_input2 = raw_input("Enter 'u' to play yourself, or 'c' for computer to play: ")
            
        if user_input1 == 'n':
            hand = deal_hand(HAND_SIZE)
         
        if user_input2 == 'u':
            play_hand(hand.copy(), word_list) 
        elif user_input2 == 'c':
            comp_play_hand(hand.copy(), word_list)


        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    
