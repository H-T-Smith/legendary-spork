import numpy as np
import random
import string

NUM_ITERATIONS = 1

infile = open('valid_wordle_words.txt', 'r')
ALL_WORDS = infile.read().split('\n')
ALL_LETTERS = string.ascii_lowercase

def wordle(guess, correct_word):
    result = {'green': set(), 'yellow': set(), 'gray': set()}
    
    for i in range(5):
        if guess[i] == correct_word[i]:
            result['green'].add(i)
        elif guess[i] in correct_word:
            result['yellow'].add(i)
        else:
            result['gray'].add(i)
    
    return result

def compute_probabilities():
    pass

def wordle_ai(green, yellow, gray, possible_words, attempts, correct_word):
    
    # guess using compute_probabilites
    guess = random.choice(possible_words)
    
    result = wordle(guess, correct_word)
    attempts += 1
    
    print('Attempt:', attempts, 'Guess:', guess)
    
    # update green, yellow, gray
    for index in result['green']:
        green[index] = guess[index]
    for index in result['yellow']:
        if guess[index] in yellow:
            yellow[guess[index]].add(index)
        else:
            yellow[guess[index]] = {index}
    for index in result['gray']:
        if guess[index] in yellow:
            yellow.pop(guess[index])
        gray.add(guess[index])

    # update possible_words
    for word in possible_words:
        flag = False
        # green letters
        for index, letter in green.items():
            if word[index] != letter:
                possible_words.remove(word)
                flag = True
                break
        if flag:
            continue
        # gray letters
        for letter in gray:
            if letter in word:
                possible_words.remove(word)
                flag = True
                break
        if flag:
            continue
        # yellow letters
        for letter, indices in yellow.items():
            if letter not in word:
                possible_words.remove(word)
                flag = True
                break
            for index in indices:
                if word[index] == letter:
                    possible_words.remove(word)
                    flag = True
                    break
            if flag:
                break
        if flag:
            continue
        
    
    
    if len(green) == 5:
        answer = ''
        for i in range(5):
            answer += green[i]
        print(f'Found answer: {answer} in {attempts} attempts')
        return


    wordle_ai(green, yellow, gray, possible_words, attempts, correct_word)


def play_wordle():
    # green maps integers to characters
    green = dict()
    # yellow maps characters to sets of integers
    yellow = dict()
    # gray is just a set of characters
    gray = set()
    
    correct_word = random.choice(ALL_WORDS)

    wordle_ai(green, yellow, gray, ALL_WORDS.copy(), 0, correct_word)
    
    
for i in range(NUM_ITERATIONS):
    play_wordle()