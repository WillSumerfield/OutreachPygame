# Import Packages
import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
BACKGROUND_COLOR = (135, 206, 235)  # Light Blue
GRAVITY = 0.001

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Platformer Game")

# Player properties
class Player:

    def __init__(self, width, height, velx, vely, x, y, jump_power):
        self.width = width
        self.height = height
        self.velx = velx
        self.vely = vely
        self.x = x
        self.y = y
        self.jump_power = jump_power

    # Returns True/False if the player is inside the given platform
    def platform_collision(self, platforms, x_offset=0, y_offset=0):

        # Check each platform for a collision...
        for platform in platforms:

            # If one is on left side of other
            if (self.x + x_offset > platform.x + platform.width) or (platform.x > self.x + self.width + x_offset):
                continue
 
            # If one rectangle is above other
            if (self.y+1 + y_offset > platform.y + platform.height) or (platform.y+1 > self.y + self.height + y_offset):
                continue
        
            # The platforms are overlapping
            return True

        # If no platforms collided, then say "False
        return False

    # Returns True/False if a platform is right under the player
    def platform_below(self, platforms):

        # Check each platform for collisions
        for platform in platforms:

            # If one is on left side of other
            if (self.x > platform.x + platform.width) or (platform.x > self.x + self.width):
                continue

            # If the platform is just below the player, return True!
            if abs(platform.y - (self.y + self.height-1)) <= 1:
                return True

        # If no platforms are below the player, return false
        return False

player = Player(50, 50, 0.15, 0, 100, SCREEN_HEIGHT-120, -0.5)

# Platform properties
class Platform:
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

platforms = [
    Platform(150,   SCREEN_HEIGHT -  50, 100, 20),
    Platform(350,   SCREEN_HEIGHT -  50, 100, 20),
    Platform(540,   SCREEN_HEIGHT -  50, 100, 20),
    Platform(750,   SCREEN_HEIGHT -  50, 100, 20),  
    Platform(950,   SCREEN_HEIGHT -  50, 100, 20),  
]

# Creates a new platform
def generate_platform(x_offset):
    return Platform(900 + x_offset, SCREEN_HEIGHT - 50, 100, 20)

# Game loop
running = True
previous_time = pygame.time.get_ticks()
while running:

    # Find the time that has passed since the last frame
    current_time = pygame.time.get_ticks()
    delta_time = current_time - previous_time
    previous_time = current_time

    # Check if we want to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remove platforms which go off the screen, and generate new platforms as needed
    platform_dist = platforms[0].x + platforms[0].width;
    if platform_dist < 0:
        del platforms[0]
        platforms += [generate_platform(platform_dist)]

    # Check if the player is grounded
    grounded = False
    if player.platform_below(platforms):
        grounded = True
        player.vely = 0

    # Check for keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and grounded:
       player.vely = player.jump_power

    # Apply gravity
    player.vely = player.vely+(GRAVITY*delta_time)

    # Move the player vertically
    y_dist = player.vely*delta_time # The total vertical movement to move the player
    if not player.platform_collision(platforms, 0, y_dist): # Try moving the player veritically. Does it collide with a platform?
        player.y += y_dist # If it didn't collide, great! Move the player vertically.

    # The player did collide with a platform when we tried moving it - move it one space at a time until it collides with the platform.
    else: 
        print("Y-Dist: ", y_dist)
        while not player.platform_collision(platforms, 0, math.copysign(1, y_dist)): # Keep moving the player until they collide with the platform
            player.y += math.copysign(1, y_dist)

    # Move the player horizontally (but actually move each of the platforms instead, to make it 'look' like the player is moving
    x_dist = player.velx*delta_time # The total horizontal movement to move the player
    if not player.platform_collision(platforms, x_dist, 0): # Try moving the player horizontally. Does it collide with a platform?

        # If it didn't collide, great! Move each platform horizontally
        for platform in platforms:
            platform.x -= x_dist 
    
    # The player did collide with a platform when we tried moving it - move it one space at a time until it collides with the platform.
    else: 
        while not player.platform_collision(platforms, 0, math.copysign(1, x_dist)): # Keep moving the player until they collide with the platform
            for platform in platforms:
                platform.x -= math.copysign(1, x_dist)

    # If the player fell off the map, quite the game
    if (player.y < 0):
        running = False

    # Draw the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the platforms
    for platform in platforms:
        pygame.draw.rect(screen, (0, 0, 0), (platform.x, platform.y, platform.width, platform.height))

    # Draw the player
    pygame.draw.rect(screen, (255, 0, 0), (player.x, player.y, player.width, player.height))

    # Invert the screen
    pygame.display.flip()

# Clean up and quit
pygame.quit()
sys.exit()