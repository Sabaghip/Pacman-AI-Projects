import numpy as np

player_moves = {
    'L': np.array([-1., 0.]),
    'R': np.array([1., 0.]),
    'U': np.array([0., -1.]),
    'D': np.array([0., 1.])
}
initial_player_size = 4


class SnakeClass(object):
    def __init__(self, grid_size):
        self.pos = np.array([grid_size // 2, grid_size // 2]).astype('float')
        self.dir = np.array([1., 0.])
        self.len = initial_player_size
        self.prev_pos = [np.array([grid_size // 2, grid_size // 2]).astype('float')]
        self.grid_size = grid_size

    def move(self):
        self.pos += self.dir
        self.prev_pos.append(self.pos.copy())
        self.prev_pos = self.prev_pos[-self.len - 1:]

    def check_dead(self, pos):
        if pos[0] <= -1 or pos[0] >= self.grid_size:
            return True
        elif pos[1] <= -1 or pos[1] >= self.grid_size:
            return True
        elif list(pos) in [list(item) for item in self.prev_pos[:-1]]:
            return True
        else:
            return False

    def get_proximity(self):
        L = self.pos - np.array([1, 0])
        R = self.pos + np.array([1, 0])
        U = self.pos - np.array([0, 1])
        D = self.pos + np.array([0, 1])
        poss_directions = [L, R, U, D]
        proximity = [int(self.check_dead(x)) for x in poss_directions]
        return proximity

    def __len__(self):
        return self.len + 1


class AppleClass(object):
    def __init__(self, grid_size):
        self.pos = np.random.randint(1, grid_size, 2)
        self.score = 0
        self.grid_size = grid_size

    def eaten(self):
        self.pos = np.random.randint(1, self.grid_size, 2)
        self.score += 1


class GameEnvironment(object):
    def __init__(self, grid_size, nothing, dead, apple):
        self.snake = SnakeClass(grid_size)
        self.apple = AppleClass(grid_size)
        self.game_over = False
        self.grid_size = grid_size
        self.reward_nothing = nothing
        self.reward_dead = dead
        self.reward_apple = apple
        self.time_since_apple = 0

    def reset_game(self):
        self.apple.pos = np.random.randint(1, self.grid_size, 2).astype('float')
        self.apple.score = 0
        self.snake.pos = np.random.randint(1, self.grid_size, 2).astype('float')
        self.snake.prev_pos = [self.snake.pos.copy().astype('float')]
        self.snake.len = initial_player_size
        self.game_over = False

    def get_board_state(self):
        return [self.snake.pos, self.snake.dir, self.snake.prev_pos, self.apple.pos, self.apple.score, self.game_over]

    def update_board_state(self, move):
        reward = self.reward_nothing
        Done = False

        if move == 0:
            if not (self.snake.dir == player_moves['R']).all():
                self.snake.dir = player_moves['L']
        if move == 1:
            if not (self.snake.dir == player_moves['L']).all():
                self.snake.dir = player_moves['R']
        if move == 2:
            if not (self.snake.dir == player_moves['D']).all():
                self.snake.dir = player_moves['U']
        if move == 3:
            if not (self.snake.dir == player_moves['U']).all():
                self.snake.dir = player_moves['D']

        self.snake.move()
        self.time_since_apple += 1

        if self.time_since_apple == 100:
            self.game_over = True
            reward = self.reward_dead
            self.time_since_apple = 0
            Done = True

        if self.snake.check_dead(self.snake.pos):
            self.game_over = True
            reward = self.reward_dead
            self.time_since_apple = 0
            Done = True

        elif (self.snake.pos == self.apple.pos).all():
            self.apple.eaten()
            self.snake.len += 1
            self.time_since_apple = 0
            reward = self.reward_apple

        len_of_snake = len(self.snake)

        return reward, Done, len_of_snake
