import pygame
import random
import time


# GAME CONSTANTS
WIDTH, HEIGHT = 600, 300
INITIAL_LENGTH = 3
INITIAL_POS = (15, 15)
INITIAL_APPLE_POS = (150, 150)
HEAD, BODY, APPLE = 1, 2, 3
SQUARE_SIZE = 15
CLOCK_SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)


class Square:
    '''A square object, representing either Snake bodyparts or the Apple'''
    
    def __init__(self, position=INITIAL_POS, static=False, color=BLACK):
        '''Initialize square attributes
        
        Args:
            position (tuple): position of square on screen
            static (bool): determines if square can move or not
            color (tuple): RBG color value
        '''
        self.static = static
        self.color = color
        self.rect = pygame.rect.Rect(
            position[0], 
            position[1], 
            SQUARE_SIZE, 
            SQUARE_SIZE
            )

    def move(self, coord, absolute=False):
        '''Move square object by `coord`

        Args:
            coord (tuple): coordinates of movement
            absolute (bool): determines if `coord` are to be considered
                relative to actual position (default), or in absolute
        '''
        self.rect.x += coord[0]
        self.rect.y += coord[1]
        if absolute:
            self.rect.x, self.rect.y = coord

    def move_randomly(self):
        '''Move square object to a random position'''
        self.rect.x = random.choice(range(0, WIDTH, SQUARE_SIZE))
        self.rect.y = random.choice(range(0, HEIGHT, SQUARE_SIZE))


class Snake:
    '''A Snake object, composed of a chain of Square objects'''

    def __init__(self):
        '''Initialize Snake with a head, and a growing attribute
        
        Params:
            growing (int): number of segments (squares) to add to snake
            head (Square): square object representing snake's head
            squares (list): list of Squares representing snake's bodyparts
        '''
        self.growing = INITIAL_LENGTH       
        self.head = Square(INITIAL_POS, color=GREEN, static=False)
        self.squares = []
    
    def dies(self):
        '''Check if snake head collides with screen edges or itself
        
        Returns:
            Boolean: snake dies or not
        '''
        edge_collision = (
            self.head.rect.x < 0 or
            self.head.rect.x > WIDTH or
            self.head.rect.y < 0 or
            self.head.rect.y > HEIGHT
            )
        if edge_collision:
            return True
        for square in self.squares:
            body_collision = self.head.rect.colliderect(square.rect)
            if body_collision:
                return True
        else:
            return False
        
    def move(self, speed):
        '''Move each snake bodypart that is not static.
        Squares are moved starting from the last, to the position of 
        the square that just precedes it. 
        First square is moved to head position.
        Finally, the head is moved according to current speed.
        
        Args:
            speed (tuple): relative coordinates used to move head
        '''
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
        self.head.move(speed, absolute=False)
    
    def grow(self):
        '''Check for growth, and grow the snake by one square if needed.
        If needed, a new static Square is spawned at the position of 
        the last square of the snake.
        If there are no bodyparts (only head), spawn new static
        square at head position instead.
        '''
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
    '''The actual Snake game'''

    def __init__(self, width, height):
        '''Initialise Game instance, and run main game loop.

        Args:
            width (int): screen width
            height (int): screen height
        
        Params:
            score (int): current score
            speed (list): how big square positions are incremented
            snake (Snake): the snake object
            apple (Square): a square representing the Apple
        '''
        self.score = 0
        self.speed = [0, SQUARE_SIZE]
        self.snake = Snake()
        self.apple = Square(position=INITIAL_APPLE_POS, color=RED)
        self.update_apple(init=True)

        pygame.init()
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(WHITE)

        while True:
            self.main_loop()
            clock.tick(CLOCK_SPEED)

    def main_loop(self):
        '''What happens every frame:
        Fill screen with background color,
        Check for QUIT event,
        Get player INPUT,
        Check if apple has been eaten,
        Check if snake is growing,
        Move the snake accordingly,
        Render apple and snake,
        Check for game over,
        Update display.
        '''
        self.screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            self.get_input(event)
        self.update_apple()
        self.snake.grow()            
        self.snake.move(self.speed)
        self.render(self.apple)
        self.render(self.snake.head)
        self.render(self.snake.squares)
        if self.snake.dies():
            time.sleep(2)
            pygame.quit()
        self.display_text(f'Score: {self.score}', 18, (0,0))
        pygame.display.update()

    def display_text(self, text, size, position):
        '''Print text to screen

        Args:
            text (str): message to display
            size (int): font size
            position (tuple): text coordinates on screen
        '''
        font = pygame.font.SysFont("arial", size)
        message = font.render(text, True, BLACK)
        self.screen.blit(message, position)
        pygame.display.update()
    
    def get_input(self, event):
        '''Get user input and adjust "speed" accordingly '''
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
        '''Move apple, increment `growing` and `score`.
        If snake's head collides with apple, increment `growing`
        and `score`, and move apple randomly.

        Args:
            init (bool): force random apple location without
                updating `score` or `growing`
        '''
        collision = self.snake.head.rect.colliderect(self.apple)
        if collision or init:
            self.apple.move_randomly()
        if collision:
            self.snake.growing += 1
            self.score += 1

    def render(self, items):
        '''Display an element or a list of elements on the screen
        
        Args:
            items (list/Square): a Square or a list of Squares to render
        '''
        if isinstance(items, list):
            for square in items:
                pygame.draw.rect(self.screen, square.color, square.rect)
        else:
            pygame.draw.rect(self.screen, items.color, items.rect)


if __name__ == '__main__':
    Game(WIDTH, HEIGHT)
