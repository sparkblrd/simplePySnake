import pygame
from random import randrange

def resetGame():
    global x, y, snake, length, dx, dy, next_dx, next_dy, fps, score, apple, game_over
    x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
    snake = [(x,y)]
    length = 1
    dx, dy = 0, 0
    next_dx, next_dy = 0, 0
    fps = 5
    score = 0
    apple = spawnApple(snake)
    game_over = False

def spawnApple(snake):
    while True:
        apple = (
            randrange(0, RES, SIZE),
            randrange(0, RES, SIZE)
        )
        if apple not in snake:
            return apple
        
RES = 800
SIZE = 50
GREEN = pygame.Color("green")
RED = pygame.Color("red")
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")

resetGame()

pygame.init()
font = pygame.font.SysFont("Arial", 50)
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    resetGame()

            else:
                if event.key == pygame.K_w and dy != 1:
                    next_dx, next_dy = 0, -1

                elif event.key == pygame.K_s and dy != -1:
                    next_dx, next_dy = 0, 1

                elif event.key == pygame.K_a and dx != 1:
                    next_dx, next_dy = -1, 0

                elif event.key == pygame.K_d and dx != -1:
                    next_dx, next_dy = 1, 0

    if game_over:
        sc.fill(BLACK)

        text = font.render("GAME OVER", True, RED)
        text_score = font.render(f"Score: {score}", True, WHITE)
        restart_text = font.render("Press R to restart", True, WHITE)

        sc.blit(text, (RES // 2 - text.get_width() // 2, RES // 2 - 80))
        sc.blit(text_score, (RES // 2 - text_score.get_width() // 2, RES // 2 - 30))
        sc.blit(restart_text, (RES // 2 - restart_text.get_width() // 2, RES // 2 + 20))

        pygame.display.flip()
        clock.tick(10)
        continue

    sc.fill(BLACK)
    for i, j in snake:
        pygame.draw.rect(sc, GREEN, (i, j, SIZE, SIZE))
    pygame.draw.rect(sc, RED, (*apple, SIZE, SIZE))

    dx, dy = next_dx, next_dy
    x += dx * SIZE
    y += dy * SIZE

    snake.append((x, y))
    snake = snake[-length:]

    if snake[-1] == apple:
        length += 1
        fps += 1
        score += 1

        apple = spawnApple(snake)

    if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
        game_over = True

    pygame.display.flip()
    clock.tick(fps)