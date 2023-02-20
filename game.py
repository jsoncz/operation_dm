import pygame
import random

pygame.joystick.init()
# Get a reference to each connected joystick
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Enable each joystick
for joystick in joysticks:
    joystick.init()

FPS = 30

# Define the block types and their corresponding images
BLOCK_TYPES = ["wood", "diamond", "rock", "bomb"]
BLOCK_IMAGES = [pygame.image.load(f"{block_type}.png") for block_type in BLOCK_TYPES]

# Define the size of the bag and the number of blocks in each set
BAG_SIZE = 100
SET_SIZE = 3
NUM_BLOCKS = 3
# Create the bag of blocks
bag = []
for block_type in BLOCK_TYPES:
    count = BAG_SIZE // len(BLOCK_TYPES)
    bag.extend([block_type] * count)
bag = random.sample(bag, k=BAG_SIZE)

# Draw a new set of blocks
def draw_set():
    set_blocks = random.sample(bag, k=SET_SIZE)
    for block_type in set_blocks:
        bag.remove(block_type)
    set_images = [BLOCK_IMAGES[BLOCK_TYPES.index(block_type)] for block_type in set_blocks]
    return set_images

# Define some colors
BLACK, WHITE, BLUE, RED, YELLOW, GRAY = (0, 0, 0), (255, 255, 255), (0, 0, 255), (255, 0, 0), (255, 255, 0), (128, 128, 128)

# Define the size of the game grid and blocks
GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE = 8, 12, 64

# Load the game block images
BLOCK_IMAGES = [pygame.image.load("block{}.png".format(i)) for i in range(4)]


class Block:
    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.block_type = block_type

class FallingSet:
    def __init__(self, block_images, block_size, grid_width, player):
        self.player = player
        self.blocks = [Block(grid_width//2, 0, random.randint(1, 4)),
                       Block(grid_width//2, -block_size, random.randint(1, 4)),
                       Block(grid_width//2-block_size, -block_size, random.randint(1, 4)),
                       Block(grid_width//2+block_size, -block_size, random.randint(1, 4))]
        self.block_size = block_size
        self.rotation_point = self.blocks[1].x, self.blocks[1].y
    
    def update(self):
        self.move_down()

    def move_down(self):
        # Move the current set of blocks down by one row
        for block in self.blocks:
            block.y += self.block_size

        # Check if the blocks would collide with any blocks on the grid
        for block in self.blocks:
            row = (block.y - self.player.y) // self.block_size
            col = (block.x - self.player.x) // self.block_size
            if not (0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH and self.player.grid[row][col] == 0):
                # Move the blocks back up by one row and add them to the grid
                for block in self.blocks:
                    block.y -= self.block_size
                    row = (block.y - self.player.y) // self.block_size
                    col = (block.x - self.player.x) // self.block_size
                    self.player.grid[row][col] = block.block_type
                self.blocks = []
                break

    def rotate(self):
        # Rotate the current set of blocks around the second block in the set
        for block in self.blocks:
            x_diff = block.x - self.rotation_point[0]
            y_diff = block.y - self.rotation_point[1]
            block.x = self.rotation_point[0] + y_diff
            block.y = self.rotation_point[1] - x_diff

            # Check if the rotated block would collide with any blocks on the grid
            row = (block.y - self.player.y) // self.block_size
            col = (block.x - self.player.x) // self.block_size
            if not (0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH and self.player.grid[row][col] == 0):
                # Rotate the blocks back to their original position
                for block in self.blocks:
                    x_diff = block.x - self.rotation_point[0]
                    y_diff = block.y - self.rotation_point[1]
                    block.x = self.rotation_point[0] - y_diff
                    block.y = self.rotation_point[1] + x_diff
                break

class Player:
    def __init__(self, x, y, block_size, grid_size):
        self.x = x
        self.y = y
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.blocks = []
        self.block_size = block_size
        self.grid_size = grid_size
        self.current_set = FallingSet(BLOCK_IMAGES, BLOCK_SIZE, NUM_BLOCKS, self)
        self.next_blocks = [Block(GRID_WIDTH//2, 0, random.randint(1, 4)),
                            Block(GRID_WIDTH//2, -self.block_size, random.randint(1, 4)),
                            Block(GRID_WIDTH//2, -2*self.block_size, random.randint(1, 4))]
        self.ready = False

    def spawn_blocks(self):
        self.blocks.extend(self.next_blocks)
        self.next_blocks = [Block(GRID_WIDTH//2, 0, random.randint(1, 4)),
                            Block(GRID_WIDTH//2, -self.block_size, random.randint(1, 4)),
                            Block(GRID_WIDTH//2, -2*self.block_size, random.randint(1, 4))]
    def handle_input(self, joystick=None):
        # Handle keyboard input
        keys = pygame.key.get_pressed()

        # Handle player 1 input
        if keys[pygame.K_LEFT]:
            self.player1.move_left()
        elif keys[pygame.K_RIGHT]:
            self.player1.move_right()
        elif keys[pygame.K_DOWN]:
            self.player1.move_down()
        elif keys[pygame.K_SPACE]:
            self.player1.rotate()
       
        # Handle player 2 input
        
        if keys[pygame.K_a]:
            self.player2.move_left()
        elif keys[pygame.K_d]:
            self.player2.move_right()
        elif keys[pygame.K_s]:
            self.player2.move_down()
        elif keys[pygame.K_q]:
            self.player2.rotate()
     
       
        # Handle joystick input, if a joystick is passed as a parameter
        if joystick is not None:
            x_axis = joystick.get_axis(0)
            y_axis = joystick.get_axis(1)
            rotate_button = joystick.get_button(0)
            if x_axis < -0.5:
                self.move_left()
            elif x_axis > 0.5:
                self.move_right()

            if y_axis > 0.5:
                self.move_down()

            if rotate_button:
                self.rotate()
         

    def update(self):
        # Move the current set of blocks down the grid
        self.current_set.update()

        # Check if the current set has landed
        if self.set_landed():
            # Add the blocks in the set to the player's grid
            self.add_set_to_grid()

            # Create a new falling set of blocks
            self.current_set = FallingSet(BLOCK_IMAGES, BLOCK_SIZE, NUM_BLOCKS, self)

    def set_landed(self):
        for block in self.blocks:
            row = int((block.y - self.y) / self.block_size)
            col = int((block.x - self.x) / self.block_size)
            if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
                self.grid[row][col] = block.block_type
        self.blocks = []

        # Check if the blocks would collide with any blocks on the grid
        for block in self.current_set.blocks:
            row = int((block.y - self.y) / self.block_size)
            col = int((block.x - self.x) / self.block_size)
            if row >= GRID_HEIGHT or self.grid[row][col] != 0:
                return True

        return False

    def add_set_to_grid(self):
        # Add the blocks in the current set to the player's grid
        for block in self.current_set.blocks:
            row = (block.y - self.y) // self.block_size
            col = (block.x - self.x) // self.block_size
            self.grid[row][col] = block.block_type

    def move_left(self):
        # Move the current set of blocks to the left by one column
        for block in self.current_set.blocks:
            block.x -= self.block_size

        # If the set would collide with any blocks on the grid, move it back to its original position
        if self.set_would_collide():
            for block in self.current_set.blocks:
                block.x += self.block_size

    def move_right(self):
        # Move the current set of blocks to the right by one column
        for block in self.current_set.blocks:
            block.x += self.block_size

        # If the set would collide with any blocks on the grid, move it back
        if self.set_collides():
            for block in self.current_set.blocks:
                block.x -= self.block_size

        # Check if the set is out of bounds and move it back if necessary
        if self.set_out_of_bounds():
            for block in self.current_set.blocks:
                block.x -= self.block_size

    def set_collides(self):
        # Check if the set would collide with any blocks on the grid
        for block in self.current_set.blocks:
            row = int((block.y - self.y) / self.block_size)
            col = int((block.x - self.x) / self.block_size)
            if not (0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH) or self.grid[row][col] != 0:
                return True
        return False

    def set_out_of_bounds(self):
        # Check if the set is out of bounds
        for block in self.current_set.blocks:
            if block.x < self.x or block.x >= self.x + self.grid_size[0]:
                return True
        return False



class Game:
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size

        # Set up the game grid and players
        GRID_WIDTH = 10
        GRID_HEIGHT = 20
        BLOCK_SIZE = 30
        PADDING = 50
        MARGIN = 20

        player1_x = (self.size[0] - (2 * GRID_WIDTH + PADDING)) // 2
        player1_y = MARGIN
        player2_x = player1_x + GRID_WIDTH + PADDING
        player2_y = MARGIN

        self.player1_grid_size = (GRID_WIDTH, GRID_HEIGHT)
        self.player2_grid_size = (GRID_WIDTH, GRID_HEIGHT)
        self.player1 = Player(player1_x, player1_y, BLOCK_SIZE, self.player1_grid_size)
        self.player2 = Player(player2_x, player2_y, BLOCK_SIZE, self.player2_grid_size)

        # Set up the falling speed of the blocks
        self.fall_speed = 0.5  # seconds per block

        # Set up the timer for block falling
        self.fall_timer = 0
        self.game_over = False
        # Set up a flag to check if both players are ready
        self.both_players_ready = False

        # Set up the clock to control the game's FPS
        self.clock = pygame.time.Clock()
   
      
    def check_players_ready(self):
        if self.player1.ready and self.player2.ready:
            self.both_players_ready = True
            print ("ready")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


    def display_splash_screen(self):
        # Set up font and text
        font = pygame.font.Font(None, 50)
        text = font.render("Press Start to begin", True, BLACK)
        text_rect = text.get_rect(center=self.screen.get_rect().center)

     
        # Set up font and text for player 1 status
        p1_font = pygame.font.Font(None, 30)
        p1_text = p1_font.render("Player 1 - Ready" if self.player1.ready else "Player 1 - Not ready", True, BLACK)
        p1_rect = p1_text.get_rect(center=(text_rect.centerx, text_rect.centery + 50))
        self.screen.blit(p1_text, p1_rect)

        # Set up font and text for player 2 status
        p2_font = pygame.font.Font(None, 30)
        p2_text = p2_font.render("Player 2 - Ready" if self.player2.ready else "Player 2 - Not ready", True, BLACK)
        p2_rect = p2_text.get_rect(center=(text_rect.centerx, text_rect.centery + 100))
        self.screen.blit(p2_text, p2_rect)

        # Update the display
        pygame.display.flip()

        # Wait for both players to be ready
        while not (self.player1.ready and self.player2.ready):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 7:
                    if event.joy == 0:
                        self.player1.ready = True
                    elif event.joy == 1:
                        self.player2.ready = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                       self.player1.ready = True
                    if event.key == pygame.K_e:
                       self.player2.ready = True
            screen.fill((255, 255, 255))
            # Draw the text
            self.screen.fill(WHITE)
            self.screen.blit(text, text_rect)

            # Update the player status text
            p1_color = BLACK if self.player1.ready else RED
            p1_text = p1_font.render("Player 1 - Ready" if self.player1.ready else "Player 1 - Not ready", True, p1_color)
            p1_rect = p1_text.get_rect(center=(text_rect.centerx, text_rect.centery + 50))
            self.screen.blit(p1_text, p1_rect)
            p2_color = BLACK if self.player2.ready else RED
            p2_text = p2_font.render("Player 2 - Ready" if self.player2.ready else "Player 2 - Not ready", True, p2_color)
            p2_rect = p2_text.get_rect(center=(text_rect.centerx, text_rect.centery + 100))
            self.screen.blit(p2_text, p2_rect)
          
            # Update the display
            pygame.display.flip()

            # Wait a bit to avoid using too much CPU
            pygame.time.wait(10)
    def update(self, dt):
        # Update the timer for block falling
        self.fall_timer += dt

    def run(self):
      
        while not self.both_players_ready:
            self.check_players_ready()
            self.display_splash_screen()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
            joystick_count = pygame.joystick.get_count()
            if joystick_count < 2:
                self.player1.handle_input()  # keyboard input
                self.player2.handle_input()  # keyboard input
            else:
                joystick1 = pygame.joystick.Joystick(0)
                joystick2 = pygame.joystick.Joystick(1)
                joystick1.init()
                joystick2.init()
                self.player1.handle_input(joystick1)  # joystick input
                self.player2.handle_input(joystick2)  # joystick input

            dt = self.clock.tick(FPS) / 1000.0
            self.update(dt)
            self.draw()
        pygame.quit()
    

pygame.init()
screen = pygame.display.set_mode((800, 600))
size = (800, 600)
game = Game(screen, size)
game.run()
