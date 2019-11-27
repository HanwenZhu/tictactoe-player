import random


alpha = 1
decay = .999

values = {}


class Board:

    def __init__(self, nw=0, n=0, ne=0, w=0, m=0, e=0, sw=0, s=0, se=0):
        # -1 is O (opponent); 1 is X (player)
        self.nw = nw
        self.n = n
        self.ne = ne
        self.w = w
        self.m = m
        self.e = e
        self.sw = sw
        self.s = s
        self.se = se
        self.grid = (self.nw, self.n, self.ne,
                     self.w, self.m, self.e,
                     self.sw, self.s, self.se)

    def transpose(self):
        return Board(self.nw, self.w, self.sw,
                     self.n, self.m, self.s,
                     self.ne, self.e, self.se)

    def rotate(self):
        return Board(self.sw, self.w, self.nw,
                     self.s, self.m, self.n,
                     self.se, self.e, self.ne)

    def similar(self):
        board = self
        yield board
        yield board.transpose()
        board = board.rotate()
        yield board
        yield board.transpose()
        board = board.rotate()
        yield board
        yield board.transpose()
        board = board.rotate()
        yield board
        yield board.transpose()

    def invert(self):
        return Board(*(-i for i in self.grid))

    def win(self):
        if self.nw == self.n == self.ne == -1:
            return -1
        if self.w == self.m == self.e == -1:
            return -1
        if self.sw == self.s == self.se == -1:
            return -1
        if self.nw == self.w == self.sw == -1:
            return -1
        if self.n == self.m == self.s == -1:
            return -1
        if self.ne == self.e == self.se == -1:
            return -1
        if self.nw == self.m == self.se == -1:
            return -1
        if self.sw == self.m == self.ne == -1:
            return -1

        if self.nw == self.n == self.ne == 1:
            return 1
        if self.w == self.m == self.e == 1:
            return 1
        if self.sw == self.s == self.se == 1:
            return 1
        if self.nw == self.w == self.sw == 1:
            return 1
        if self.n == self.m == self.s == 1:
            return 1
        if self.ne == self.e == self.se == 1:
            return 1
        if self.nw == self.m == self.se == 1:
            return 1
        if self.sw == self.m == self.ne == 1:
            return 1

        return 0

    def play(self, position):
        grid = list(self.grid)
        grid[position] = 1
        return Board(*grid)

    def full(self):
        return all(self.grid)

    def step(self, explore=False):
        if explore:
            return random.choice([self.play(i)
                                  for i in range(9) if not self.grid[i]])
        max_value = -float('inf')
        for i in range(9):
            if not self.grid[i]:
                b = self.play(i)
                v = value(b)
                if v >= max_value:
                    max_value = v
                    max_board = b
        return max_board

    def display(self):
        symbols = {0: ' ', 1: 'X', -1: 'O'}
        print(' %s | %s | %s ' % (symbols[self.nw],
                                  symbols[self.n],
                                  symbols[self.ne]))
        print('---+---+---')
        print(' %s | %s | %s ' % (symbols[self.w],
                                  symbols[self.m],
                                  symbols[self.e]))
        print('---+---+---')
        print(' %s | %s | %s ' % (symbols[self.sw],
                                  symbols[self.s],
                                  symbols[self.se]))
        print()
        print()


def set_value(board, value):
    # 2 separate lists of [.5] constructed
    # .5 is the default value if not encounted before
    values[board.grid] = [value]
    for b in board.similar():
        values[b.grid] = values[board.grid]
    inverted = board.invert()
    values[inverted.grid] = [1 - value]
    for b in inverted.similar():
        values[b.grid] = values[inverted.grid]


def value(board):
    win = board.win()
    if win == 1:
        return 1
    if win == -1:
        return 0

    # List so that they point to the same number
    value, = values.get(board.grid, [None])
    if value is not None:
        return value
    inverted = board.invert()
    value, = values.get(inverted.grid, [None])
    if value is not None:
        return 1 - value

    set_value(board, .5)
    return .5


def update_value_by_temporal(previous, now):
    global alpha
    set_value(previous, (1 - alpha) * value(previous) + alpha * value(now))
    alpha *= decay


def game(update=False, explore_frequency=0, display=False):
    board = Board()
    while True:
        if display:
            board.display()
        if board.win() == -1:
            if display:
                print('Player loses')
            break
        if board.full():
            if display:
                print('Stale')
            break

        previous = board
        explore = (explore_frequency
                   and random.randint(0, explore_frequency) == 0)
        board = board.step(explore=explore)
        if update:
            update_value_by_temporal(previous, board)

        if display:
            board.display()
        if board.win() == 1:
            if display:
                print('Player wins')
            break
        if board.full():
            if display:
                print('Stale')
            break

        inverted = board.invert()
        previous = inverted
        explore = (explore_frequency
                   and random.randint(0, explore_frequency) == 0)
        inverted = inverted.step(explore=explore)
        if update:
            update_value_by_temporal(previous, inverted)

        board = inverted.invert()


def beat_the_human():
    board = Board()
    while True:
        board.display()
        if board.win() == -1:
            print('You lost')
            break
        if board.full():
            print('Stale')
            break

        position = int(input('Play at position (1 2 3; 4 5 6; 7 8 9): ')) - 1
        if board.grid[position]:
            raise ValueError('The position is already marked')
        board = board.play(position)

        board.display()
        if board.win() == 1:
            print('You win')
            break
        if board.full():
            print('Stale')
            break

        inverted = board.invert()
        inverted = inverted.step(explore=False)

        board = inverted.invert()


# Training
for i in range(10000):
    print('\rTraining: %d/10000' % i, end='')
    game(update=True, explore_frequency=random.randint(3, 10), display=False)
print()
print()

# Displayed testing
print('Simulated game')
print('--------------')
print()
game(update=False, explore_frequency=0, display=True)
print('\n')

# Gaming time
print('Beating you')
print('-----------')
print()
while True:
    beat_the_human()
