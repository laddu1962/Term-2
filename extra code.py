import random

import pygame
from sys import exit


pygame.init()
pygame.display.set_caption("Hello World")
screen = pygame.display.set_mode((1080, 960))
clock = pygame.time.Clock()

# circle
xpos = 100
ypos = 100
moving_down = False

# rain drop
raindrop_y = 0
raindrop_speed =1

centre_x = list(screen.get_size())[0]/2


class Raindrop:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.raindrop_y = 0
        self.raindrop_speed = 1

    def Move(self):
        self.ypos += self.raindrop_speed
        self.raindrop_speed += 1
        if self.ypos > list(screen.get_size())[1]:
            self.ypos = 0
            self.raindrop_speed = 1

    def Draw(self):
        pygame.draw.circle(screen, ('Blue'), (self.xpos, self.ypos), 5)

drop = Raindrop(100, 200)

random_x = random.randrange(0, screen.get_size()[0])


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            moving_down = False
        if event.type == pygame.KEYUP and event.key == pygame.K_0:
            moving_down = True

    screen.fill((90,90,90))  # colours using RGB
    pygame.draw.circle(screen, (255,229,180), (xpos,ypos), 10)  # circle(surface, colour, position, radius, width=0)

    # centre the raindrop
    print(list(screen.get_size())[0]/2)

    # raindrop
    drop.Draw()
    drop.Move()


    circle = pygame.draw.circle(screen, ('Blue'), (centre_x, raindrop_y), 5)
    raindrop_y += raindrop_speed
    raindrop_speed += 1

    if raindrop_y > list(screen.get_size())[0]:  # resets the raindrop when it hits the bottom of the screen
        raindrop_y = 0
        raindrop_speed = 1

    pressed_key = pygame.key.get_pressed()  # movement of the circle though key press
    # x position
    if pressed_key[pygame.K_RIGHT]:  # for specific key
        xpos += 1  # moving the circle for x position
    # y position
    if moving_down:
        ypos += 2  # moving the circle for x position

    # raindrop, if you want this to work turn off all other press key code
    ypos += 2

    pygame.display.flip()  # Display flip isn#t required
    pygame.display.update()
    clock.tick(60)