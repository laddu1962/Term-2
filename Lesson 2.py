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

# human
human_image = pygame.image.load('Ship.png')
human_image.set_colorkey((255, 255, 255))
human_rect = human_image.get_rect(topleft=(540,500))

# cloud
cloud_image = pygame.image.load('cloud.png')
cloud_x = screen.get_size()[1]/2
cloud_y = 0


class Raindrop:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.raindrop_y = 0
        self.raindrop_speed = 1
        self.size = random.randrange(3, 5)

        self.rect = pygame.Rect(self.xpos, self.ypos, self.size, self.size)
        self.active = True

    def Move(self):
        self.ypos += self.raindrop_speed
        self.rect.y = self.ypos
        self.rect.x = self.xpos
        self.raindrop_speed += 1

        if self.rect.colliderect(human_rect):
            self.active = False

        if self.ypos > list(screen.get_size())[1]:
            y_min = cloud_y + cloud_image.get_size()[1] / 2
            y_max = cloud_y + cloud_image.get_size()[1]
            self.ypos = random.randrange(200, 700)
            self.raindrop_speed = 1
            range = cloud_image.get_size()[0]
            self.xpos = random.randrange(cloud_x, cloud_x + range)
            self.active = True

    def Draw(self):
        if self.active:
            pygame.draw.circle(screen, ('Blue'), (self.xpos, self.ypos), 5)


drop = Raindrop(100, 200)

drops = []
for x in range(50):
    random_x = random.randrange(cloud_x, cloud_x + cloud_image.get_size()[0])
    y_min = cloud_y + cloud_image.get_size()[1] / 2
    y_max = cloud_y + cloud_image.get_size()[1]
    random_y = random.randrange(cloud_y, 700)
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

    screen.blit(cloud_image, (0,-150))
    screen.blit(human_image, human_rect)



    pygame.display.flip()  # Display flip isn#t required
    pygame.display.update()
    clock.tick(60)




