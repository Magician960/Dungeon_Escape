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
class Game():
    """A class to help manage gameplay and sprite interactions"""
    def __init__(self, player, door):
        #Set constant variables
        self.STARTING_ROUND_TIME = 30

        #Set game values
        self.round_number = 1
        self.frame_count = 0
        self.round_time = self.STARTING_ROUND_TIME

        #Set fonts
        self.title_font = pygame.font.Font("assets/aAbsoluteEmpire.ttf", 96)
        self.HUD_font = pygame.font.Font("assets/aAbsoluteEmpire.ttf", 48)

        #Attach sprites and groups
        self.player = player
        self.door = door
    
    def update(self):
        """Update the game"""
        self.frame_count+= 1
        if self.frame_count % FPS == 0:
            self.round_time -= 1
            self.frame_count = 0
    
    def draw(self):
        """Draw the GAME HUD"""
        #Set colors
        WHITE = (255,255,255)

        #Set text
        round_text = self.HUD_font.render(f"Round: {self.round_number}", True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (10, 10)

        time_text = self.HUD_font.render(f"Time Left: {self.round_time}", True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 50)

        #Blit the HUD
        display_surface.blit(round_text, round_rect)
        display_surface.blit(time_text, time_rect)

class Player(pygame.sprite.Sprite):
    """A class the user can control"""
    def __init__(self, x, y):
        """Initialise the player"""
        super().__init__()

        #Set constant varialbes
        self.STARTING_SPEED = 4

        #Set starting variables
        self.speed = self.STARTING_SPEED

        #Load the player sprites
        filename = "assets/player_spritesheet.png"
        player_ss = SpriteSheet(filename)

        #Get player sprites
        self.player_down_sprites = []
        for i in range(0,3):
            image = player_ss.image_at((0 + i*48, 0, 48, 64))
            self.player_down_sprites.append(image)
        
        self.player_left_sprites = []
        for i in range(0,3):
            image = player_ss.image_at((0 + i*48, 64, 48, 64))
            self.player_left_sprites.append(image)

        self.player_right_sprites = []
        for i in range(0,3):
            image = player_ss.image_at((0 + i*48, 128, 48, 64))
            self.player_right_sprites.append(image)
        
        self.player_up_sprites = []
        for i in range(0,3):
            image = player_ss.image_at((0 + i*48, 192, 48, 64))
            self.player_up_sprites.append(image)

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
        #If a player holds down a directional key AND is in-bounds, move them in that direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.animate(self.player_left_sprites, .1)
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
            self.animate(self.player_right_sprites, .1)
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.animate(self.player_up_sprites, .1)
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed
            self.animate(self.player_down_sprites, .1)
    
    def animate(self, sprite_list, speed):
        """A method to animate the character moving"""
        if self.current_sprite <= len(sprite_list) - 0.1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]

class Door(pygame.sprite.Sprite):
    """A class that the player sprite can collide with to pass the game"""
    def __init__(self, x, y):
        super().__init__()
        #Load image
        self.image = pygame.image.load("assets/castledoors.png")
        self.rect = self.image.get_rect()
        self.rect.topright = (x, y)

#Create sprite groups
my_player_group = pygame.sprite.Group()
my_door_group = pygame.sprite.Group()

#Add door to sprite group
my_door = Door(WINDOW_WIDTH - 50, 50)
my_door_group.add(my_door)

#Add player to sprite group
my_player = Player(0,WINDOW_HEIGHT)
my_player_group.add(my_player)

#Start the game
my_game = Game(my_player, my_door)

#Main game loop
running = True
while running:
    #Check to see if the user wants to quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Fill screen with black (REPLACE THIS WITH BACKGROUND IMAGE SOON)
    display_surface.fill((0,0,0))

    #Update and draw sprite groups
    my_door_group.update()
    my_door_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)

    #Update and draw the game
    my_game.update()
    my_game.draw()
    
    #Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

#Uninitialise pygame
pygame.quit()