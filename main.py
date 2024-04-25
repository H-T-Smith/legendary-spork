import numpy as np
import copy
import time

infile = open('valid_wordle_words.txt','r')

words = infile.readlines()

# Remove the newline character from each word
for i in range(len(words)):
  words[i]=words[i][0:5]

def letter_frequencies(words):
    # Optional step: determine the best starting word or a set of words using the probability of a letter's occurence
    # This can also factor into the algorithm's decision making for later words
    # Determine what letters are most common in the dataset
    letter_freq = { 'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i':0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y':0, 'z': 0}
    
    from collections import OrderedDict
    
    for word in words:
      for letter in word:
        letter_freq[letter]+=1
        #print(int(letter_freq[letter]))
    #keys,items=letter_freq.items()
    sorted_letters = dict(sorted(letter_freq.items(), key = lambda item: item[1]))
    for i in reversed(sorted_letters):
      print(i)

# This suggests that the word "arose" has the highest liklihood of having at least 1 letter in the final word


# This function acts as our "guess" to wordle
# We query with the answer (we treat this as an unknown)
# The guess is what we think the answer is
# Tries is a variable that stores the number of times wordle is called
def wordle(answer,tries,guess):
    
    
  # Optional code if making a user interface for manually testing wordle
  #print("Welcome to wordle! Type a 5 letter word to begin. Note all characters are lowercase. Type 'quit' to quit at any time. \n")
  ##print("Guide:\n")
  #print("     0: letter not in word, gets removed from t\n")
  #print ("    1: letter in word in the incorrect spot")
  #print("     2: letter in word and in the correct spot.\n")

  tries+=1

  if guess in words: # Always true if guess is coming out of words
    guess_info=''
    for pos in range(5): # For each letter in the word
      if guess[pos] == answer[pos]: # Green case, right letter in the right spot
        guess_info+='2'
      elif guess[pos] in answer: # Yellow case, right letter in the wrong spot
        guess_info+='1'
      else: # Gray case, letter not in answer
        guess_info+='0'
       
    return tries, guess_info

# Function for the ai to play wordle. Num_restarts is currently unused.
# As of now, requires choosing a first guess before running
def wordle_ai(num_restarts,first_guess,compute_remaining,tries=0):
    
    # green letters (dict, letter -> index) # Should be index -> letter
    G = {}
        # yellow letters (dict, letter -> possible indices)
    Y = {}
        # grey letters (set)
    R = []
    
    # Deepcopy from words so we can shrink the temporary list without affecting the original
    remaining_words = copy.deepcopy(words)
    
    # First time variables setup:
    feedback=''
    #answer = 'vents'
    answer=np.random.choice(words)
    global guess
    guess=first_guess 
    
    max_tries=15 # Used for testing to prevent infinite loops
    global count
    count=0
    
    # If feedback = '22222', that's equivalent to all green letters meaning guess == answer
    while not(feedback == '22222') and (count < max_tries):
    #for i in range(1):
        
        count+=1
        
        # Make our guess, update feedback and the tries number
        tries, feedback=wordle(answer,tries,guess)

        # Remove the guess from remaining words so that word isn't guessed twice
        if (guess in remaining_words): 
            remaining_words.remove(guess)

        # Game state updaters
        update_GRY(feedback,guess,G,R,Y)
        update_possible_words(remaining_words,G,R,Y)
        
        # Print status: gives an idea of what the guess is, what the game state variables equal, and how many words remain
        print('Word: ',answer,'Guess: ',guess,'Feedback: ',feedback, 'Try #: ',tries, 'Remaining words:',len(remaining_words),'G',G,'Y',Y,'R',R,)
            
        if (len(remaining_words) > 0) and (not(feedback == '22222')):
            # Use if guessing the remaining word at random
            guess=np.random.choice(remaining_words)
            
        
        # Optional, calls a function that returns the guess optimized for eliminating the most choices of the remaining words
        if (len(remaining_words) < 100) and (compute_remaining):
            # For the sake of speed, limit to when we have less than 100 words left
            lens = []
            
            #print('guess before',guess)
            guess, lens = find_min_words_remaining(remaining_words,remaining_words,guess,lens,G,R,Y)
            #print('guess after',guess)
            
            if (np.std(lens) < 0.5) and len(remaining_words) > 2: 
                print('checking entire word set for the best word to eliminate choices')
                # Perform a deeper search considering all words as possible guesses
                # The guess returned here may not be following the rules, but is the best at eliminating the remaining choices
                guess, lens = find_min_words_remaining(words,remaining_words,guess,lens,G,R,Y)
        
        print('chosen guess:',guess)
    return (guess,answer,tries)

def find_min_words_remaining(words,words_subset,guess,lens,G,R,Y):
    min_words_remaining = float('inf')
    

    global lengths
    for word in words:
        tmp = 0
        feedback_tmp = ''
        potential_words = copy.deepcopy(words_subset)
        if (word in potential_words):
            potential_words.remove(word)
        num_words_remaining = {}
        
        lengths=[]
        for pot_answer in potential_words:
            tmp, feedback_tmp=wordle(pot_answer,tries,word)
            cR = copy.deepcopy(R)
            cG = copy.deepcopy(G)
            cY = copy.deepcopy(Y)
                
            c_potential_words = copy.deepcopy(words_subset)
            update_GRY(feedback_tmp,word,cG,cR,cY)
            update_possible_words(c_potential_words,cG,cR,cY)
            lengths.append(len(c_potential_words))
            
        num_words_remaining[word] = float(np.mean(lengths))
        lens.append(np.mean(lengths))
        
        if len(words) == len(words_subset):
            print(num_words_remaining)
        
        if (num_words_remaining[word] < min_words_remaining):
            min_words_remaining = num_words_remaining[word]
            guess = copy.deepcopy(word)
            print(guess, min_words_remaining)
    
    return guess, lens

# Updates the variables G, R, and Y based off the guess and feedback from that guess
def update_GRY(feedback, guess, G, R, Y):
    pos = 0
    # TODO: fix so that G has indices at keys, not letters
    for i in feedback:
        letter = guess[pos]
        if (i == '2'):
            G[pos] = letter
        elif (i == '1'): # Yellow case
            if (letter not in Y):
                # If the letter is yellow for the first time, start off assuming it could be in any index
                Y[letter] = {0,1,2,3,4}
            
            if (pos in Y[letter]): 
                # If the letter is yellow, it cannot be in that position so remove that index from the list
                Y[letter].remove(pos)
                
        elif (i == '0'):
            # Grey case
            if (letter not in R):
                R += letter
            
        pos += 1

# Shrinks the list of possible words, basically a constraint satisfaction algorithm considering G, R, and Y
def update_possible_words(remaining_words,G,R,Y):
    iters=0
    words_to_remove = []
    for word in remaining_words:
        iters+=1
        pos=0
        case=0
        
        possible=True
        for letter in word:
            # These two require looping through the letters of the word
            
            if letter in R: # In case of grey: 
                possible=False
                case = 1
            
            if letter in Y: # in case of yellow
                if (pos not in Y[letter]):       
                    possible=False
                    case = 2
            
            if pos in G:
                if not(G[pos] == letter):
                    possible=False
            
            pos+=1
            
            # These require looping through the dictionaries for Y and G
            for letter in Y:
                if letter not in word:
                    possible=False
                    case = 4
           

        
        if not(possible):
            # Removing elements from the list you are iterating through is problematic
            # Solved by creating a temporary list of words to remove and then removing them all at the end
            words_to_remove.append(word)
            
    # If a word cannot be the final answer, remove it from the list of remaining words
    for word in words_to_remove:
        if word in remaining_words:
            remaining_words.remove(word)
    
    
    
# Call function
#avgs = []


# test with "vents"

compute_remaining=True
print(wordle_ai(1,'salet',compute_remaining))
avgs = []
compute_times = []
start_time = time.time()
for i in range(100):
    tmp = 0
    tmp1 = 0
    num_tries = 0
    tmp, tmp1, num_tries = wordle_ai(1,'salet',compute_remaining)
    avgs.append(num_tries)
    end_time = time.time()
    compute_times.append(end_time - start_time)
    print(num_tries)
#stdout.close()