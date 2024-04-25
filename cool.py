import numpy as np
import random
import string
import time
import copy
import sys
import csv

NUM_ITERATIONS = 999999999

infile = open('valid_wordle_words.txt', 'r')
ALL_WORDS = infile.read().split('\n')
ALL_LETTERS = string.ascii_lowercase

class GameState:
    def __init__(self, green, yellow, gray, possible_words):
        self.green = green
        self.yellow = yellow
        self.gray = gray
        self.possible_words = possible_words

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

def simulate_guess(state, guess, correct_word):
    result = wordle(guess, correct_word)
    
    # update green, yellow, gray
    for index in result['green']:
        state.green[index] = guess[index]
    for index in result['yellow']:
        if guess[index] in state.yellow:
            state.yellow[guess[index]].add(index)
        else:
            state.yellow[guess[index]] = {index}
    for index in result['gray']:
        if guess[index] in state.yellow:
            state.yellow.pop(guess[index])
        state.gray.add(guess[index])

    if len(state.green) == 5:
        answer = ''
        for i in range(5):
            answer += state.green[i]
        state.possible_words = { answer: 1 }
        return
        
    possible_words_copy = state.possible_words.copy()
    updated_possible_words = {}
    # update possible_words
    for word in possible_words_copy:
        flag = False

        # Check green letters
        for index, letter in state.green.items():
            if word[index] != letter:
                flag = True
                break
        
        # Check gray letters
        if not flag:
            for letter in state.gray:
                if letter in word:
                    flag = True
                    break

        # Check yellow letters
        if not flag:
            for letter, indices in state.yellow.items():
                if letter not in word:
                    flag = True
                    break
                for index in indices:
                    if word[index] == letter:
                        flag = True
                        break
                if flag:
                    break

        # Add word to updated_possible_words if all checks passed
        if not flag:
            updated_possible_words[word] = possible_words_copy[word]

        # Update state.possible_words
    state.possible_words = updated_possible_words
        
def print_result(green, attempts):
    answer = ''
    for i in range(5):
        answer += green[i]
    print(f'Found answer: {answer} in {attempts} attempts')

def calculate_evals_limited(state, correct_word, depth, max_depth, k):
    print(depth)
    if len(state.possible_words) == 1 or depth == max_depth:
        keys_iterator = iter(state.possible_words.keys())
        any_key = next(keys_iterator)
        return (depth, any_key, len(state.possible_words))
    
    new_states = {}
    for guess in ALL_WORDS:
        new_states[guess] = copy.deepcopy(state)
        for word in new_states[guess].possible_words:
            new_states[guess].possible_words[word] = 0
        for word in state.possible_words:
            current_state = copy.deepcopy(state)
            simulate_guess(current_state, guess, word)
            inner_freq = sum(current_state.possible_words.values())
            for surviving_word in current_state.possible_words:
                new_states[guess].possible_words[surviving_word] += current_state.possible_words[surviving_word] / inner_freq
        total_freq = sum(new_states[guess].possible_words.values())
        for word in new_states[guess].possible_words:
            new_states[guess].possible_words[word] *= 100 * state.possible_words[word] / total_freq


    new_states = {key: new_states[key] for key in sorted(new_states, key=lambda x: sum(new_states[x].possible_words.values()))[:k]}
    
    best_depth = sys.maxsize
    best_eval = sys.maxsize
    best_guess = None
    for key in new_states.keys():
        current_depth, _, current_eval = calculate_evals_limited(new_states[key], correct_word, depth + 1, max_depth, k)
        if current_depth < best_depth or (current_depth == best_depth and current_eval < best_eval):
            best_depth = current_depth
            best_eval = current_eval
            best_guess = key           
                
    return (best_depth, best_guess, best_eval)
    

def wordle_state_space(state, correct_word, max_depth, k, current_depth=0):
    # simulate all possible guesses, make a sorted list based on the heuristic (remaining possible answers)
    guess = random.choice(list(state.possible_words.keys()))
    simulate_guess(state, guess, correct_word)
    current_depth = 1
    if guess == correct_word:
        return 1
    while (len(state.green) < 5):
        _, guess, _ = calculate_evals_limited(state, correct_word, 0, max_depth, k)
        print('*********REAL_GUESSS***********')
        print(guess, correct_word)
        simulate_guess(state, guess, correct_word)
        print(len(state.green))
        current_depth += 1
    return current_depth

def wordle_informed_guess(state, correct_word, current_depth=0):
    if len(state.green) == 5:
        return current_depth
    guess = ''
    for i in range(5):
        if i in state.green:
            guess += state.green[i]
            continue
        letter_freqs = {letter: 0 for letter in ALL_LETTERS}
        for word in state.possible_words.keys():
            letter_freqs[word[i]] += 1
        guess += max(letter_freqs, key=letter_freqs.get)        
    simulate_guess(state, guess, correct_word)
    return wordle_informed_guess(state, correct_word, current_depth + 1)

def wordle_random_guess(state, correct_word, current_depth=0):
    if len(state.green) == 5:
        return current_depth
    guess = random.choice(list(state.possible_words.keys()))
    simulate_guess(state, guess, correct_word)
    return wordle_random_guess(state, correct_word, current_depth + 1)
        

def play_wordle():
    # green maps integers to characters
    green = dict()
    # yellow maps characters to sets of integers
    yellow = dict()
    # gray is just a set of characters
    gray = set()
    
    correct_word = random.choice(ALL_WORDS)

    return wordle_state_space(GameState(green, yellow, gray, {key: 1 for key in ALL_WORDS}), correct_word, 1, 1)
    
    

with open('1deep_allwords.csv', 'w', newline='') as csvfile:
    # Define CSV writer object
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow(['Iteration', 'Execution Time (seconds)'])
    
    # Run the program for each iteration and record the execution time
    for i in range(NUM_ITERATIONS):
        start_time = time.time()
        turns = play_wordle()
        end_time = time.time()
        # Calculate and write the execution time to the CSV file
        execution_time = end_time - start_time
        writer.writerow([i + 1, turns, execution_time])
    