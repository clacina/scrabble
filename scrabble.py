import copy
import random

random.seed(1001)

dictionary_file = 'dictionary.csv'

board_width = 15
horizontal_axis = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O']
vertical_axis = ['1', '2', '3', '4','5', '6', '7', '8', '9', '10', '11', '12',
                 '13', '14', '15']
user_letter_count = 7

# Letter, count, score
letters = {
    'E': (12, 1),
    'A': (9, 1),
    'I': (9, 1),
    'O': (8, 1),
    'N': (6, 1),
    'R': (6, 1),
    'T': (6, 1),
    'L': (4, 1),
    'S': (4, 1),
    'U': (4, 1),
    'D': (4, 2),
    'G': (3, 2),
    'B': (2, 3),
    'C': (2, 3),
    'M': (2, 3),
    'P': (2, 3),
    'F': (2, 4),
    'H': (2, 4),
    'V': (2, 4),
    'W': (2, 4),
    'Y': (2, 4),
    'K': (1, 5),
    'J': (1, 8),
    'X': (1, 8),
    'Q': (1, 10),
    'Z': (1, 10),
    ' ': (2, 0)
}


def get_letter_score(letter):
    return letters[letter.upper()][1]

triple_word_squares = 8
double_word_squares = 17
triple_letter_squares = 12
double_letter_squares = 24


class BoardCell(object):
    def __init__(self):
        self.letter_modifier = 1
        self.word_modifier = 1
        self.letter_value = None
        self.score = 0


class Board(object):
    def __init__(self):
        # create board matrix
        self.Matrix = [[BoardCell() for x in range(board_width)]
                       for y in range(board_width)]

        # create letter pool
        self.letter_pool = list()
        for l, d in letters.iteritems():
            # print("There are {} {}s".format(d[0], l))
            for a in range(d[0]):
                self.letter_pool.append((l, d[1]))

    def pull_random_letter_from_pool(self):
        index = random.randint(0, len(self.letter_pool)-1)
        return_val = self.letter_pool[index]
        del self.letter_pool[index]
        return return_val

    def place_word(self, word, position, direction='down'):
        x = ord(position[0].upper()) - ord('A')
        y = position[1]

        for l in word:
            self.Matrix[x][y].letter_value = l
            if direction == 'down':
                y += 1
            else:
                x += 1

    @staticmethod
    def print_x_axis():
        row = "|   |"
        for x in horizontal_axis:
            row += " {} |".format(x)
        print(row)

    def print_board(self):
        self.print_x_axis()
        for y in range(0, board_width):
            if y < 9:
                row = "| {} |".format(vertical_axis[y])
            else:
                row = "|{} |".format(vertical_axis[y])

            for x in range(0, board_width):
                letter = self.Matrix[x][y].letter_value
                if letter is None:
                    letter = ' '
                row += " {} |".format(letter)
            print(row)

    def playable_areas(self):
        """
        Loop through each row and each column to find where letters can be placed.
        Return is a 'find word' query spec
        """
        for y in range(0, board_width):
            found_at = list()
            for x in range(0, board_width):
                if self.Matrix[x][y].letter_value is not None:
                    found_at.append(CellCoord(x, y,
                                              self.Matrix[x][y]))


class CellCoord(object):
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter


class LookupSpec(object):
    def __init__(self):
        self.match = list()
        self.max_len = 0
        self.positions = list()


class BoardUser(object):
    def __init__(self):
        self.letters = list()

    def refill(self, board_object):
        while len(self.letters) < 7 and len(board_object.letter_pool) >= 0:
            self.letters.append(board_object.pull_random_letter_from_pool())

    def find_word(self, lookup_dictionary, match=None, position=None,
                  max_len=None):
        words = list()
        for word in lookup_dictionary:
            available_letters = copy.deepcopy(self.letters)
            found_word = list()

            # First, see if we have the first character in the word
            for w in word.upper():
                letter_in_rack = False
                for l in available_letters:
                    if l[0] == w:
                        letter_in_rack = True
                        found_word.append(l)
                        available_letters.remove(l)
                        break

                if not letter_in_rack:
                    break

            # see if we found all the letters
            if len(found_word) == len(word):
                words.append(word)
            # Now check for conditions
            # if word_length >= len(l):
            #     if match:
            #         if len(l) > position < max_len and l[position] == match:
            #             words.append(l)
            #     else:
            #         words.append(l)

        return words

    def print_rack(self):
        print(self.letters)


b = Board()
user1 = BoardUser()
user2 = BoardUser()

user1.refill(b)
user2.refill(b)

user1.print_rack()
user2.print_rack()

# load our dictionary
dictionary = list()
with open(dictionary_file, 'r') as df:
    line = df.readline()
    while line:
        dictionary.append(line.strip())
        line = df.readline()

print('Dictionary length is {}'.format(len(dictionary)))

result_words = user1.find_word(dictionary, 'c', 2, 5)
result_words = user1.find_word(dictionary)

print("{}".format(result_words))

if len(result_words):
    # figure out which word
    best_score = 0
    best_score_index = -1
    for w in range(0, len(result_words)):
        cur_score = 0
        for c in result_words[w]:
            cur_score += get_letter_score(c)

        if cur_score > best_score:
            best_score = cur_score
            best_score_index = w

    print("Best word was {} with a score of {}".format(result_words[best_score_index],
                                                       best_score))

    half_len = len(result_words[best_score_index]) / 2
    xpos = 8 - half_len
    xpos += ord('A')

    b.place_word(result_words[best_score_index], (chr(xpos), 8), direction='left')
    b.print_board()
