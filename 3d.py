# Import the pygame module
import pygame
import math
import sys

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)
# Define constants for the screen width and height

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600

MAP_WIDTH = SCREEN_WIDTH - SCREEN_HEIGHT
MAP_HEIGHT = SCREEN_HEIGHT

GAME_WIDTH  = SCREEN_WIDTH - MAP_WIDTH
GAME_HEIGHT = SCREEN_HEIGHT

RECT_WIDTH = 60

FOV = 80
RAYS = 80

STEP = 5

MAX_DISTANCE = 10

VISIBLE_WALLS =[]

class Wall(pygame.sprite.Sprite):
    id = "wall"
    def __init__(self,x,y):
        super(Wall, self).__init__()
        self.surf = pygame.image.load("wall.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x += x
        self.rect.y += y
        
class Floor(pygame.sprite.Sprite):
    id="floor"
    def __init__(self,x,y):
        super(Floor, self).__init__()
        self.surf = pygame.image.load("floor.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x += x
        self.rect.y += y 

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    id = "player"
    angle = 0
    i =0
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25), pygame.SRCALPHA)  # Use SRCALPHA for transparency
        # Draw a filled circle on the surface
        pygame.draw.circle(self.surf, (123, 255, 255), (12, 12), 6)
        self.rect = self.surf.get_rect()
    
    def get_direction_line(self):
        start_pos = (self.rect.centerx, self.rect.centery)  # Start position at the center of the rect
        length = 20  # Length of the line

        # Convert angle to radians for trigonometric calculations
        radians = math.radians(self.angle)

        # Calculate the end position based on the angle
        end_pos = (
            start_pos[0] + length * math.cos(radians),  # Note: x = start_x + length * sin(angle)
            start_pos[1] + length * math.sin(radians)   # Note: y = start_y - length * cos(angle)
        )

        return start_pos, end_pos

    def get_fov_lines(self):
        start_pos = (self.rect.centerx, self.rect.centery)  # Start position at the center of the rect
        length = 160  # Length of the line
        normalize_angle
        # Convert angle to radians for trigonometric calculations
        start_angle = normalize_angle(self.angle - FOV/2)
        end_anble = normalize_angle(self.angle + FOV/2)
        start = math.radians(start_angle)
        end   = math.radians(end_anble)

        # Calculate the end position based on the angle
        end_pos_1 = (
            start_pos[0] + length * math.cos(start),  # Note: x = start_x + length * sin(angle)
            start_pos[1] + length * math.sin(start)   # Note: y = start_y - length * cos(angle)
        )

        end_pos_2 = (
            start_pos[0] + length * math.cos(end),  # Note: x = start_x + length * sin(angle)
            start_pos[1] + length * math.sin(end)   # Note: y = start_y - length * cos(angle)
        )

        return start_pos, end_pos_1, end_pos_2

    def update(self, pressed_keys):
        original_position = self.rect.copy()

        self.angle %= 360

        speed = 5

        if pressed_keys[K_UP]:
            # Move in the direction of the angle
            radians = math.radians(self.angle)
            dx = speed * math.cos(radians)  # x change based on angle
            dy = speed * math.sin(radians) # y change (negative because y increases downwards)
            self.rect.move_ip(dx, dy) 
        if pressed_keys[K_DOWN]:
            # Move in the opposite direction of the angle
            radians = math.radians(self.angle)
            dx = -speed * math.cos(radians)  # negative for moving down
            dy = -speed * math.sin(radians)  
              # positive for moving down
            self.rect.move_ip(dx, dy) 
        if pressed_keys[K_LEFT]:
            self.angle -= 1
        if pressed_keys[K_RIGHT]:
            self.angle += 1
        if pressed_keys[K_SPACE]:
             print("===============START")
             d = cast_ray(self.rect.centerx-800, self.rect.centery, self.angle, self.angle-FOV/2)
             d = cast_ray(self.rect.centerx-800, self.rect.centery, self.angle, self.angle-FOV/2+10)
             d = cast_ray(self.rect.centerx-800, self.rect.centery, self.angle, self.angle-FOV/2+20)
             d = cast_ray(self.rect.centerx-800, self.rect.centery, self.angle, self.angle-FOV/2+30)
             d = cast_ray(self.rect.centerx-800, self.rect.centery, self.angle, self.angle-FOV/2+40)
             d = cast_ray(self.rect.centerx-800, self.rect.centery, self.angle, self.angle-FOV/2+50)
             d = cast_ray(self.rect.centerx-800, self.rect.centery, self.angle, self.angle-FOV/2+60)
             d = cast_ray(self.rect.centerx-800, self.rect.centery, self.angle, self.angle+FOV/2)
             print("===============END")

         # Keep player on the screen
        if self.rect.left < MAP_WIDTH:
            self.rect.left = MAP_WIDTH
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        if pygame.sprite.spritecollideany(player, map_level):
            # If so, then remove the player and stop the loop
            self.rect = original_position

def cast_ray(x,y, player_angle, ray_angle):
    player_angle = normalize_angle(player_angle)
    ray_angle = normalize_angle(ray_angle)
    nx = x
    ny = y
    radian_angle = math.radians(ray_angle)
    radian_player_angle = math.radians(player_angle)
    step = 0.5
    dx = math.cos(radian_angle)*step
    dy = math.sin(radian_angle)*step
    m_range = int(MAX_DISTANCE * RECT_WIDTH/step)
    exit_i=0
    for depth in range(m_range):
        exit_i +=1
        nx += dx 
        ny += dy 
        cell_x      = int(nx // RECT_WIDTH)
        cell_y      = int(ny // RECT_WIDTH)

        if cell_x < 0 or cell_x > len(array_2d[0]) or cell_y<0 or cell_y>len(array_2d):
            return MAX_DISTANCE*RECT_WIDTH
        elif array_2d[cell_y][cell_x] == 1:
            delta_x = nx - x
            delta_y = ny - y
            
            distance = delta_x * math.cos(radian_player_angle) + delta_y*math.sin(radian_player_angle)
            
            return distance
            
    return MAX_DISTANCE*RECT_WIDTH

def convert_angle(theta):
    new_theta = -theta  # Reverse direction
    # Normalize to [0, 360]
    if new_theta < 0:
        new_theta += 360
    return new_theta

def normalize_angle(angle):
    # Add 360 until the angle is positive
    angle = angle % 360
    return angle 

def game_angle(angle):
    return normalize_angle(90 - angle)

def render_walls(p_angle, p_x, p_y ):
    walls = []
    delta = FOV/RAYS
    
    for i in range(RAYS):
        ray_angle = p_angle -FOV/2 + delta*i
        d = cast_ray(p_x-800, p_y, p_angle, ray_angle)
        if d<0:
            d = d * -1
        walls.append(d)
   
    return walls

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create Sprite Goup for Map level
allsprites  = pygame.sprite.Group()

# Create Sprite Goup for Map Player
map_level = pygame.sprite.Group()

# Create Floor Grout for Map Level
floor_level = pygame.sprite.Group()

# Draw minimap
array_2d = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
for row_index, row in enumerate(array_2d):
    for col_index, cell in enumerate(row):
        if cell != 0:
            # Calculate the rectangle's position based on row and column
            x = col_index * RECT_WIDTH
            y = row_index * RECT_WIDTH
            wall = Wall(x+MAP_WIDTH,y)
            allsprites.add(wall)
            map_level.add(wall)
        else:
            x = col_index * RECT_WIDTH
            y = row_index * RECT_WIDTH
            floor = Floor(x+MAP_WIDTH,y)
            allsprites.add(floor)

allsprites.add(player)

player.rect.x = 1100
player.rect.y = 100

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player on the screen
    
    for entity in allsprites:
        screen.blit(entity.surf, entity.rect)

    w_to_render = render_walls(player.angle, player.rect.x, player.rect.y)

    for index, wall_3d in enumerate(w_to_render):
        height = int(SCREEN_HEIGHT/(wall_3d+0.001) * 40)
        color = int(127 - (wall_3d * 127 / SCREEN_HEIGHT)) + 20  # Inverted mapping with reduced brightness
        color = max(0, min(127, color))  # Clamp color to [0, 127]
        pygame.draw.rect(screen, (color,color,color), (index * ( (SCREEN_WIDTH-600) // RAYS ), (SCREEN_HEIGHT - height) // 2, (SCREEN_WIDTH-600) // RAYS, height ) )
    
    # Draw the Player Angle line separately
    start_pos, end_pos = player.get_direction_line()
    pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 2)  
    
    # Draw the Player Fov
    fov_x, fov_y1, fov_y2 = player.get_fov_lines()
    pygame.draw.line(screen, (255, 255, 0), fov_x, fov_y1, 2)
    pygame.draw.line(screen, (255, 255, 0), fov_x, fov_y2, 2)

    # Update the display
    pygame.display.flip()