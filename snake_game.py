import pygame
import time
import random
import numpy as np



WIDTH, HEIGHT = 600, 300
INITIAL_LENGTH = 3
INITIAL_POS = (15, 15)
HEAD, BODY, APPLE = 1, 2, 3
SQUARE_SIZE = 15
GAME_SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)



class Square:
    def __init__(self, position=INITIAL_POS, typ='body', color=BLACK):
        self.position = position
        self.typ = typ
        self.color = color
        print(position)
        self.rect = pygame.rect.Rect(
            position[0], 
            position[1], 
            SQUARE_SIZE, 
            SQUARE_SIZE
        )

    def move(self, coord, absolute=False):
        if absolute:
            self.rect.x = coord[0]
            self.rect.y = coord[1]
            self.position = coord
        else:
            self.rect.move_ip(coord)
            self.position = (self.position[0] + coord[0],
                             self.position[1] + coord[1])

    def move_randomly(self):
        x = random.choice(range(0, WIDTH, SQUARE_SIZE))
        y = random.choice(range(0, HEIGHT, SQUARE_SIZE))
        self.rect.x = x
        self.rect.y = y
        self.position = (x, y)

class Snake:
    def __init__(self):
        self.alive = True
        self.length = INITIAL_LENGTH
        self.squares = self.spawn()
        self.head = self.squares[0]

    def __iter__(self):
        return iter(self.squares)
    
    def spawn(self):
        snake = [Square(INITIAL_POS, typ='head', color=GREEN)]
        # for _ in range(INITIAL_LENGTH-1):
        #     pos = self.get_valid_pos(snake)
        #     snake.append(Square(pos, typ='body'))
        return snake

    # def get_valid_pos(self, lst):
    #     last_sq = lst[-1]
    #     sec_last_sq = lst[-2]
    #     if last_sq.get_alignment(sec_last_sq) == "up":
    #         if last_sq.rect.top > SQUARE_SIZE:
    #             return (last_sq.rect.top-SQUARE_SIZE,
    #                     last_sq.rect.left)
    #         else:

    def collides(self):
        body_collision, edge_collision = 0, 0
        if (self.head.rect.top < -SQUARE_SIZE or
                self.head.rect.bottom > HEIGHT+SQUARE_SIZE or
                self.head.rect.left < -SQUARE_SIZE or
                self.head.rect.right > WIDTH+SQUARE_SIZE):
            return True

        for square in self.squares[1:]:
            if self.head.rect.colliderect(square.rect):
                return True
        else:
            return False
        
    def grow(self):
        self.length += 1
        # SPAWN NEW SQUARE

class Game:
    def __init__(self, width, height):
        self.score = 0
        self.speed = [0, SQUARE_SIZE]
        self.snake = Snake()
        self.apple = Square(typ='apple', color=RED)
        self.apple.move_randomly()

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(WHITE)
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                self.get_input(event)
            
            self.screen.fill(WHITE)
            self.render(self.apple)
            
            self.snake.squares[0].move(self.speed)
            self.render(self.snake.squares[0])
            for i, square in enumerate(self.snake.squares[1:]):
                coord_of_previous = (self.squares[i-1].x,
                                     self.squares[i-1].y)
                square.move(coord_of_previous, absolute=True)
                self.render(square)

            self.check_apple()
            if self.snake.collides():
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
                
    def check_apple(self):
        if self.snake.head.rect.colliderect(self.apple):
            self.snake.grow()
            self.apple.move_randomly()

    def render(self, square):
        pygame.draw.rect(self.screen, square.color, square.rect)


# if __name__ == '__main__':
#     Game(300, 300)

Game(WIDTH, HEIGHT)

