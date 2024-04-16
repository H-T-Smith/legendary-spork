import numpy as np

# create a list of sets
# each index in the list represents a letter slot, and each set represents the possible letters in that slot 

# green letters (dict, letter -> index)
G = {}
# yellow letters (dict, letter -> possible indices)
Y = {}
# grey letters (set)
R = {}

valid_words = {}
remaining_words = valid_words

# translate the following from iterative to recursive:

# while the word is not solved: 

#   update remaining words
#   update g, y, and r

#   for each word in valid_words:
#       calculate partition rate

#   rank valid words by parition rate
#   for the top k words:
#       recurse (making a tree)

#   choose the best word

