import pygame
import time
import random
import numpy as np



WIDTH, HEIGHT = 600, 300
INITIAL_LENGTH = 3
INITIAL_POS = (15, 15)
INITIAL_APPLE_POS = (150, 150)
HEAD, BODY, APPLE = 1, 2, 3
SQUARE_SIZE = 15
GAME_SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)



class Square:
    def __init__(self, position=INITIAL_POS, static=False, color=BLACK):
        self.static = static
        self.color = color
        self.rect = pygame.rect.Rect(
            position[0], 
            position[1], 
            SQUARE_SIZE, 
            SQUARE_SIZE
            )

    def move(self, coord, absolute=False):
        self.rect.x += coord[0]
        self.rect.y += coord[1]
        if absolute:
            self.rect.x = coord[0]
            self.rect.y = coord[1]

    def move_randomly(self):
        x = random.choice(range(0, WIDTH, SQUARE_SIZE))
        y = random.choice(range(0, HEIGHT, SQUARE_SIZE))
        self.rect.x = x
        self.rect.y = y



class Snake:
    def __init__(self):
        self.growing = INITIAL_LENGTH       
        self.head = Square(INITIAL_POS, color=GREEN, static=False)
        self.squares = []

    def __iter__(self):
        return iter(self.squares)
    
    def dies(self):
        if (self.head.rect.x < 0 or
                self.head.rect.x > WIDTH or
                self.head.rect.y < 0 or
                self.head.rect.y > HEIGHT):
            return True
        for square in self.squares[1:]:
            if self.head.rect.colliderect(square.rect):
                return True
        else:
            return False
        
    def move(self, coord):
        for i, square in enumerate(reversed(self.squares)):
            if square.static:
                square.static = False
            else:
                if i+1 == len(self.squares):
                    coord_of_previous = (self.head.rect.x,
                                         self.head.rect.y)
                else:
                    coord_of_previous = (self.squares[-i-2].rect.x,
                                         self.squares[-i-2].rect.y)
                square.move(coord_of_previous, absolute=True)
        self.head.move(coord, absolute=False)
    

    def grow(self):
        if self.growing > 0:
            if not self.squares:
                coord_of_last = (self.head.rect.x,
                                 self.head.rect.y)
            else:
                coord_of_last = (self.squares[-1].rect.x,
                                 self.squares[-1].rect.y)
            self.squares.append(
                Square(position=coord_of_last, static=True)
                )
            self.growing -= 1


class Game:
    def __init__(self, width, height):
        self.score = 0
        self.speed = [0, SQUARE_SIZE]
        self.snake = Snake()
        self.apple = Square(position=INITIAL_APPLE_POS, color=RED)
        self.update_apple()

        pygame.init()
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(WHITE)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                self.get_input(event)
            
            self.screen.fill(WHITE)
            
            self.update_apple()
            self.snake.grow()            
            self.snake.move(self.speed)

            self.render(self.apple)
            self.render(self.snake.head)
            self.render(self.snake.squares)
            
            if self.snake.dies():
                pygame.quit()
            pygame.display.update()
            
            clock.tick(GAME_SPEED)

    def get_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.speed = [0, -SQUARE_SIZE]
            if event.key == pygame.K_DOWN:
                self.speed = [0, SQUARE_SIZE]
            if event.key == pygame.K_LEFT:
                self.speed = [-SQUARE_SIZE, 0]
            if event.key == pygame.K_RIGHT:
                self.speed = [SQUARE_SIZE, 0]
                
    def update_apple(self, init=False):
        collision = self.snake.head.rect.colliderect(self.apple)
        if collision or init:
            self.apple.move_randomly()
        if collision:
            self.snake.growing += 1
            self.score += 1

    def render(self, items):
        if isinstance(items, list):
            for square in items:
                pygame.draw.rect(self.screen, square.color, square.rect)
        else:
            pygame.draw.rect(self.screen, items.color, items.rect)


# if __name__ == '__main__':
#     Game(300, 300)

Game(WIDTH, HEIGHT)

