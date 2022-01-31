from tkinter import SCROLL
from turtle import window_width
import pygame
import os
import random
import csv

pygame.init()

SCREEN_WIDTH = 1216
SCREEN_HEIGHT = SCREEN_WIDTH * 0.6

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 0.75
SCROLL_THRESH = 300
ROWS = 16
COLUMNS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 27
screen_scroll = 0
bg_scroll = 0
level = 1

# define colours
BLUE = (0,128,255)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)

# define player action variables
moving_left = False
moving_right = False
shoot = False
tv = False
tv_thrown = False

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f"Assets/level_editor/img/tile/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Room Game")

# load images
pine1_img = pygame.image.load('Assets/level_editor/img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('Assets/level_editor/img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('Assets/level_editor/img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('Assets/level_editor/img/Background/sky_cloud.png').convert_alpha()

#football
football_img = pygame.image.load('Assets/projectiles/football.png').convert_alpha()
football_img = pygame.transform.scale(football_img, (int(football_img.get_width() * 1.5), int(football_img.get_height() * 1.5)))
#tv
tv_img = pygame.image.load('Assets/projectiles/tv.png').convert_alpha()
tv_img = pygame.transform.scale(tv_img, (int(tv_img.get_width() * 1.5), int(tv_img.get_height() * 1.5)))
#pickup boxes
tv_box_img = pygame.image.load('Assets/item_boxes/tv_box.png').convert_alpha()
tv_box_img = pygame.transform.scale(tv_box_img, (int(tv_box_img.get_width() * 0.5), int(tv_box_img.get_height() * 0.5)))
health_box_img = pygame.image.load('Assets/item_boxes/health_box.png').convert_alpha()
health_box_img = pygame.transform.scale(health_box_img, (int(health_box_img.get_width() * 0.5), int(health_box_img.get_height() * 0.5)))
item_boxes = {
    'TV': tv_box_img,
    'Health': health_box_img
}

#define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.fill(BLUE)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x*width) - bg_scroll*0.5,0))
        screen.blit(mountain_img, ((x*width) - bg_scroll*0.6,SCREEN_HEIGHT-mountain_img.get_height()-300))
        screen.blit(pine1_img, ((x*width) - bg_scroll*0.7,SCREEN_HEIGHT-pine1_img.get_height()-150))
        screen.blit(pine2_img, ((x*width) - bg_scroll*0.8,SCREEN_HEIGHT-pine2_img.get_height()))

class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, tvs):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.ammo = ammo
        self.start_ammo = ammo
        self.tvs = tvs
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.jump = False
        self.in_air = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #create ai specific variables
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0,0,300,20)

        animation_types = ['idle','running','jumping', 'death']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'Assets/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'Assets/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0
        
        # assign movement variables
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check for collision
        for tile in world.obstacle_list:
            #check in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground (jumping)
                if self.vel_y < 0:#jumping
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground (falling)
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom


        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.char_type == 'player':
            if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH or self.rect.left < SCROLL_THRESH:
                self.rect.x -= dx
                screen_scroll = -dx
        
        return screen_scroll


    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 30
            projectile = Projectile(self.rect.centerx + (self.rect.size[0] * 1 * self.direction), self.rect.centery, self.direction)
            projectile_group.add(projectile)
            self.ammo -= 1

    def ai(self):
        if self.alive and tommy.alive:
            if random.randint(1,200) == 1 and self.idling_counter == 0:
                self.idling = True
                self.update_action(0) #idle
                self.idling_counter = 50
            for tile in world.obstacle_list:
            #check in the x direction
                if tile[1].colliderect(self.rect.right, self.rect.y, self.width, self.height) and self.direction == 1:
                    self.direction *= -1
                if tile[1].colliderect(self.rect.left-5, self.rect.y, self.width, self.height) and self.direction == -1:
                    self.direction *= -1
            #check if the ai is near the player
            if self.vision.colliderect(tommy.rect):
                #stop running and face the player
                self.update_action(0)#idle
                #shoot
                self.shoot()
            else:

                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False

                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1 run
                    self.move_counter += 1
                    # update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 150 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE * 5:
                        self.direction*=-1
                        self.move_counter *=-1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter == 0:
                        self.idling = False
                        self.update_action(1) #running
            
            #scroll
            self.rect.x += screen_scroll


    def update_animation(self):
        # update animation
        if self.char_type == "player":
            ANIMATION_COOLDOWN = 50 
        else:
            ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset the index
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        #shows the rectangle around the sprite as a red border
        #pygame.draw.rect(screen, RED, self.rect, 1)

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        #iterate through each value in data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile>= 0 and tile < 1:
                        self.obstacle_list.append(tile_data)
                    #elif tile >= x and tile <= y: 
                    #   pass(water)
                    #    water = Water(img, x*TILE_SIZE, y*TILE_SIZE)
                    #    water_group.add(water)
                    elif tile >=1 and tile<=22:
                        decoration = Decoration(img, x*TILE_SIZE, y*TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 25: #create tommy
                        tommy = Character('player',x*TILE_SIZE,y*TILE_SIZE, 2,5,100000, 5)
                        health_bar = HealthBar(10,10,tommy.health, tommy.health)
                    elif tile == 23:
                        enemy = Character('enemy',x*TILE_SIZE,y*TILE_SIZE, 1,3,500,0)
                        enemy_group.add(enemy)             
                    elif tile == 26:#tv box
                        item_box = ItemBox('TV', x*TILE_SIZE, y*TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 24:#health box
                        item_box = ItemBox('Health', 20, 260)
                        item_box_group.add(item_box)
                    #elif tile == x:#exit
                    #    exit = Exit(img, x*TILE_SIZE, y*TILE_SIZE)
                    #    exit_group.add(decoration)                   
        return tommy, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+TILE_SIZE // 2, y+(TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+TILE_SIZE // 2, y+(TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+TILE_SIZE // 2, y+(TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()) )

    def update(self):
        #scroll
        self.rect.x += screen_scroll
        #check for collision
        if pygame.sprite.collide_rect(self, tommy):
            if self.item_type == "TV":
                self.kill()
                tommy.tvs += 5
            if self.item_type == "Health" and tommy.health < tommy.max_health:
                self.kill()
                tommy.health += 25
                if tommy.health > tommy.max_health:
                    tommy.health = tommy.max_health

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    
    def draw(self, health):
        #update with new health
        self.health = health
        #calculate health ratio
        ratio = tommy.health/tommy.max_health
        #draw health bars
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150,20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.image = football_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #check for collision with obstacles
        for tile in world.obstacle_list:
            #check in the x direction
            if tile[1].colliderect(self.rect):
                self.kill()
        #check if bullet has gone off screen
        if self.rect.x > SCREEN_WIDTH or self.rect.x < 0:
            self.kill()
        #check for collision with characters
        if pygame.sprite.spritecollide(tommy, projectile_group, False):
            if tommy.alive:
                tommy.health -= 10
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, projectile_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    print(enemy.health)
                    self.kill()


class Television(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 5
        self.vel_y = -7
        self.speed = 10
        self.image = tv_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y


        #check collision with floor
        # check for collision
        for tile in world.obstacle_list:
            #check in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                self.kill()
                explosion = Explosion(self.rect.x, self.rect.y, 1.5)
                explosion_group.add(explosion)
            #check in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground (jumping)
                if self.vel_y < 0:#thrown
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    self.kill()
                    explosion = Explosion(self.rect.x, self.rect.y, 1.5)
                    explosion_group.add(explosion)
                #check if above the ground (falling)
                if self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
                    self.kill()
                    explosion = Explosion(self.rect.x, self.rect.y, 1.5)
                    explosion_group.add(explosion)

        
            
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, tv_group, False):
                if enemy.alive:
                    enemy.health -= 100
                    self.kill()
                    explosion = Explosion(self.rect.x, self.rect.y, 1.5)
                    explosion_group.add(explosion)

        #check collision with walls
        if self.rect.left + dx < 0:
            self.direction *= -1
            dx = self.direction * self.speed
        #update grenade position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        #countdown timer
        self.timer -= 5

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(0, 16):
            img = pygame.image.load(f'Assets/projectiles/explosion/{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        #scroll
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        #update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index == len(self.images) - 1:
                self.kill()
            else:
                self.image = self.images[self.frame_index]


        if pygame.sprite.spritecollide(enemy, explosion_group, False) and self.frame_index<=14:
            if enemy.alive:
                enemy.health -= 100
                print(enemy.health)
        
        if pygame.sprite.spritecollide(tommy, explosion_group, False) and self.frame_index<=10:
            tommy.health -= 25
            self.kill()


#create sprite groups
projectile_group = pygame.sprite.Group()
tv_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLUMNS
    world_data.append(r)
#load in level data and create world

with open(f"level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x,row in enumerate(reader):
        for y,tile in enumerate(row):   
            world_data[x][y] = int(tile)
world = World()
tommy,health_bar = world.process_data(world_data)
run = True

while run:
    clock.tick(FPS)
    #update background
    draw_bg()
    #draw world map
    world.draw()
    #show player health
    health_bar.draw(tommy.health)
    #show ammo
    draw_text("TVS:", font, RED, 10, 45)
    for x in range(tommy.tvs):
        screen.blit(pygame.transform.scale(
            tv_img, (int(tv_img.get_width() * 0.5), int(tv_img.get_height() * 0.5))), (65+x * 30, 40))
    tommy.update()
    tommy.draw()
    for enemy in enemy_group:
        enemy.update()
        enemy.draw()
        enemy.ai()

    #update and draw groups
    projectile_group.update()
    tv_group.update()
    explosion_group.update()
    item_box_group.update()
    decoration_group.update()
    water_group.update()
    exit_group.update()
    projectile_group.draw(screen)
    tv_group.draw(screen)
    explosion_group.draw(screen)
    item_box_group.draw(screen)
    decoration_group.draw(screen)
    water_group.draw(screen)
    exit_group.draw(screen)

    # update player actions
    if tommy.alive:
        #shoot projectile
        if shoot:
            tommy.shoot()
        elif tv and tv_thrown == False and tommy.tvs > 0:
            tv = Television(
                tommy.rect.centerx + (tommy.rect.size[0] * 0.8), tommy.rect.top, tommy.direction)
            tv_group.add(tv)
            #reduce grenades
            tv_thrown = True
            tommy.tvs -= 1
            print(tommy.tvs)
        if tommy.in_air:
            tommy.update_action(2) # 2 for jump
        elif moving_left or moving_right:
            tommy.update_action(1) # 1 means run
        else:
            tommy.update_action(0) # 0 means idle
        screen_scroll = tommy.move(moving_left, moving_right)
        bg_scroll -= screen_scroll

    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            run = False

        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and tommy.alive:
                tommy.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

        #mouse presses
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                shoot = True
            if event.button == 3:
                tv = True

        #mouse button released
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                shoot = False
            if event.button == 3:
                tv = False
                tv_thrown = False

    pygame.display.update()

pygame.quit()
