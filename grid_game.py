import pygame
import numpy
from color import Color

class CliffWalker():
    def __init__(self, dim_x = 12, dim_y = 4):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.grid = numpy.zeros([dim_x, dim_y])

        self.player_x = 0
        self.player_y = 0
        self.goal_x = dim_x - 1
        self.goal_y = 0

        self.width = 960
        self.height = 540
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.render_size = 40
        self.render_spacing = 5
        s = self.render_size
        sp = self.render_spacing

        self.player = pygame.Rect((0, 0, s, s))
        self.goal = pygame.Rect((0, 0, s, s))

        self.score = 0
        self.steps = 0
        self.max_steps = 3000

        for n in range(1, self.dim_x - 1):
            self.grid[n][0] = -1
        self.grid[dim_x - 1][0] = 1
        # print(self.grid)

    def render(self):
        screen = self.screen
        screen.fill(Color.black)

        s = self.render_size
        sp = self.render_spacing

        for x in range(0, self.dim_x):
            for y in range (0, self.dim_y):
                if self.grid[x][y] == 0:
                    pygame.draw.rect(screen, Color.light_grey, pygame.Rect((x*(s+sp), y*(s+sp), s, s)))
                else:
                    pygame.draw.rect(screen, Color.dark_grey, pygame.Rect((x*(s+sp), y*(s+sp), s, s)))

        self.player.x = self.player_x * (s+sp)
        self.player.y = self.player_y * (s+sp)
        self.goal.x = self.goal_x * (s+sp)
        self.goal.y = self.goal_y * (s+sp)
        pygame.draw.rect(screen, Color.blue, self.goal)
        pygame.draw.rect(screen, Color.green, self.player)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def move(self, action):
        x = self.player_x
        y = self.player_y

        # action = [up, right, down, left]
        up = bool(action[0])
        right = bool(action[1])
        down = bool(action[2])
        left = bool(action[3])

        if (up):
            y -= 1
        elif(right):
            x += 1
        elif(down):
            y += 1
        elif(left):
            x -= 1

        if (x >= 0 and y >= 0 and x < self.dim_x and y < self.dim_y):
            self.player_x = x
            self.player_y = y

    def get_user_input(self):
        key = pygame.key.get_pressed()
        action = [0, 0, 0, 0]

        if key[pygame.K_UP]:
            action[0] = 1
        elif key[pygame.K_RIGHT]:
            action[1] = 1
        elif key[pygame.K_DOWN]:
            action[2] = 1
        elif key[pygame.K_LEFT]:
            action[3] = 1

        return action

    def get_reward(self):
        reward = 0

        if (self.check_death()):
            reward = -100
        elif(self.check_win()):
            reward = +30
        else:
            reward = -1

        return reward
    
    def check_win(self):
        return (self.grid[self.player_x][self.player_y] == 1)
    
    def check_death(self):
        return (self.grid[self.player_x][self.player_y] == -1)

    def reset(self):
        self.player_x = 0
        self.player_y = 0
        self.score = 0
        self.steps = 0

    def step(self, action):
        done = False

        self.move(action)
        reward = self.get_reward()

        if (self.check_win() or self.check_death() or self.steps > self.max_steps):
            done = True

        if (self.check_win()):
            self.score = 1

        self.render()

        self.steps += 1
        return (reward, done, self.score)

# clock = pygame.time.Clock()
# game = CliffWalker()

# run = True
# while run:
#     action = game.get_user_input()
#     reward, done, score = game.step(action)
#     clock.tick(10)

#     if done:
#         if (score > 0):
#             print('You won! :-)')
#         else:
#             print('You lost :(')
#         game.reset()

# pygame.quit()
# quit()