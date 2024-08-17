import pygame
import sys
import random

pygame.init()

width = 480
height = 480
grid_size = 20
GRID_WIDTH = width // grid_size
GRID_HEIGHT = height // grid_size



gray1 = (120, 120, 120)
gray2 = (170, 170, 170)
green = (0, 100, 0)
red = (255, 0, 0)
black = (0, 0, 0)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
font = pygame.font.Font('freesansbold.ttf', 30)

die_sound = pygame.mixer.Sound("die.ogg")
point_sound = pygame.mixer.Sound("point.ogg")

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((width // 2), (height // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = green

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
        
    def move(self):
        current = self.get_head_position()
        x, y = self.direction
        new = (((current[0] + (x * grid_size)) % width), (current[1] + (y * grid_size)) % height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
            return True
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return False

    def reset(self):
        self.length = 1
        self.positions = [((width // 2), (height // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect((pos[0], pos[1]), (grid_size, grid_size))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, black, rect, 1)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.turn(UP)
        elif keys[pygame.K_DOWN]:
            self.turn(DOWN)
        elif keys[pygame.K_LEFT]:
            self.turn(LEFT)
        elif keys[pygame.K_RIGHT]:   
            self.turn(RIGHT)

class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = red
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * grid_size, random.randint(0, GRID_HEIGHT - 1) * grid_size)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (grid_size, grid_size))
        pygame.draw.rect(surface, self.color, r)    
        pygame.draw.rect(surface, black, r, 1)

def background(surface):
    surface.fill((255,255,255))

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    snake.reset()
                    score = 0
                    game_over = False

        if not game_over:
            snake.handle_keys()
            game_over = snake.move()
            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 1
                point_sound.play()
                food.randomize_position()

        background(surface)
        snake.draw(surface)
        food.draw(surface)

        screen.blit(surface, (0, 0))

        if game_over:
            screen.fill((255,255,255))
            text = font.render("Game Over", True, red)
            screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
            restart_text = font.render("Press SPACE to restart", True, black)
            screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + text.get_height()))

        score_text = font.render("Score: {0}".format(score), True, black)
        screen.blit(score_text, (5, 10))

        pygame.display.update()
        clock.tick(10)

main()
