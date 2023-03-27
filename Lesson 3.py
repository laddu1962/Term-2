import math
import random
from pygame import mixer
import pygame
pygame.font.init()
from sys import exit
# sound
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# load sounds
laser_fx = pygame.mixer.Sound('audio.mp3')
laser_fx.set_volume(0.50)

# font
font30 = pygame.font.Font(None, 30)

# define game variables
rows = 6
cols = 5
alien_cooldown = 1000 # bullet cooldwon in milliseconds
last_alien_shot = pygame.time.get_ticks()


# define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# load image
background = pygame.image.load("Background.png")

w,h = background.get_size()
y = 0
y1 = -h

# score
score = 0
score_increment = 10


# implementing score
def draw_background():
    screen.blit(background, (0,0))


def rollingBackgrd():
    global y,y1,h
    screen.blit(background,(0,y))
    screen.blit(background,(0,y1))
    y += 1
    y1 += 1

    if y > h:
        y = -h
    if y1 > h:
        y1 = -h


# implementing score
def score_increase():
    global score
    global score_increment

    score += score_increment


# creating spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.baseImage = pygame.image.load("Ship.png")
        self.image = self.baseImage
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        self.acceleration = [0, 0]



    def update(self):
        # set movement speed
        speed = 0.1
        # cooldown variable
        cooldown = 300  # millisecond

        # rotate sprite to race acceleration
        angle = math.atan2(self.acceleration[0], self.acceleration[1])
        angle = angle * (180 / math.pi)
        self.image = pygame.transform.rotate(self.baseImage, 180 + angle)

        # get key press
        key = pygame.key.get_pressed()
        # left and right movement
        if key[pygame.K_LEFT]:
            self.acceleration[0] -= speed
            self.image = pygame.transform.rotate(self.image, -90)
        if key[pygame.K_RIGHT]:
            self.acceleration[0] += speed
        # stops ship from going off screen
        if self.rect.left <= 0 and self.acceleration[0] < 0 or self.rect.right >= screen_width and self.acceleration[0] > 0:
            self.acceleration[0] = 0

        self.rect.x += self.acceleration[0]
        # up and down movement
        if key[pygame.K_UP]:
            self.acceleration[1] -= speed
        if key[pygame.K_DOWN]:
            self.acceleration[1] += speed
        # stops ship at the edge of the screen [y] change number in the brackets for y-axis
        if self.rect.top <= 0 and self.acceleration[1] < 0 or self.rect.bottom >= screen_height and self.acceleration[1] > 0:
            self.acceleration[1] = 0

        self.rect.y += self.acceleration[1]

        # record time now
        time_now = pygame.time.get_ticks()
        # shooting
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # update mask
        self.mask = pygame.mask.from_surface(self.image)

        # draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            self.kill()
            quit()


# creating Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            explosion_group.add(Explosion(self.rect.x, self.rect.y))
            self.kill()
            laser_fx.play()
            score_increase()
            #add score


# creating Aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Invader" + str(random.randint(1, 6)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


# creating Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self,spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            # reduce spaceship health
            spaceship.health_remaining -= 1


# Explosion
explosion_group = pygame.sprite.Sprite()
explosion_images = []
for x in range(9):
    explosion_images.append(pygame.image.load('Archive/regularExplosion0' + str(x) + ".png"))


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.anim_index = 0
        self.current_frame = 0
        self.nr_frame_between = 10

    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.nr_frame_between:
            if self.anim_index < len(explosion_images) - 1:
                self.anim_index += 1
                self.image = explosion_images[self.anim_index]
            else:
                self.kill()


# create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_aliens():
    # generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)


create_aliens()

# create player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

run = True
while run:

    clock.tick(fps)

    # draw background
    draw_background()
    # rolling background
    rollingBackgrd()
    # displaying score
    screen.blit(font30.render('score: {}'.format(score), True, (255, 255, 255)), (10, 10))
    # text then brackets for the score.format(score)

    # create random alien bullets
    # record current time
    time_now = pygame.time.get_ticks()
    # shoot
    if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = time_now

    # update spaceship
    game_over = spaceship.update()

    # update sprite groups
    bullet_group.update()
    # alien_group.update()
    # alien_bullet_group.update()
    explosion_group.update()

    # draw sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    # alien_group.draw(screen)
    # alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
