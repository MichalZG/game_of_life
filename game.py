
import time
from scipy.signal import convolve2d
import numpy as np
import pygame 
from PIL import Image, ImageDraw, ImageFont
from pygame.locals import *
import matplotlib.pyplot as plt

board_size = (1000, 1000)
resize = 3

filter_cell = np.ones((3, 3))
init_board = np.random.randint(2, size=board_size)

def text_phantom(text, board_size):
    font = 'arialbold'

    pil_font = ImageFont.truetype(font + ".ttf", size=board_size[0] // len(text),
                                  encoding="unic")
    text_width, text_height = pil_font.getsize(text)
    canvas = Image.new('RGB', board_size, (255, 255, 255))

    draw = ImageDraw.Draw(canvas)
    offset = ((board_size[0] - text_width) // 2,
              (board_size[1] - text_height) // 2)
    white = "#000000"

    draw.text(offset, text, font=pil_font, fill=white)

    return (255 - np.asarray(canvas)) // 255

init_board = np.flipud(np.rot90(text_phantom('KASIA', board_size)[..., 0]))


def step(board): 
    counts_board = convolve2d(board, filter_cell, mode='same', boundary='wrap') 
    counts_board -= board 
    
    new_life = (counts_board == 3)
    old_life = (board & (counts_board == 2))
    
    new_board = (new_life | old_life)
    return new_board


def play():
    board = step(init_board)
    pygame.init()
    display = pygame.display.set_mode(board_size)
    running = True
    run_flag = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        surf = pygame.surfarray.make_surface(board*255)
        # surf = pygame.transform.scale2x(surf)
        display.blit(surf, (0, 0))
        pygame.display.update()
        if not run_flag:
            input("Press Enter to continue...")
            run_flag = True
        board = step(board)
    pygame.quit()


if __name__ == "__main__":
    play()
