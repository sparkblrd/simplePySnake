from random import randrange
import pygame

CELL_NUMBER = 16
SIZE = 10
RES = CELL_NUMBER * SIZE

class SnakeGameAI:
    def __init__(self):
        pygame.init()
        self.sc = pygame.display.set_mode([RES, RES], pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.reset()

    def spawnApple(self, snake):
        while True:
            apple = (
                randrange(0, RES, SIZE),
                randrange(0, RES, SIZE)
            )
            if apple not in snake:
                return apple
            
    def reset(self):
        self.direction = "RIGHT"
        self.x, self.y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
        self.snake = [(self.x, self.y)]
        self.length = 1
        self.score = 0
        self.apple = self.spawnApple(self.snake)
        self.game_over = False
    
    def playStep(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        reward = 0
        self.move(action)
        self.snake.append((self.x, self.y))
        self.snake = self.snake[-self.length:]

        if self.isCollision():
            reward = -10
            self.game_over = True
            return reward, self.game_over, self.score

        if (self.snake[-1]) == self.apple:
                self.length += 1
                self.score += 1
                reward = 10
                self.apple = self.spawnApple(self.snake)

        self.draw()
        self.clock.tick(10)
        return reward, self.game_over, self.score
    
    def move(self, action):
        directions = ["RIGHT", "DOWN", "LEFT", "UP"]
        index = directions.index(self.direction)

        if action == [1, 0, 0]:
            new_direction = directions[index]
        elif action == [0, 1, 0]:
            new_direction = directions[(index + 1) % 4]
        else:
            new_direction = directions[(index - 1) % 4]

        self.direction = new_direction

        if self.direction == "RIGHT":
            self.x += SIZE
        elif self.direction == "LEFT":
            self.x -= SIZE
        elif self.direction == "DOWN":
            self.y += SIZE
        elif self.direction == "UP":
            self.y -= SIZE

    def isCollision(self, point=None):
        if point is None:
            point = (self.x, self.y)

        x, y = point

        if x < 0 or x > RES - SIZE:
            return True
        if y < 0 or y > RES - SIZE:
            return True
        if point in self.snake[:-1]:
            return True

        return False
    
    def draw(self):
        self.sc.fill(pygame.Color("black"))

        for i, j in self.snake:
            pygame.draw.rect(self.sc, pygame.Color("green"), (i, j, SIZE, SIZE))

        pygame.draw.rect(self.sc, pygame.Color("red"), (*self.apple, SIZE, SIZE))

        pygame.display.flip()