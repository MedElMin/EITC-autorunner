import numpy as np
from numpy import array
import pygame
from copy import deepcopy


class Obstacle:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size


class Platform:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size


def inside_rect(point, rect) -> bool:
    return rect[0] < point[0] < rect[0] + rect[2] and rect[1] < point[1] < rect[1] + rect[3]


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# physics constants
GRAVITY = 98.
GROUND_HEIGHT = screen.get_height() / 2

# Game constants
HORIZON = 1000
FENCE_INIT_DIST = 1000
LOOKAHEAD = 0.7

# Obstacle presets
FENCE = Obstacle(np.zeros(2), array([10, 10]))
TABLE = Platform(np.zeros(2), array([100, 1]))

# input map

# player
pos = array([100, 0], dtype=float)
vel = array([100, 0], dtype=float)
acc = array([0, 0], dtype=float)

# Obstacles
obstacles = []

# Camera
camera_pos = deepcopy(pos)

while running:
    delta = clock.get_time() / 100
    jumped = False

    # TODO: Add a buffer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_COMMA:
                # print("pressed comma")
                jumped = True

    # LOGIC
    # # Spawn obstacles
    i = 0
    while i < len(obstacles):
        if obstacles[i].pos[0] - camera_pos[0] < -obstacles[i].size[0] - 10:
            obstacles[i], obstacles[-1] = obstacles[-1], obstacles[i]
            obstacles.pop()
        else:
            i += 1

    if len(obstacles) == 0:
        fence = deepcopy(FENCE)
        fence.pos = array([pos[0], GROUND_HEIGHT])\
            + array([FENCE_INIT_DIST, 0])
        obstacles.append(fence)

    # # Physics
    if jumped and pos[1] == GROUND_HEIGHT:
        print("jump")
        vel[1] = -100

    acc = array([0., GRAVITY])
    vel += acc * delta
    pos += vel * delta

    # # # Collision
    if GROUND_HEIGHT < pos[1]:
        pos[1] = GROUND_HEIGHT
        vel[1] = min(0, vel[1])

    # circle_extremities = [pos + array([])]
    # for obstacle in obstacles:
    #     # detect collision
    #     # either a circle extremity is in the rect
    #     # or a rect corner is in the circle

    #     # if any()
    #     pass


    # DRAW
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")
    camera_pos[0] = pos[0] - screen.get_width() * (1 - LOOKAHEAD)

    pygame.draw.circle(screen,
                       (255, 200, 19),
                       pos - camera_pos,
                       10)
    for obstacle in obstacles:
        print("obstacle.pos - camera_pos", obstacle.pos - camera_pos)
        pygame.draw.rect(screen,
                         (200, 50, 50),
                         (obstacle.pos - camera_pos, obstacle.size))

    # BUG: This spot in code is not ideal, figure out where to put it, such that it changes nothing about the game logic, nor does it misrepresent something in game
    # if pos[0] > HORIZON:
    #     pos[0] -= HORIZON
    #     for obstacle in obstacles:
    #         obstacle.pos[0] -= 1000

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
