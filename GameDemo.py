# Import Packages
import pygame
import sys
import math
import random

# ---------- Function Definitions ----------

# Do general initialization stuff here
def initialize(screen_width, screen_height):

    # Initialize Pygame
    pygame.init()

    # Initialize the screen
    screen = pygame.display.set_mode((screen_width, screen_height))

    return screen

# Creates a new platform
def generate_platform(x_offset):
    return Platform(900 + x_offset, SCREEN_HEIGHT - 50, 100, 20)

# Draw the player, the platforms, and the background to the screen. If you add new things to your game, update this function so that you can see them!
def draw(screen, platforms, player):

    # Draw the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the platforms
    for platform in platforms:
        pygame.draw.rect(surface=screen, color=(0, 0, 0), rect=pygame.Rect(int(platform.x), int(platform.y), platform.width, platform.height))

    # Draw the player
    pygame.draw.rect(surface=screen, color=(255, 0, 0), rect=pygame.Rect(int(player.x), int(player.y), player.width, player.height))

    # Update the screen
    pygame.display.flip()

# Check if the exit button is pressed - stop the game if so
def exit_pressed():

    # "Events" in pygame are things like mouse clicks, button clicks, keypresses, etc...
    for event in pygame.event.get():

        # If one of the events was pressing the "Exit" button, quit the game!
        if event.type == pygame.QUIT:

            # Return "True" to show that we should close the game
            return True

    # Return "False" to show that we should keep the game running
    return False

# If a platforms goes off the screen, remove it!
def remove_offscreen_platforms(platforms):

    # How far a platform is from the left side of the screen
    platform_dist = platforms[0].x + platforms[0].width

    # If the platform is fully offscreen, delete it!
    if platform_dist < 0:
        del platforms[0] # Delete the platform
        platforms += [generate_platform(platform_dist)] # Generate a new platform!

    return platforms

# -------------------------------------------


# ------------ Class Definitions ------------

# The player
class Player:

    # Create a new player with the given properties
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

    # Move the player based on their speed
    def move(self, platforms, delta_time):

        # Apply gravity
        self.vely = self.vely+(GRAVITY*delta_time)

        # Move the player vertically
        y_dist = self.vely*delta_time # The total vertical movement to move the player
        if not self.platform_collision(platforms, 0, y_dist): # Try moving the player veritically. Does it collide with a platform?
            self.y += y_dist # If it didn't collide, great! Move the player vertically.

        # The player did collide with a platform when we tried moving it - move it one space at a time until it collides with the platform.
        else:
            while not self.platform_collision(platforms, 0, math.copysign(1, y_dist)): # Keep moving the player until they collide with the platform
                self.y += math.copysign(1, y_dist)

        # Move the player horizontally (but actually move each of the platforms instead, to make it 'look' like the player is moving
        x_dist = self.velx*delta_time # The total horizontal movement to move the player
        if not self.platform_collision(platforms, x_dist, 0): # Try moving the player horizontally. Does it collide with a platform?

            # If it didn't collide, great! Move each platform horizontally
            for platform in platforms:
                platform.x -= x_dist

        # The player did collide with a platform when we tried moving it - move it one space at a time until it collides with the platform.
        else:
            # For each pixel we need to move the player...
            for pixel in range(math.ceil(abs(x_dist))):

                # Find the distance to move the player
                dist = 0
                if x_dist > 1:
                    dist = math.copysign(1, x_dist)
                else:
                    dist = x_dist

                # Move each platform
                for platform in platforms:
                    platform.x -= dist

                # If the player is touching a platform, move it backwards
                if self.platform_collision(platforms, 0, 0):
                    self.x -= dist

    # Returns True/False if the player is on the ground or not
    def is_grounded(self):

        # Check if there is a platform below the player
        if player.platform_below(platforms):

            # If they're on the ground, they shouldn't be falling
            player.vely = 0

            # The player is on the ground
            return True

        # The player is not on the ground
        return False

# The platforms
class Platform:

    # Create a new platform with the given properties
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

# Keeps track of the time which passed between each frame of the game, so we know how much to move things!
class Clock:

    # Create a new clock
    def __init__(self):
        self.previous_time = pygame.time.get_ticks() # The time it was last frame
        self.current_time = pygame.time.get_ticks() # The current time

    # Returns the time since the last frame
    def get_delta_time(self):
        current_time = pygame.time.get_ticks() # Find the current time
        delta_time = current_time - self.previous_time # Find the time that has passed since the last frame and this one
        self.previous_time = current_time # Update the previous time
        return delta_time

# -------------------------------------------

# Set up constant values here. Change them as you'd like!
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
BACKGROUND_COLOR = (135, 206, 235)  # Light Blue
GRAVITY = 0.001

# Initialize the game, and return the screen we draw to
screen = initialize(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)

# Create the player - jump power is negative because in pygame, negative y values are "up"!
player = Player(width=50, height=50, velx=0.15, vely=0, x=100, y=SCREEN_HEIGHT-120, jump_power=-0.5)

# Create the starting platforms - we will delete these and generate more as these go offscreen
platforms = [
    Platform(150,   SCREEN_HEIGHT -  50, 100, 20),
    Platform(350,   SCREEN_HEIGHT -  50, 100, 20),
    Platform(550,   SCREEN_HEIGHT -  50, 100, 20),
    Platform(750,   SCREEN_HEIGHT -  50, 100, 20),
    Platform(950,   SCREEN_HEIGHT -  50, 100, 20),
]

# Create the clock timer
clock = Clock()

# Game loop
running = True # If something sets this to "False", we exit the while loop and the program exits - effectively closing the game!
while running:

    # Find how much time has passed since the last frame
    delta_time = clock.get_delta_time()

    # Exit the game if we press the exit button
    running = not exit_pressed()

    # Remove platforms which go off the screen, and generate new platforms as needed
    platforms = remove_offscreen_platforms(platforms=platforms)

    # Keeps track of if the player is on the ground or not
    grounded = player.is_grounded()

    # Check for keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and grounded: # If the player is on the ground and presses space, let them jump
       player.vely = player.jump_power # Increase the player's y velocity by their jump power

    # Move the player as needed
    player.move(platforms=platforms, delta_time=delta_time)

    # If the player fell off the map, quit the game
    if (player.y > SCREEN_HEIGHT):
        running = False

    # If the player was pushed off the map, quit the game
    if (player.x < -player.width):
        running = False

    # Draw the player, the platforms, and the background to the screen. If you add new things to your game, update this function so that you can see them!
    draw(screen=screen, platforms=platforms, player=player)
