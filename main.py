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
            self.xpos = random.randrange(0, screen.get_size()[0])

    def Draw(self):
        pygame.draw.circle(screen, ('Blue'), (self.xpos, self.ypos), 5)

drop = Raindrop(100, 200)

drops = []
for x in range(10):
    random_x = random.randrange(0, screen.get_size()[0])
    random_y = random.randrange(0, screen.get_size()[1])
    drops.append(Raindrop(random_x, random_y))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.fill((255,229,180))  # colours using RGB

    # raindrop
    for drop in drops:
        drop.Draw()
        drop.Move()

    pygame.display.flip()  # Display flip isn#t required
    pygame.display.update()
    clock.tick(60)




