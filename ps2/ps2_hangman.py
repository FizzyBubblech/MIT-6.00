# 6.00 Problem Set 2
# Hangman
# Denis Savenkov
# hangman.py


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code begins here!
SECRET_WORD = choose_word(wordlist)
LETTERS_GUESSED = []
AVAILABLE_LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m',\
                     'n','o','p','q','r','s','t','u','v','w','x','y','z']
    
def word_guessed():
    '''
    Returns True if the player has successfully guessed the word,
    and False otherwise.
    '''
    global SECRET_WORD
    global LETTERS_GUESSED
    
    for letter in SECRET_WORD:
        if letter not in LETTERS_GUESSED:
            return False
    return True

def print_available():
    '''
    Prints out available letters to choose for a guess
    '''
    global LETTERS_GUESSED
    global AVAILABLE_LETTERS

    for i in range(len(AVAILABLE_LETTERS)-1):
        if AVAILABLE_LETTERS[i] in LETTERS_GUESSED:
            del AVAILABLE_LETTERS[i]
    return string.join(AVAILABLE_LETTERS,'')
        
def print_guessed():
    '''
    Prints out the characters you have guessed in the secret word so far
    '''
    global SECRET_WORD
    global LETTERS_GUESSED

    char_list = []
    for letter in SECRET_WORD:
        if letter in LETTERS_GUESSED:
            char_list.append(letter)  
        else:
            char_list.append('_')
    return string.join(char_list,' ')
          
def hangman():
    '''
    Plays the game itself
    '''
    global SECRET_WORD
    global LETTERS_GUESSED
    guesses = 8
    
    print "\n", "Welcome to the game, Hangman!"
    print "I am thinking of a word that is", len(SECRET_WORD),\
          "letters long."
    print "-------------"
    
    # Letter-guessing loop. Ask the user to guess a letter and respond to the
    # user based on whether the word has yet been correctly guessed.
    while guesses > 0 and not word_guessed():
        print "You have", guesses, "guesses left."
        print "Available letters:", print_available()
        letter = string.lower(raw_input("Please guess a letter: "))
        while letter in LETTERS_GUESSED:
            letter = string.lower(raw_input("This letter has already been "\
                                            "given, please try again: "))
        LETTERS_GUESSED.append(letter)
        if letter not in SECRET_WORD:
            guesses -= 1
            print "Oops! That letter is not in my word:", print_guessed()
            print "------------"
        else:
            print "Good guess:", print_guessed()
            print "------------"

    if word_guessed():
        print "Congratulations, you won!"
        return 1
    else:
        print "You lost!"
        print "The secret word is:", SECRET_WORD
        return -1

hangman()
