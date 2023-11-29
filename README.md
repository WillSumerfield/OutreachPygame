# OutreachPygame
 A super simple pygame platformer for new programmers to learn coding with

## Cool Modifications

### 1. Make the game faster!

Increase the x velocity and jump power on this line:

`player = Player(width=50, height=50, velx=0.15, vely=0, x=100, y=SCREEN_HEIGHT-120, jump_power=-0.5)`

to 0.4 and -0.75, like this:

`player = Player(width=50, height=50, velx=0.15, vely=0, x=100, y=SCREEN_HEIGHT-120, jump_power=-0.5)`

and increase the gravity to 0.002, too:

`GRAVITY = 0.002`

### 2. Randomize the platform generation

Change this function to place the platforms semi-randomly:

```
def generate_platform(x_offset):
    return Platform(900 + x_offset, SCREEN_HEIGHT - 50, 100, 20)
```

by adding random offsets to the position and size, like this:

```
def generate_platform(x_offset):
    return Platform(900 + x_offset + random.randint(-50, 50), SCREEN_HEIGHT - 50 - random.randint(0, 100), 100 + random.randint(-50, 50), 20 + random.randint(0, 50))
```

### 3. Add a "boost" button!

Underneath the code where we check for the spacebar being pressed (for jumping):

```
    if keys[pygame.K_SPACE] and grounded: # If the player is on the ground and presses space, let them jump
       player.vely = player.jump_power # Increase the player's y velocity by their jump power
```

add a new check for pressing the right arrow button. If it is pressed, increase the player's speed:

```
    if keys[pygame.K_SPACE] and grounded: # If the player is on the ground and presses space, let them jump
       player.vely = player.jump_power # Increase the player's y velocity by their jump power
    if keys[pygame.K_RIGHT]: # If the player presses the right arrow, give them a boost!
       player.velx = 0.8
```

and then reset the x velocity after the player has moved:

```
    # Move the player as needed
    player.move(platforms=platforms, delta_time=delta_time)

    # Reset the x velocity
    player.velx = 0.4
```
