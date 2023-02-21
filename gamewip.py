import pygame
import random

# Define some colors
BLACK, WHITE, BLUE, RED, YELLOW, GRAY = (0, 0, 0), (255, 255, 255), (0, 0, 255), (255, 0, 0), (255, 255, 0), (128, 128, 128)

# Define the size of the game grid and blocks
GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE = 8, 12, 64


class Block:
    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.block_type = block_type
        if block_type == 1:
            self.texture = "wood.png"
        elif block_type == 2:
            self.texture = "rock.png"
        elif block_type == 3:
            self.texture = "diamond.png"
        elif block_type == 4:
            self.texture = "bomb.png"
        elif block_type == 5:
            self.texture = "missile.png"
        self.texture = pygame.image.load(self.texture).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (BLOCK_SIZE, BLOCK_SIZE))

    def draw(self, screen):
        screen.blit(self.texture, (self.x, self.y))
    
#class for the player, including the grid, blocks, and the next set of blocks, 
#ensure a set of blocks only spawns after the current one has reached the bottom of the grid
class Player:
    def __init__(self, x, y, block_size, grid_size):
        self.x = x
        self.y = y
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.blocks = []
        self.block_size = block_size
        self.grid_size = grid_size
        self.next_blocks = []  # store the next set of blocks here
        self.generate_blocks()  # generate the first set of blocks
        self.is_ready = False
        self.timer = pygame.time.get_ticks()   # Initialize the timer
        self.speed = 1
        self.block_y = 0

    def check_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left()
            elif event.key == pygame.K_RIGHT:
                self.move_right()
            elif event.key == pygame.K_SPACE:
                self.rotate()
            elif event.key == pygame.K_DOWN:
                self.drop()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.ready()
            elif event.key == pygame.K_SPACE:
                self.ready()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.move_left()
            elif event.key == pygame.K_d:
                self.move_right()
            elif event.key == pygame.K_q:
                self.rotate()
            elif event.key == pygame.K_s:
                self.drop()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                self.ready()
            elif event.key == pygame.K_q:
                self.ready()
                
    def generate_blocks(self):
        # Generate a random L-shaped block (2 blocks wide and 2 blocks tall), that falls down the grid slowly and can be controlled by players - a new set will only generate once the current set has reached the bottom of the grid
        self.blocks = []
        self.current_height = 0
        block_type = random.randint(1, 5)
        self.blocks.append(Block(self.x + self.grid_size[0] // 2 - self.block_size, self.y + self.current_height, block_type))
        block_type = random.randint(1, 5)
        self.blocks.append(Block(self.x + self.grid_size[0] // 2, self.y + self.current_height, block_type))
        block_type = random.randint(1, 5)
        self.blocks.append(Block(self.x + self.grid_size[0] // 2, self.y + self.block_size + self.current_height, block_type))
        self.current_height = self.block_size
        self.ready = True

    #handle movement of sets of blocks, once a set is at the bottom of the grid, it will be added to the grid and a new set will be generated, a set can only move when it's not added to the grid
    def move_left(self):
        if self.ready:
            for block in self.blocks:
                block.x -= self.block_size
                if block.x < self.x or self.check_collision():
                    block.x += self.block_size
                    break
    
    def move_right(self):
        if self.ready:
            for block in self.blocks:
                block.x += self.block_size
                if block.x >= self.x + self.grid_size[0] or self.check_collision():
                    block.x -= self.block_size
                    break
    
    def rotate(self):
        if self.ready:
            for block in self.blocks:
                block.x, block.y = block.y, block.x
                block.x = self.x + self.grid_size[0] // 2 - (block.x - self.x - self.grid_size[0] // 2)
                if block.x < self.x or block.x >= self.x + self.grid_size[0] or block.y < self.y or block.y >= self.y + self.grid_size[1] or self.check_collision():
                    block.x, block.y = block.y, block.x
                    block.x = self.x + self.grid_size[0] // 2 - (block.x - self.x - self.grid_size[0] // 2)
                    break
    
    
    #sets of blocks will drop down the grid using the self.speed, a collision check will be performed every time the set drops down by 1 block and when a block or blocks collide with the bottom of the grid or another block, the set will be added to the grid and a new set will be generated, when a set is added to the grid all blocks within it must be added and like a classic puzzle game blocks that land on top of an empty cell will drop further to fill the empty cells
    def drop(self):
        if self.ready:
            for block in self.blocks:
                block.y += self.block_size
                if block.y >= self.y + self.grid_size[1] or self.check_collision():
                    block.y -= self.block_size
                    self.add_to_grid()
                    self.generate_blocks()
                    self.ready = False
                    break
    
    def add_to_grid(self):
        for block in self.blocks:
            x = (block.x - self.x) // self.block_size
            y = (block.y - self.y) // self.block_size
            self.grid[y][x] = block.block_type

    #check for collision 
    def check_collision(self, x=None, y=None):
        if x is None and y is None:
            for block in self.blocks:
                # Check if any part of the block set is hitting another block on the grid
                block_row = (block.y - self.y) // self.block_size
                block_col = (block.x - self.x) // self.block_size
                if self.grid[block_row][block_col] != 0:
                    return True
                # Check if any part of the block set is hitting the sides of the grid
                if block.x < self.x or block.x >= self.x + self.grid_size[0]:
                    return True
                # Check if any part of the block set is hitting the bottom of the grid
                if block.y + self.block_size >= self.y + self.grid_size[1]:
                    return True
            return False
        else:
            # Check if any part of the block set is hitting another block on the grid
            block_row = (y - self.y) // self.block_size
            block_col = (x - self.x) // self.block_size
            if self.grid[block_row][block_col] != 0:
                return True
            # Check if any part of the block set is hitting the sides of the grid
            if x < self.x or x >= self.x + self.grid_size[0]:
                return True
            # Check if any part of the block set is hitting the bottom of the grid
            if y + self.block_size >= self.y + self.grid_size[1]:
                return True
            return False

    def ready(self):
        self.is_ready = True


    def update(self):
        if self.is_ready:
            for block in self.blocks:
                if block.y + self.block_size >= self.y + self.grid_size[1] - self.block_size:
                    block.y = self.y + self.grid_size[1] - self.block_size
                    self.add_to_grid()
                    self.generate_blocks()
                    self.is_ready = False
                    break
                elif self.check_collision(block.x, block.y + self.block_size):
                    block.y -= self.block_size
                    self.add_to_grid()
                    self.generate_blocks()
                    self.is_ready = False
                    break

        
    def draw(self):
        # draw the grid
        pygame.draw.rect(self.win, self.grid_color, (self.x, self.y, self.grid_size[0], self.grid_size[1]))
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if self.grid[row][col] != 0:
                    pygame.draw.rect(self.win, self.block_color, (self.x + col * self.block_size, self.y + row * self.block_size, self.block_size, self.block_size))
        # draw the blocks
        for block in self.blocks:
            pygame.draw.rect(self.win, self.block_color, (block.x, block.y, self.block_size, self.block_size))
        # draw the grid lines
        for row in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.win, (255, 255, 255), (self.x, self.y + row * self.block_size), (self.x + self.grid_size[0], self.y + row * self.block_size))
        for col in range(GRID_WIDTH + 1):
            pygame.draw.line(self.win, (255, 255, 255), (self.x + col * self.block_size, self.y), (self.x + col * self.block_size, self.y + self.grid_size[1]))


    def add_to_grid(self):
        for block in self.blocks:
            row = (block.y - self.y) // self.block_size
            col = (block.x - self.x) // self.block_size
            if row >= 0 and row < GRID_HEIGHT and col >= 0 and col < GRID_WIDTH:
                self.grid[row][col] = block.block_type


    def check_game_over(self):
        # Check if the game is over
        for col in range(GRID_WIDTH):
            if self.grid[0][col] != 0:
                return True
        return False
    
    

    def ready(self):
        self.ready = False
    
    def update(self):
        # move the blocks down slowly and allow players to move them
        self.timer += 1
        if self.timer >= self.speed:
            self.timer = 0
            if self.ready:
                for block in self.blocks:
                    block.y += self.block_size
                    if block.y >= self.y + self.grid_size[1] or self.check_collision():
                        block.y -= self.block_size
                        self.add_to_grid()
                        self.generate_blocks()
                        if self.check_game_over():
                            self.game_over = True
                        break
            else:
                self.ready = True


    def draw(self, screen):
        # Fill the empty cells with a gray background color
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if self.grid[row][col] == 0:
                    pygame.draw.rect(screen, GRAY, [self.x + col * self.block_size, self.y + row * self.block_size, self.block_size, self.block_size])

        # Draw the grid lines
        for i in range(GRID_WIDTH + 1):
            pygame.draw.line(screen, BLACK, (self.x + i * self.block_size, self.y), (self.x + i * self.block_size, self.y + self.grid_size[1]))
        for i in range(GRID_HEIGHT + 1):
            pygame.draw.line(screen, BLACK, (self.x, self.y + i * self.block_size), (self.x + self.grid_size[0], self.y + i * self.block_size))

        # Draw the landed blocks
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if self.grid[row][col] != 0:
                    block_type = self.grid[row][col]
                    block = Block(self.x + col * self.block_size, self.y + row * self.block_size, block_type)
                    block.draw(screen)

        # Draw the falling blocks
        for block in self.blocks:
            block.draw(screen)


class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Get the current display size
        display_info = pygame.display.Info()
        width = display_info.current_w
        height = display_info.current_h

        # Set the size of the screen to the current display size
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)

        # Set the caption of the window
        pygame.display.set_caption("Game Prototype")

        # Define the size and position of the grid areas on the screen
        padding = 200
        margin = (self.size[1] - (GRID_HEIGHT * BLOCK_SIZE)) // 2
        grid_width = GRID_WIDTH * BLOCK_SIZE
        grid_height = GRID_HEIGHT * BLOCK_SIZE

        player1_x = (self.size[0] - (2 * grid_width + padding)) // 2
        player1_y = margin
        player2_x = player1_x + grid_width + padding
        player2_y = margin

        # Create the game grids for each player
        self.player1_grid_size = (grid_width, grid_height)
        self.player2_grid_size = (grid_width, grid_height)
        self.player1 = Player(player1_x, player1_y, BLOCK_SIZE, self.player1_grid_size)
        self.player2 = Player(player2_x, player2_y, BLOCK_SIZE, self.player2_grid_size)
    
    
    # create a method to display a splash screen, two players need to press the start button on the joypad or on keyboard before the game can start
    # for player 1, the start button is 'e'and for player 2 the start button is Enter
    def splash_screen(self):
        # Create a font
        font = pygame.font.SysFont("Calibri", 25, True, False)

        # Render the text
        text = font.render("Press 'e' for player 1 and Enter for player 2 to start the game", True, BLACK)

        # Get the size of the text (why is font.size a string?)
        text_size = font.size("Press 'e' for player 1 and Enter for player 2 to start the game")
        # Get the position of the text
        text_x = (self.size[0] - text_size[0]) // 2
        text_y = (self.size[1] - text_size[1]) // 2
        # fill entire screen with white
        self.screen.fill(WHITE)
        # Draw the text on the screen
        self.screen.blit(text, [text_x, text_y])

        # Update the screen
        pygame.display.flip()

        # Wait for the player to press the start button
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.player1.is_ready=True
                    if event.key == pygame.K_RETURN:
                        self.player2.is_ready=True
                    if self.player1.is_ready == True and self.player2.is_ready == True:
                        # Both players are ready, break out of the while loop
                        self.run()
            self.screen.fill(WHITE)
            self.screen.blit(text, [text_x, text_y])
            pygame.display.flip()


    def game_over_screen(self, player):
        # Create a font
        font = pygame.font.SysFont("Calibri", 25, True, False)

        # Render the text
        text = font.render("Player {} wins!".format(player), True, BLACK)

        # Get the size of the text
        text_size = font.size("Player {} wins!".format(player))

        # Get the position of the text
        text_x = (self.size[0] - text_size[0]) // 2
        text_y = (self.size[1] - text_size[1]) // 2

        # Draw the text on the screen
        self.screen.blit(text, [text_x, text_y])

        # Update the screen
        pygame.display.flip()

        # Wait for the player to press the start button
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:
                        return
        
   
   
    def run(self):
        # Game loop
        done = False
        clock = pygame.time.Clock()
        while not done:
            # check if Escape key is pressed amd exit the game if it is
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    
              

            # Update the game state
            self.player1.update()
            self.player2.update()

            # Draw the game on the screen
            self.screen.fill(WHITE)
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            pygame.display.flip()

            # Limit to 60 frames per second
            clock.tick(5)

        # Quit Pygame
        pygame.quit()
        sys.exit()
game = Game()
game.splash_screen()
