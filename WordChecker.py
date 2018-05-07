

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



root = SequenceTree()
for word in open('wordlist', 'r'):
    root.add(cleaned(word))


print('built')

import pickle
pickle.dump(root, open('word_lookup.pkl', 'wb'))

print('saved')
