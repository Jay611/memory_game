import pygame
from random import *


# Set up game
def setup(level):
    global display_time
    display_time = max(5 - (level // 3), 1)   # Min: 1sec
    
    number_count = min((level // 3) + 5, 20)  # Max: 20 numbers
    
    # Arrange numbers on grid
    shuffle_grid(number_count)


def shuffle_grid(number_count):
    rows = 5
    columns = 9
    
    cell_size = 90
    button_size = 70
    screen_left_margin = 45
    screen_top_margin = 25
    
    grid = [[0 for col in range(columns)] for row in range(rows)]
    
    number = 1
    while number <= number_count:
        row_index = randrange(0, rows)
        col_index = randrange(0, columns)
        
        if grid[row_index][col_index] == 0:
            grid[row_index][col_index] = number
            number += 1

            # Calculate x, y of currnet cell
            center_x = screen_left_margin + (col_index * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_index * cell_size) + (cell_size  / 2)

            # Create number button
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)
            
            number_buttons.append(button)
         
# Display start screen
def display_start_screen():
   # Draw start button
    pygame.draw.circle(screen, WHITE, start_button.center, 40, 5)
    
    msg = game_font.render(f'{current_level}', True, WHITE) 
    msg_rect = msg.get_rect(center=start_button.center)
    screen.blit(msg, msg_rect)

# Check button corresponding to the position
def check_buttons(pos):
    global start, start_ticks

    if start:
        check_number_buttons(pos)
    elif start_button.collidepoint(pos):
        start = True
        start_ticks = pygame.time.get_ticks()

def check_number_buttons(pos):
    global start, hidden, current_level
    for button in number_buttons:
        if button.collidepoint(pos):
            if button == number_buttons[0]:
                del number_buttons[0]
                if not hidden:
                    hidden = True
            else:
                game_over()
            break
        
    if len(number_buttons) == 0:
        start = False
        hidden = False
        current_level += 1
        setup(current_level)

# Game over
def game_over():
    global running
    running = False
    
    msg = game_font.render(f'Your level is {current_level}', True, WHITE) 
    msg_rect = msg.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.fill(BLACK)
    screen.blit(msg, msg_rect)

# Display game screen
def display_game_screen():
    global hidden
    
    if not hidden:
        elasped_time = (pygame.time.get_ticks() - start_ticks) / 1000
        if elasped_time > display_time:
            hidden = True
    
    for idx, rect in enumerate(number_buttons, start=1):
        if hidden:
            pygame.draw.rect(screen, WHITE, rect)
        else:
            # Display numbers
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)

# Game init
pygame.init()
screen_width = 900
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Memory Game')
game_font = pygame.font.Font(None, 100)   # Define font

# Start button
start_button = pygame.Rect(0, 0, 80, 80)
start_button.center = (80, screen_height - 80)

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

number_buttons = []
current_level = 1
display_time = None  # Time showing numbers
start_ticks = None

# Game start?
start = False


hidden = False

setup(current_level)

running = True

while running:
    click_pos = None  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()
            
            
    screen.fill(BLACK)
    
    if start:
        display_game_screen()
    else:
        display_start_screen()
        
    if click_pos:
        check_buttons(click_pos)
    
    pygame.display.update()


pygame.time.delay(5000)
pygame.quit()