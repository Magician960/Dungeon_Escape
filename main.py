import pygame
import os
from spritesheet import SpriteSheet

#Set working directory
path = "/home/tonynguyen/Personal_Projects/Game_Jam_Projects/Dungeon_Escape/"
os.chdir(path)

#Initialise pygame
pygame.init()

#Create a display surface and caption it
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dungeon Escape")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Define classes
class Player(pygame.sprite.Sprite):
    """A class the user can control"""
    def __init__(self, x, y):
        """Initialise the player"""
        super().__init__()

        #Set constant varialbes
        self.STARTING_SPEED = 1

        #Set starting variables
        self.speed = self.STARTING_SPEED

        #Load the player sprites
        filename = "assets/player_spritesheet.png"
        player_ss = SpriteSheet(filename)

        #Get player sprites
        self.player_down_sprites = []
        for i in range(2):
            image = player_ss.image_at((0 + i*48, 0 + i*64, 48, 64))
            self.player_down_sprites.append(image)

        #Load image and get rect
        self.current_sprite = 0
        self.image = self.player_down_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    
    def update(self):
        """A method to update the player sprite"""
        self.move()

    def move(self):
        """A method to move the player"""
        #If a player holds down a directional key, move them in that direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

#Create sprite groups
my_player_group = pygame.sprite.Group()

#Add player to sprite group
my_player = Player(0,WINDOW_HEIGHT)
my_player_group.add(my_player)

#Main game loop
running = True
while running:
    #Check to see if the user wants to quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update and draw sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)
    
    
    #Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

#Uninitialise pygame
pygame.quit()