import numpy as np
import itertools

wordlist = set(open('wordlist', 'r').read().split('\n'))

def valid(word):
    assert word == word.strip().upper()
    return word in wordlist



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

        self.words = []
        for cords in self.starts:
            self._search([cords,])
        return self.words


    def _search(self, path):

        # path :: [(0,0), (1,1), ...]
        #          start  ------> current location

        # --- check current word ---
        word = ''.join(self.board[tuple(cords)] for cords in path)
        if valid(word):
            print(word)
            self.words.append(word)


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




words = Board((
    'tsf',
    'yus',
    'eca',
    )).solve()



print(tuple(words))





