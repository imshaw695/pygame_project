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
ROWS = 16
COLUMNS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 27
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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Room Game")

# load images

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
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

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

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
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

        # check collision with the floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

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

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()) )

    def update(self):
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
        self.speed = 5
        self.image = football_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
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

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y


        #check collision with floor
        if self.rect.bottom > 300 :
            dy = 300 - self.rect.bottom
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
        if self.rect.right + dx > SCREEN_WIDTH or self.rect.left + dx < 0:
            self.direction *= -1
            dx = self.direction * self.speed
        #update grenade position
        self.rect.x += dx
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


        if pygame.sprite.spritecollide(enemy, explosion_group, False):
            if enemy.alive:
                enemy.health -= 100
                print(enemy.health)
        
        if pygame.sprite.spritecollide(tommy, explosion_group, False):
            tommy.health -= 25
            self.kill()


#create sprite groups
projectile_group = pygame.sprite.Group()
tv_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

#temporary - create item boxes
item_box = ItemBox('TV', 100, 260)
item_box_group.add(item_box)
item_box = ItemBox('Health', 20, 260)
item_box_group.add(item_box)


tommy = Character('player',200,200, 2,5,100000, 5)
health_bar = HealthBar(10,10,tommy.health, tommy.health)
enemy = Character('enemy',500,250, 0.25,3,500,0)
enemy2 = Character('enemy',700,250, 0.25,3,500,0)
enemy_group.add(enemy)
enemy_group.add(enemy2)

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

 

run = True

while run:
    clock.tick(FPS)
    draw_bg()
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
    projectile_group.draw(screen)
    tv_group.draw(screen)
    explosion_group.draw(screen)
    item_box_group.draw(screen)

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
        tommy.move(moving_left, moving_right)

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
