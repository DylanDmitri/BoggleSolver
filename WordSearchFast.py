
# --- build the trie ---
import pickle

def cleaned(word):
    return word.strip().upper()

class SequenceTree(dict):
    def __init__(self):
        dict.__init__({})
        self.word_end = False


    def add(self, word, index=0):

        if index==len(word):
            self.word_end = True

        else:
            next_letter = word[index]
            if next_letter not in self:
                self[next_letter] = SequenceTree()
            self[next_letter].add(word, index+1)

    def lookup(self, sequence, index=0):
        if index == len(sequence):
            return self

        next_letter = sequence[index]
        if next_letter not in self:
            return False

        return self[next_letter].lookup(sequence, index+1)



rebuild = False

if rebuild:
    root = SequenceTree()
    for word in open('wordlist', 'r'):
        root.add(cleaned(word))
    print('built')

    pickle.dump(root, open('word_lookup.pkl', 'wb'))
    print('saved')

else:
    root = pickle.load(open('word_lookup.pkl', 'rb'))
    print('loaded')


def valid_word(word):
    return root.lookup(sequence=word).word_end

def valid_stem(word):
    return bool(root.lookup(sequence=word))


# ===============================
# --- do the search ---

import numpy as np
import itertools


class Board:
    def __init__(self, letters):

        # needs to be a 2D array of letters
        assert all((
                hasattr(letters, '__iter__'),
                hasattr(letters[0], '__iter__'),
                type(letters[0][0]) is str,
                len(letters[0][0]) == 1))

        length,width = len(letters),len(letters[0])

        # make sure everything is capitalized

        self.board = np.empty((length, width), dtype='str',)

        for x in range(length):
            for y in range(width):
                self.board[x,y] = letters[x][y].upper()



    def solve(self):

        dimensions = len(self.board.shape)

        self.offsets = np.array(list(
            itertools.product(*([(-1, 0, 1),]*dimensions))
        ))

        self.starts = np.array(list(
            itertools.product(*[range(self.board.shape[d]) for d in range(dimensions)])
        ))

        self.words = set()
        for cords in self.starts:
            self._search([cords,])
        return self.words


    def _search(self, path):

        # path :: [(0,0), (1,1), ...]
        #          start  ------> current location

        # --- check current word ---
        word = ''.join(self.board[tuple(cords)] for cords in path)
        if not valid_stem(word):
            return

        if valid_word(word):
            self.words.add(word)


        # --- check potential steps ---
        current = path[-1]
        for offset in self.offsets:
            new = current + offset

            # skip if out of bounds
            if not all(0 <= new[dimension] < max_size
               for dimension,max_size in enumerate(self.board.shape)):
                continue

            # skip if already in path
            if (path == new).all(axis=1).any(): continue

            self._search(path + [new])




# words = Board((
#     'apur',
#     'nkpg',
#     'ting',
#     'caln'
#     )).solve()


words = Board((
    'knapping',
    'knappedq',
    'knappple',
    'knapsack',
)).solve()


print(len(tuple(words)), 'words found')

for word in sorted(words, key=len, reverse=True):
    print(word)





