import pygame
import os

# To make it clear, set your width and height as variables first
WIDTH, HEIGHT = 1100, 800


# Now you can set the size of your window using those variables in a tuple, where the 1st is width and 2nd is height
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# This method sets what is written at the top of the window
pygame.display.set_caption("Tutorial Game")

# Colours for the background are always done in RGB
BLUE =  (0,128,255)

# Set desired frames per second
FPS = 60
VEL = 3

# Import the images
TOMMY_WISEAU_IMAGE = pygame.image.load(
    os.path.join('Assets','tommy.png'))

background = pygame.image.load(os.path.join("Assets", "background.png")).convert()
TKY = pygame.image.load(os.path.join("Assets", "tky.png"))
SAL = pygame.image.load(os.path.join("Assets", "sal.png"))

TOMMY_WISEAU_REVERSE_IMAGE = pygame.transform.flip(TOMMY_WISEAU_IMAGE, True, False)
TKY_REVERSE_IMAGE = pygame.transform.flip(TKY, True, False)


# Now you create your function for main
def main():

    backgroundX = 0
    backgroundX2 = background.get_width()

    isJump = False
    jumpCount = 10
    tommy = pygame.Rect(350, 500, 54, 201)
    turkey = pygame.Rect(900, 551, 132, 150)

    if backgroundX < background.get_width() * -1:
        backgroundX = background.get_width()
    if backgroundX2 < background.get_width() * -1:
        backgroundX2 = background.get_width()


    clock = pygame.time.Clock()
    # run set to true to start, until the game is exited, when it is set to false
    run = True
    direction = True
    direction_tky = True
    # always need a while loop now to run all the events that you set
    while run:
        # Set the game to run at the FPS, tick being one second
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_d] and tommy.x > VEL: # LEFT
            direction = True
            backgroundX -= VEL
            backgroundX2 -= VEL
        if keys_pressed[pygame.K_a] and tommy.x < (WIDTH - 54): # RIGHT
            direction = False
            backgroundX += VEL
            backgroundX2 += VEL
        if not(isJump):
            if keys_pressed[pygame.K_SPACE]: # JUMP
                isJump = True
        if not(isJump):
            if keys_pressed[pygame.K_SPACE]: # JUMP
                isJump = True
        else: 
            if jumpCount >= -10:
                tommy.y -=  (jumpCount * abs(jumpCount))/2
                jumpCount -= 1
            else:
                isJump = False
                tommy.y = 500
                jumpCount = 10


        # Run the previously defined function to set the display settings
        # The .fill method fills the window you created earlier with a set colour, which you defined above
        WIN.fill(BLUE)
        WIN.blit(background, (backgroundX,0))
        WIN.blit(background, (backgroundX2,0))
        # The blit method is used to load images or "surfaces" onto the screen
        if direction == True:
            WIN.blit(TOMMY_WISEAU_IMAGE, (tommy.x, tommy.y))
        if direction == False:
            WIN.blit(TOMMY_WISEAU_REVERSE_IMAGE, (tommy.x, tommy.y))
        if direction_tky == True:
            WIN.blit(TKY, (turkey.x, turkey.y))
        if direction_tky == False:
            WIN.blit(TKY_REVERSE_IMAGE, (turkey.x, turkey.y))

        # you need the method below to update changes made to display on previous lines so that you can make
        # several changes update at once
        pygame.display.update()   

    pygame.quit()

# You have to run main to run the game, and putting it in name == main means that it will only run if you
# run this code directly, not when it's imported
if __name__ == "__main__":
    main()