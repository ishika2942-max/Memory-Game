# Memory Challenge Game
# Developed by: Ishika Agarwal
# Submitted to: Jimson Mathew | CS1101
# Description: Tests memory by showing number sequences that increase every level.


import pygame
import random
import sys     #to call sys.exit()
import time

pygame.init()
pygame.mixer.init()      #to initialize the mixer for sound

# Screen Setup....................
WIDTH, HEIGHT = 1300, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✨✨....MEMORY GAME....✨✨")
clock = pygame.time.Clock()

#COLORS........................................
DARK_BG = (15, 20, 45)
LIGHT_BG = (35, 60, 120)
WHITE = (255, 255, 255)
GREEN = (80, 230, 120)
RED = (255, 80, 80)
GRAY = (230, 230, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 180, 255)
GRAY = (230, 230, 230)
CYAN = (0, 255, 255)
RED = (255, 80, 80)
GRAY = (230, 230, 230)
YELLOW = (255, 215, 0)

# Fonts...........................................................................
font_large=pygame.font.SysFont("comicsansms",90,bold=True,italic=True)
font_medium=pygame.font.SysFont("trebuchetms",60,bold=True,italic=True)
font_small=pygame.font.SysFont("arial",40,bold=True,italic=True)

background=pygame.image.load("background.jpg")
background=pygame.transform.scale(background, (WIDTH, HEIGHT))

# MUSIC.........................................................
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)
sound_correct = pygame.mixer.Sound("correct.mp3")
sound_wrong = pygame.mixer.Sound("wrong.mp3")

# USER-DEFINED Functions .........................................
def draw_text(text, font, color, y_offset=-50):                   # y_offset to position text vertically shifted from center
   render=font.render(text,True,color)                            # True for anti-aliasing i.e. smooth edges
   rect=render.get_rect(center=(WIDTH//2,HEIGHT//2 + y_offset))     # gets rectangle of the text surface and centers it
   screen.blit(render,rect)
   
    #Display a window with title and optional subtext........... Displays full screen message
def show_window(message, subtext=None, wait_time=2000):
    screen.blit(background, (0, 0))                          #Draws the background image at position (x=0, y=0) on screen
    draw_text(message, font_large, WHITE)
    if subtext:
        draw_text(subtext, font_small, WHITE, 80)
    pygame.display.flip()                                      #Refresh the display to show the updated content
    pygame.time.delay(wait_time)

#Draw number boxes horizontally...................................
def draw_boxes(numbers, y_offset=100):            
    box_w, box_h = 70, 70           #70*70 pixel boxes
    spacing = 20                         #spacing between each block
    total_w = len(numbers) * (box_w + spacing)      #total width of all boxes combined
    start_x = WIDTH // 2 - total_w // 2           #arrange them horizontally centered
                                
    for i, n in enumerate(numbers):         #i=index, n=number in the list   loops via each element and its index
        rect = pygame.Rect(start_x + i * (box_w + spacing), HEIGHT // 2 + y_offset, box_w, box_h)   #creates rectangle at calculated position, X-> moves right in each loop, Y-> use y_offset for vertical placement
        pygame.draw.rect(screen, GRAY, rect, border_radius=8)
        pygame.draw.rect(screen, BLUE, rect, 3, border_radius=8)
        text = str(n)                  #converting No. to string for rendering
        draw = font_medium.render(text, True, BLACK)
        screen.blit(draw,(rect.centerx - draw.get_width() / 2, rect.centery - draw.get_height() / 2))   


# ---........................ Game Screens ..........................---
def intro_screen():
    show_window("LET’S TEST YOUR MEMORY", "Press any key to start", 2000)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(30)

def show_instructions():
    show_window("Remember the Sequence", "You will see numbers for a few seconds", 2500)

#Show random numbers for 3 seconds.............."""
def show_numbers(sequence):
    screen.blit(background, (0, 0))
    draw_text("Memorize!", font_large, WHITE, -100)
    draw_boxes(sequence)
    pygame.display.flip()
    pygame.time.delay(3000)

"""Ask user to type numbers shown earlier.
           list(typed) -> converts typed digits into a list of characters   like '53'=['5', '3']
      ["_"] * (seq_len - len(typed))::::Creates underscore boxes for remaining empty slots
         Example (seq_len=4, typed="53"): ['_', '_']"""
def get_user_input(seq_len):
    typed = ""                           # String to store user input
    active = True
    while active:
        screen.blit(background, (0, 0))                  #Draws the background image at position (x=0, y=0) on screen
        draw_text("Enter the numbers", font_medium, WHITE, -120)
        draw_boxes(list(typed) + ["_"] * (seq_len - len(typed)))   
        pygame.display.flip()                           #Refresh the display to show the updated content   
     

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(typed) == seq_len:
                    active = False
                elif event.key == pygame.K_BACKSPACE:                   #Deletes last character (backspace).
                    typed = typed[:-1]
                elif event.unicode.isdigit() and len(typed) < seq_len:    #Checks if the key pressed is a digit and if there's space left
                    typed += event.unicode            #Appends the digit to the typed string

        if len(typed) == seq_len:
            pygame.time.delay(300)
            active = False

        clock.tick(30)

    return typed


def feedback_screen(correct):
    if correct:
        if sound_correct: sound_correct.play()
        show_window("Correct!", "Get ready for next level", 1500)
    else:
        if sound_wrong: sound_wrong.play()
        show_window("Game Over!", "You missed the sequence!", 2500)


# ............................ Game loop function....................................................
'''IDEA BEHIND LOOP............................:
1. Start at level 1 with a sequence length of 4.
2. In every loop:
   Show instructions.
   Generate a random sequence of numbers (length increases with level).
   Display the sequence for a few seconds.
   Get user input.Check if input matches the sequence.
    * If correct, increase level and repeat.
    * If incorrect, end the game and show final level.
                      '''
def game_loop():
    level = 1
    start_length = 4  # Start with 4 numbers
    while True:
        show_instructions()
        seq_length = start_length + (level - 1)  # sequence grows by 1 per level
        #sequence = [random.randint(0, 9) for _ in range(seq_length)]
        sequence = ""
        for _ in range(seq_length):
            sequence += str(random.randint(0, 9))

        show_numbers(sequence)
        user_input = get_user_input(len(sequence))

        if user_input == sequence:
            feedback_screen(True)
            level += 1
        else:
            feedback_screen(False)
            break

# Game Over...................................................................................
    screen.blit(background, (0, 0))
    draw_text("GAME OVER!", font_large, YELLOW, -50)   
    draw_text(f"You reached Level {level}", font_medium, WHITE, 80)
    draw_text("Press ENTER to Restart ", font_small, GREEN, 200)
    draw_text("Press ESC to Quit", font_small, RED, 250)
    pygame.display.flip()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:       #Pressed ENTER to restart
                    game_loop()                     # Restart the game
                elif event.key == pygame.K_ESCAPE:         #esc to quit
                    pygame.quit()
                    sys.exit()
        clock.tick(30)            #tels pygame to run game loop at 30 frames per second

def main():
    intro_screen()
    game_loop()
if __name__ == "__main__":
    main()