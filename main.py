import numpy as np
import copy


infile = open('valid_wordle_words.txt','r')

words = infile.readlines()

# Remove the newline character from each word
for i in range(len(words)):
  words[i]=words[i][0:5]

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
#sorted_letters = dict(sorted(letter_freq.items(), key = lambda item: item[1]))
#for i in reversed(sorted_letters):
 # print(i)

# This suggests that the word "arose" has the highest liklihood of having at least 1 letter in the final word

def wordle(answer,tries,guess):
  #print("Welcome to wordle! Type a 5 letter word to begin. Note all characters are lowercase. Type 'quit' to quit at any time. \n")
  ##print("Guide:\n")
  #print("     0: letter not in word, gets removed from t\n")
  #print ("    1: letter in word in the incorrect spot")
  #print("     2: letter in word and in the correct spot.\n")


  #answer=np.random.choice(words)



  tries+=1
  #guess=' '
  #guess_info=''
  #print(tries)

  if guess in words:
    guess_info=''
    for pos in range(5):
      if guess[pos] == answer[pos]:
        guess_info+='2'
      elif guess[pos] in answer:
        guess_info+='1'
      else:
        guess_info+='0'
          #alphabet = alphabet.replace(guess[pos],'_')
      #print(guess, "   ", guess_info, "              ", alphabet)
      #print('\n')
      #tries+=1
    return tries, guess_info

    #else:
     # print("\nNot in word list")

  #print("You guessed the right word in",tries,"tries.")


# TODO: narrow down the list based on valid words



def wordle_ai(num_restarts,first_guess,tries=0):
    
    # green letters (dict, letter -> index)
    G = {}
        # yellow letters (dict, letter -> possible indices)
    Y = {}
        # grey letters (set)
    R = []

    remaining_words = copy.deepcopy(words)
    
    # TODO: Create a function that chooses words based on remaining letter frequencies, with a goal of choosing letters that
    # eliminates as many words as possible
    feedback=''
    #TMP: custom word
    #answer = 'brake'
    answer=np.random.choice(words)
    global guess
    guess=first_guess
    # While the word has not been solved for
    max_tries=15
    global count
    count=0
    #while not(feedback == '22222') and (count < max_tries):
    for i in range(1):
        
        count+=1

    

        tries, feedback=wordle(answer,tries,guess)
        #feedback = '01010'
        if (guess in remaining_words):
            remaining_words.remove(guess)

      


    # translate the following from iterative to recursive:
    
    # while the word is not solved: 
    #   update g, y, and r
     
        update_GRY(feedback,guess,G,R,Y)
        #   update remaining words
        update_possible_words(remaining_words,G,R,Y)
        
        
        print('Word: ',answer,'Guess: ',guess,'Feedback: ',feedback, 'Try #: ',tries, 'Remaining words:',len(remaining_words),'G',G,'Y',Y,'R',R)

                
            
            #print('')
            
        #print(Y)
        # REPLACE
        if (len(remaining_words) > 0) and (not(feedback == '22222')):
            
            guess=np.random.choice(remaining_words)
            
        if (len(remaining_words) < 100):
            min_words_remaining = float('inf')
            global lengths
            lens = []
            for word in remaining_words:
                tmp = 0
                feedback_tmp = ''
                potential_words = copy.deepcopy(remaining_words)
                potential_words.remove(word)
                num_words_remaining = {}
                
                lengths=[]
                for pot_answer in potential_words:
                    tmp, feedback_tmp=wordle(pot_answer,tries,word)
                    cR = copy.deepcopy(R)
                    cG = copy.deepcopy(G)
                    cY = copy.deepcopy(Y)
                    
                    c_potential_words = copy.deepcopy(remaining_words)
                    update_GRY(feedback_tmp,word,cG,cR,cY)
                    update_possible_words(c_potential_words,cG,cR,cY)
                    lengths.append(len(c_potential_words))
                
                num_words_remaining[word] = np.mean(lengths)
                lens.append(np.mean(lengths))
                #avg_words_remaining = np.mean(num_words_remaining[:])
                print(num_words_remaining)
            
                if (num_words_remaining[word] < min_words_remaining):
                    min_words_remaining = num_words_remaining[word]
                    guess = word
            if (np.std(lens) < 0.5) and len(lens) > 3: 
                print('checking entire word set for the best word to eliminate choices')
                for word in words:
                    tmp = 0
                    feedback_tmp = ''
                    potential_words = copy.deepcopy(remaining_words)
                    potential_words.remove(word)
                    num_words_remaining = {}
                    
                    lengths=[]
                    for pot_answer in potential_words:
                        tmp, feedback_tmp=wordle(pot_answer,tries,word)
                        cR = copy.deepcopy(R)
                        cG = copy.deepcopy(G)
                        cY = copy.deepcopy(Y)
                        
                        c_potential_words = copy.deepcopy(remaining_words)
                        update_GRY(feedback_tmp,word,cG,cR,cY)
                        update_possible_words(c_potential_words,cG,cR,cY)
                        lengths.append(len(c_potential_words))
                    
                    num_words_remaining[word] = np.mean(lengths)
                    #lens.append(np.mean(lengths))
                    #avg_words_remaining = np.mean(num_words_remaining[:])
                    print(num_words_remaining)
                    if (num_words_remaining[word] < min_words_remaining):
                        min_words_remaining = num_words_remaining[word]
                        guess = word
                
                
        #guess = 'arose'
        
    #   for each word in valid_words:
    
        
            #       calculate partition rate
    #   rank valid words by parition rate
    #   for the top k words:
    #       recurse (making a tree)
    
    #   choose the best word

    return (guess,answer,tries)

def update_GRY(feedback, guess, G, R, Y):
    pos = 0
    
    for i in feedback:
        #print(pos)
        letter = guess[pos]
        if (i == '2'):
            G[letter] = pos
        elif (i == '1'):
            if (letter not in Y):
                #print("letter",letter,"pos:",pos)
                Y[letter] = {0,1,2,3,4}
            
            if (pos in Y[letter]):
                Y[letter].remove(pos)
                
        elif (i == '0'):
            if (letter not in R):
                R += letter
            
        pos += 1

def update_possible_words(remaining_words,G,R,Y):
    iters=0
    words_to_remove = []
    for word in remaining_words:
        iters+=1
        pos=0
        case=0
        
        possible=True
        for letter in word:
            
            if letter in R: # In case of grey: 
                possible=False
                case = 1
            
            if letter in Y: # in case of yellow
                if (pos not in Y[letter]):       
                    possible=False
                    case = 2

            pos+=1
            for letter in Y:
                if letter not in word:
                    possible=False
                    case = 4
            for letter in G:
                    if not(letter == word[G[letter]]):
                        possible=False
                        case=5

        if not(possible):
            words_to_remove.append(word)

    for word in words_to_remove:
        if word in remaining_words:
            remaining_words.remove(word)
    
    
    
# Call function
avgs = []
print(wordle_ai(1,'salet'))
#for i in range(100):
#    tmp = 0
#    tmp1 = 0
#    num_tries = 0
#    tmp, tmp1, num_tries = wordle_ai(1,'salet')
#    avgs.append(num_tries)
#    print(num_tries)

