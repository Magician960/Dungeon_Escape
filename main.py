import pygame
import os
import random
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
    def __init__(self, player, door_group, rat_group):
        #Set constant variables
        self.STARTING_ROUND_TIME = 30
        self.STARTING_ROUND_NUMBER = 1

        #Set game values
        self.round_number = self.STARTING_ROUND_NUMBER
        self.frame_count = 0
        self.round_time = self.STARTING_ROUND_TIME

        #Set fonts
        self.title_font = pygame.font.Font("assets/aAbsoluteEmpire.ttf", 96)
        self.HUD_font = pygame.font.Font("assets/aAbsoluteEmpire.ttf", 48)

        #Attach sprites and groups
        self.player = player
        self.door_group = door_group
        self.rat_group = rat_group
    
    def update(self):
        """Update the game"""
        self.frame_count+= 1
        if self.frame_count % FPS == 0:
            self.round_time -= 1
            self.frame_count = 0
        
        self.check_collisions()

    def check_collisions(self):
        """A method to check collisions between sprites"""
        #Check to see if the player sprite collided with the door
        if pygame.sprite.spritecollide(self.player, self.door_group, False):
            self.start_new_round()

        #Check to see if the player sprite collided with a rat
        if pygame.sprite.spritecollide(self.player, self.rat_group, False):
            self.reset_game()

    def reset_game(self):
        """A method to reset the game upon a loss"""
        self.round_number = self.STARTING_ROUND_NUMBER
        self.round_time = self.STARTING_ROUND_TIME
        self.player.reset()

        #Depopulate sprite group
        self.rat_group.empty()

        #Repopulate rat group
        for i in range(self.round_number):
            rat = Rat(1)
            self.rat_group.add(rat)

        self.pause_game("You have died", "Press 'Enter' to try again...")

    def start_new_round(self):
        """A method to start a new round"""
        #Reset round values
        self.player.reset()
        self.round_time = 30
        self.round_number += 1   
        self.pause_game("You have escaped!", "Press 'Enter' to continue...")

        #Depopulate sprite group
        self.rat_group.empty()

        #Spawn new rat sprites
        for i in range(self.round_number * 3):
            rat = Rat(1)
            self.rat_group.add(rat)


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
    
    def pause_game(self, main_text, sub_text):
        """Pause the game until user presses enter"""
        global running

        #Set colors
        WHITE = (255,255,255)
        BLACK = (0,0,0)

        #Create main pause text
        main_text = self.title_font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        #Create sub pause text
        sub_text = self.HUD_font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        #Display pause screen
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)

        pygame.display.update()

        #Pause the game until user hits enter or quits
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #User wants to continue
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                #User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

class Player(pygame.sprite.Sprite):
    """A class the user can control"""
    def __init__(self, x, y):
        """Initialise the player"""
        super().__init__()

        #Set constant variables
        self.STARTING_SPEED = 4
        self.STARTING_X = x
        self.STARTING_Y = y

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
    
    def reset(self):
        """A method to return the player sprite to the starting location"""
        self.rect.bottomleft = (self.STARTING_X, self.STARTING_Y)

class Rat(pygame.sprite.Sprite):
    """A class of enemy rats the player should avoid"""
    def __init__(self, speed):
        super().__init__()

        #Set starting variables
        self.speed = speed
        #Set initial direction
        self.direction_x = 0
        self.direction_y = 0

        while self.direction_x == 0 and self.direction_y == 0:
            self.direction_x = random.choice([-1,0,1])
            self.direction_y = random.choice([-1,0,1])

        #Get animation frames
        if random.randint(0,1) == 1:
            filename = "assets/rat_spritesheet.png"
        else:
            filename = "assets/mouse_spritesheet.png"
        rat_ss = SpriteSheet(filename)

        #Get rat sprites
        self.rat_up_sprites = []
        for i in range(0,3):
            image = rat_ss.image_at((0 + i*32, 0, 32, 32))
            self.rat_up_sprites.append(image)

        self.rat_right_sprites = []
        for i in range(0,3):
            image = rat_ss.image_at((0 + i*32, 32, 32, 32))
            self.rat_right_sprites.append(image)

        self.rat_down_sprites = []
        for i in range(0,3):
            image = rat_ss.image_at((0 + i*32, 64, 32, 32))
            self.rat_down_sprites.append(image)

        self.rat_left_sprites = []
        for i in range(0,3):
            image = rat_ss.image_at((0 + i*32, 96, 32, 32))
            self.rat_left_sprites.append(image)

        #Load image and get rect
        self.current_sprite = 0
        self.image = self.rat_down_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(WINDOW_WIDTH//2 - 100, WINDOW_WIDTH//2 + 100), random.randint(WINDOW_HEIGHT//2 - 100, WINDOW_HEIGHT//2 + 100))
    def update(self):
        """A method to update the rat sprite"""
        self.move()
    
    def move(self):
        """A method to move the rat sprite"""
        self.rect.x += random.uniform(self.direction_x /2,self.direction_x * 2) * random.uniform(self.speed, self.speed*2)
        self.rect.y += random.uniform(self.direction_y /2,self.direction_y * 2) * random.uniform(self.speed, self.speed*2)

        #Check if the sprite has collided with the boundaries
        if self.rect.bottom >= WINDOW_HEIGHT or self.rect.top <= 0:
            self.direction_y *= -1
            self.rect.y += 20*self.direction_y
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.direction_x *= -1
            self.rect.x += 20 * self.direction_x
        
        #Animate the rat moving
        if self.direction_x > 0:
            self.animate(self.rat_right_sprites, 0.1)
        else:
            self.animate(self.rat_left_sprites, 0.1)
        
        if self.direction_y > 0:
            self.animate(self.rat_down_sprites, 0.1)
        else:
            self.animate(self.rat_up_sprites, 0.1)
    
    def animate(self, sprite_list, speed):
        """A method to animate the rat moving"""
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
my_rat_group = pygame.sprite.Group()

#Add door to sprite group
my_door = Door(WINDOW_WIDTH - 50, 50)
my_door_group.add(my_door)

#Add player to sprite group
my_player = Player(0,WINDOW_HEIGHT)
my_player_group.add(my_player)

#TEST - add rat
my_rat = Rat(1)
my_rat_group.add(my_rat)

#Start the game
my_game = Game(my_player, my_door_group, my_rat_group)
my_game.pause_game("Dungeon Escape", "Press 'Enter' to begin...")

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

    my_rat_group.update()
    my_rat_group.draw(display_surface)

    #Update and draw the game
    my_game.update()
    my_game.draw()
    
    #Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

#Uninitialise pygame
pygame.quit()