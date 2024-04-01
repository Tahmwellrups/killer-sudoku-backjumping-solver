# Project by: Tupas, Ramwell P.
import numpy as np
import pygame
import sys
from button import Button

cages = []

BG = pygame.Color("#203972")
BLUE = pygame.Color("#3E5AAA")
H_BLUE = pygame.Color("#6477AF")
BLACK = pygame.Color("#101B3B")
RED = pygame.Color("#FF7276")
H_RED = pygame.Color("#FFAAAC")
YELLOW = pygame.Color("#FFF36D")
H_YELLOW = pygame.Color("#EBE6B6")
WHITE = pygame.Color("#FFFFFF")

ROW_COUNT = 4
COLUMN_COUNT = 4
SQUARESIZE = 125

board_width = COLUMN_COUNT * SQUARESIZE
board_height = (ROW_COUNT+1) * SQUARESIZE
cell = board_width // 2
size = (board_width, board_height)

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

button_width = 110
button_height = 30

pygame.init()

background_image = pygame.image.load("resources/MENU.png")
pygame.display.set_caption("KILLER SUDOKU AI")

# Backjumping algorithm functions
def solve_backjumping(board, cages):
    # If the algorithm is in dead end, it will return to the first square of the board, thus backjumping
    return solve_backjumping_helper(board, cages, 0, 0) 

def solve_backjumping_helper(board, cages, row, col):
    if is_board_full(board):  # Check if the board is completely filled
        print(board)
        cages.clear()
        solution_found(board)
        return True

    empty_cell = find_empty_cell(board)
    row, col = empty_cell

    for num in range(1, 5):  # Board values range from 1 to 4
        if is_safe(board, cages, row, col, num):  # Check if placing 'num' at (row, col) is valid
            board[row][col] = num  # Place the number on the board
            if solve_backjumping_helper(board, cages, row, col):  # Recursively solve the next empty cell
                return True
            board[row][col] = 0  # If no solution found, backtrack by resetting the cell
    return False  # If no number can be placed at (row, col), backtrack further

def is_board_full(board):
    for row in board:
        if 0 in row:  # If any cell is empty, the board is not full
            return False
    return True

def find_empty_cell(board):
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT):
            if board[i][j] == 0:  # Return the first empty cell
                return i, j
    return None

def is_safe(board, cages, row, col, num):
    # Check row, column, and cage constraints
    return (
        is_unique_in_row(board, row, num) and
        is_unique_in_column(board, col, num) and
        is_unique_in_cage(board, cages, row, col, num)
    )

def is_unique_in_row(board, row, num):
    return num not in board[row]

def is_unique_in_column(board, col, num):
    return num not in [board[i][col] for i in range(ROW_COUNT)]

def is_unique_in_cage(board, cages, row, col, num):
    for sum_value, group in cages:
        if (row, col) in group:
            cage_sum = sum_value
            cage_nums = [board[r][c] for r, c in group if board[r][c] != 0]

            if num in cage_nums or sum(cage_nums) + num > cage_sum:
                return False
    return True

def solution_found(final_board):
    game_bg = pygame.image.load("resources/GAME BG.png")
    screen.blit(game_bg, (0,0))
    draw_final_board(final_board)

    while True:
        OVER_MOUSE_POS = pygame.mouse.get_pos()
        MENU_BUTTON = Button(image=None, pos=((screen_width//2)-(button_width//2)+55,(screen_height//2)+300), 
                             text_input="MAIN MENU", font=get_font(40,2), base_color="#D32735", hovering_color=H_RED)

        for button in [MENU_BUTTON]:
            button.changeColor(OVER_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.checkForInput(OVER_MOUSE_POS):
                    main()
        pygame.display.flip()		

def draw_final_board(final_board):
    font = pygame.font.SysFont("Arial Narrow", 25) 
    width_center = (screen_width/2) - (board_width/2)
    # Board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, WHITE, ((c*SQUARESIZE)+width_center, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))       
    # Cell lines
    for i in range(0, board_width, cell): # vertical
        if i != 0:
            pygame.draw.line(screen, RED, (width_center+i,SQUARESIZE),(width_center+i,board_height), 4)
    for j in range(0, (board_height-SQUARESIZE), cell): # horizontal
        if j != 0:
            pygame.draw.line(screen, RED, (width_center, SQUARESIZE + j), (width_center + board_width, SQUARESIZE + j), 4)
    # Square Lines
    for i in range(0, board_width, SQUARESIZE): # vertical
        if i % cell != 0:
            pygame.draw.line(screen, RED, (width_center+i,SQUARESIZE),(width_center+i,board_height), 1)
    for j in range(0, board_height, SQUARESIZE): # horizontal
        if j % cell != 0:
            pygame.draw.line(screen, RED, (width_center, SQUARESIZE + j), (width_center + board_width, SQUARESIZE + j), 1)
    
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            value = final_board[r][c]
            text = font.render(str(int(value)), True, pygame.Color("#D32735"))
            text_rect = text.get_rect(center=((c * SQUARESIZE) + width_center + SQUARESIZE // 2, r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2))
            screen.blit(text, text_rect)

# Main game functions
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def print_board(board):
    print(board)

def is_valid_location(board, row, col):
    return board[row][col] == 0

def is_clicked(board, row, col):
    return board[row][col] == 41

def square_selected(board, row, col, square):
    board[row][col] = square

def is_board_filled(board):
    for row in board:
        for value in row:
            if not (0 < value < 41):
                return False
    return True

def set_sum(board, sum):
    group = []
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == 41:
                board[r][c] = sum
                group.append((r, c))
    cages.append((sum, group))

def input_sum(sum):
    font = pygame.font.SysFont("Arial Narrow", 25)
    small_font = pygame.font.SysFont("Arial Narrow", 20)
    shadow_offset = 2  

    shadow_box = pygame.Rect((screen_width//2)-150 + shadow_offset, (screen_height//2)-40 + shadow_offset, 300, 100)
    shadow_color = (0, 0, 0, 128)  
    pygame.draw.rect(screen, shadow_color, shadow_box)

    main_box = pygame.Rect((screen_width//2)-150, (screen_height//2)-40, 300, 100)
    pygame.draw.rect(screen, pygame.Color("#D32735"), main_box)
    input_text = font.render(f"ENTER SUM: {sum}", True, WHITE)
    text_rect = input_text.get_rect(center=main_box.center)
    screen.blit(input_text, text_rect)
    small_text = small_font.render("Press ENTER to confirm", True, pygame.Color("#D32735"))
    small_text_rect = small_text.get_rect(midtop=(main_box.centerx, main_box.bottom + 5)) 
    screen.blit(small_text, small_text_rect)


def get_sum(board):
    current_sum = 0
    sum_input = True
    # input_sum(current_sum)
    while sum_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    num_pressed = event.key - pygame.K_0
                    current_sum = current_sum * 10 + num_pressed
                if event.key == pygame.K_RETURN:
                    set_sum(board, current_sum)
                    current_sum = 0
                    sum_input = False
                elif event.key == pygame.K_BACKSPACE:      
                    current_sum = current_sum // 10
                    
        input_sum(current_sum)
        pygame.display.update()
            

def draw_cages(cages):
    font = pygame.font.SysFont("Arial Narrow", 25) 
    list_font = pygame.font.SysFont("Arial Narrow", 22) 
    width_center = (screen_width/2) - (board_width/2)
    
    for sum_value, group in cages:
        for r, c in group:
            pygame.draw.rect(screen, BG, ((c * SQUARESIZE) + width_center, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            text = font.render(str(sum_value), True, WHITE)
            text_rect = text.get_rect(center=((c * SQUARESIZE) + width_center + SQUARESIZE // 2, r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2))
            screen.blit(text, text_rect)
    # If cages exist
    if cages:
        margin = 10  # Margin between each line of text
        i = 0
        x = 30
        y = SQUARESIZE
        for sum_value, groups in cages:
            i += 1
            text = list_font.render(f"{i}. {sum_value}, {groups}", True, WHITE)
            text_rect = text.get_rect(topleft=(x, y))
            screen.blit(text, text_rect)
            y += text_rect.height + margin  # Update y position for the next line of text

def draw_board(board):
    width_center = (screen_width/2) - (board_width/2)
    # Board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, WHITE, ((c*SQUARESIZE)+width_center, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)) 
    # Highlights
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == 41:
                pygame.draw.rect(screen, BLUE, ((c*SQUARESIZE)+width_center, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))      
    # Cell lines
    for i in range(0, board_width, cell): # vertical
        if i != 0:
            pygame.draw.line(screen, RED, (width_center+i,SQUARESIZE),(width_center+i,board_height), 4)
    for j in range(0, (board_height-SQUARESIZE), cell): # horizontal
        if j != 0:
            pygame.draw.line(screen, RED, (width_center, SQUARESIZE + j), (width_center + board_width, SQUARESIZE + j), 4)
    # Square Lines
    for i in range(0, board_width, SQUARESIZE): # vertical
        if i % cell != 0:
            pygame.draw.line(screen, RED, (width_center+i,SQUARESIZE),(width_center+i,board_height), 1)
    for j in range(0, board_height, SQUARESIZE): # horizontal
        if j % cell != 0:
            pygame.draw.line(screen, RED, (width_center, SQUARESIZE + j), (width_center + board_width, SQUARESIZE + j), 1)
    # Groups
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):	
            if 0 < board[r][c] < 41:
                pygame.draw.rect(screen, BG, ((c*SQUARESIZE)+width_center, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))

    pygame.display.update()

def killer_sudoku():
    game_bg = pygame.image.load("resources/GAME BG.png")
    screen.blit(game_bg, (0,0))

    board = create_board()
    print_board(board)
    draw_board(board)
    # draw_buttons()
    solving = True
    square = 41 # Since the highest possible cage is 40, we'll use 41 as a placeholder for each square clicked.
    width_center = (screen_width/2) - (board_width/2) # Starting point of board width

    while solving:
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        RESET_BUTTON = Button(image=None, pos=((screen_width//6)-130,(screen_height//2)+325), 
                            text_input="RESET", font=get_font(35, 2), base_color=RED, hovering_color=H_RED)
        CONFIRM_BUTTON = Button(image=None, pos=((screen_width//2)-(button_width//2)+55,(screen_height//2)+300), 
                            text_input="CONFIRM", font=get_font(35, 2), base_color="#D32735", hovering_color=H_RED)
        SOLVE_BUTTON = Button(image=None, pos=(screen_width-80,(screen_height//2)+325), 
                            text_input="SOLVE", font=get_font(35, 2), base_color=RED, hovering_color=H_RED)
        MENU_BUTTON = Button(image=None, pos=(100,30), 
                            text_input="BACK TO MENU", font=get_font(30, 2), base_color=BLUE, hovering_color=H_BLUE)

        for button in [RESET_BUTTON, CONFIRM_BUTTON, SOLVE_BUTTON, MENU_BUTTON]:
            button.changeColor(GAME_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0] # X coordinate
                posy = event.pos[1] # Y coordinate
                # Will only accept x and y coordinates within the board parameters
                if width_center <= posx <= (width_center + board_width) and SQUARESIZE <= posy <= (board_height):
                    col = int((posx - width_center) // SQUARESIZE)
                    row = int((posy - SQUARESIZE) // SQUARESIZE)
                    # If the square is clicked it will highlight, else it will erase the highlight
                    if is_valid_location(board, row, col):
                        print("(", row, col, ")")
                        square_selected(board, row, col, square)
                    elif is_clicked(board, row, col):
                        print("(", row, col, ")")
                        square_selected(board, row, col, 0)
                if RESET_BUTTON.checkForInput(GAME_MOUSE_POS):
                    board = create_board()
                    cages.clear()
                    screen.blit(game_bg, (0,0))   

                if MENU_BUTTON.checkForInput(GAME_MOUSE_POS):
                    solving = False
                    main()  
                        
                # Confirm button will only accept when there is a squared selected 
                if any(41 in row for row in board):
                    if CONFIRM_BUTTON.checkForInput(GAME_MOUSE_POS):
                        get_sum(board)

                if is_board_filled(board):
                    if SOLVE_BUTTON.checkForInput(GAME_MOUSE_POS):
                        board = create_board() # Creating a new board
                        if solve_backjumping(board, cages):
                            print("Solution Found")
                            cages.clear()
                        else:
                            print("No Solution Found")
                            cages.clear()
                            

                                    
                print_board(board)
                draw_board(board)
                draw_cages(cages)

        pygame.display.flip()
            
# Frontend functions
def get_font(size, type):
    if type == 1:
        return pygame.font.SysFont("berlin sans fb demi", size)
    if type == 2:
        return pygame.font.SysFont("Arial Narrow", size)

def controls():
    controls_bg = pygame.image.load("resources/CONTROLS.png")
    screen.blit(controls_bg, (0, 0))

    while True:
        CONTROLS_MOUSE = pygame.mouse.get_pos()
        BACK_BUTTON = Button(image=None, pos=(1160, 650), 
                            text_input="BACK", font=get_font(50, 1), base_color="#D32735", hovering_color=RED)

        for button in [BACK_BUTTON]:
            button.changeColor(CONTROLS_MOUSE)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(CONTROLS_MOUSE):
                    main()
            
        pygame.display.flip()   	

def main():
    running = True 
    while running:
        screen.blit(background_image, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BUTTON = Button(image=None, pos=(960, 350), 
                            text_input="PLAY GAME", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        CONTROLS_BUTTON = Button(image=None, pos=(960, 450), 
                            text_input="CONTROLS", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        QUIT_BUTTON = Button(image=None, pos=(960, 550), 
                            text_input="QUIT GAME", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        
        for button in [PLAY_BUTTON, CONTROLS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    killer_sudoku()
                if CONTROLS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    controls()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            
        pygame.display.update()
    
main()
