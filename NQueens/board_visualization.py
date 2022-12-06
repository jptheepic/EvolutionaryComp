import pygame
import random
from typing import TypedDict


class Individual(TypedDict):
    genome: list
    fitness: int


### This file will cotnain the tools used for visualization
def draw_board(indiv: Individual, iteration=0):
    """This will draw the chess board and the show where the errors occur on the board based on an individuals genome

    Args:
        indiv (Individual): An Individual genome object must have a genome and a fitness
        iteration (int, optional): _description_. Defaults to 0. used for showing what iteration the indivudal is on in the graphic.
    """

    pygame.init()
    colors = [(255, 0, 0), (0, 0, 0)]  # Set up colors [red, black]

    n = len(indiv["genome"])  # This is an NxN chess board.
    surface_sz = 480
    sq_sz = surface_sz // n  # sq_sz is length of a square.
    surface_sz = n * sq_sz
    pygame.display.set_caption(f"Iteration {iteration}")
    # Create the surface of (width, height), and its window.
    surface = pygame.display.set_mode((surface_sz, surface_sz))

    queen = pygame.image.load("queen.png")
    queen = pygame.transform.scale(queen, (sq_sz, sq_sz))

    # Use an extra offset to centre the queen in its square.
    queen_offset = (sq_sz - queen.get_width()) // 2

    while True:

        # Look for an event from keyboard, mouse, etc.
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break

        # Draw a fresh background (a blank chess board)
        for row in range(n):  # Draw each row of the board.
            c_indx = row % 2  # Alternate  color
            for col in range(n):
                the_square = (col * sq_sz, row * sq_sz, sq_sz, sq_sz)
                surface.fill(colors[c_indx], the_square)
                c_indx = (c_indx + 1) % 2

        # Now that squares are drawn, draw the queens.
        for (col, row) in enumerate(indiv["genome"]):
            surface.blit(
                queen, (col * sq_sz + queen_offset, row * sq_sz + queen_offset)
            )

        right_diagional, left_diagional, rpt_fit = evaluate_individual(indiv)
        # Now we will evaluate the solution and put lines showing
        # horizontal violations

        # Creating a consistant offset to graph the lines
        for (col, row) in enumerate(indiv["genome"]):
            if right_diagional[col] != None:
                draw_evaluation_lines(error_array=right_diagional,idx=col,indiv=indiv,square_size=sq_sz,surface=surface)
            if left_diagional[col] != None:
                draw_evaluation_lines(error_array=left_diagional,idx=col,indiv=indiv,square_size=sq_sz,surface=surface)
            if rpt_fit[col] != None:
                draw_evaluation_lines(error_array=rpt_fit,idx=col,indiv=indiv,square_size=sq_sz,surface=surface)


        pygame.display.flip()

    pygame.quit()


def draw_evaluation_lines(error_array:list, idx:int, indiv:Individual,surface:pygame.surface,square_size:int):
    """This function will take in the array's produced by evaluating the indiviuals along their three axis. It will take each of these list
    one at a time

    Args:
        error_array (list): list of board size containing a non-zero where an error has occured
        idx (int): index of where this error occured in the individuals genome
        indiv (Individual): Indivual object must have a fitness and a genome
        surface (pygame.surface): pygame surface to draw the line onto
        square_size (int): size of squares on chess board. For scaling 
    """
    line_offset = square_size / 2

    indexs_of_error = [
        index for index, elem in enumerate(error_array) if elem == error_array[idx]
    ]
    if len(indexs_of_error) != 0:
        pos1 = (
            indexs_of_error[-1] * square_size + line_offset,
            indiv["genome"][indexs_of_error[-1]] * square_size + line_offset,
        )
        endpos = (
            indexs_of_error[0] * square_size + line_offset,
            indiv["genome"][indexs_of_error[0]] * square_size + line_offset,
        )
        pygame.draw.line(surface, (160, 160, 160), pos1, endpos, 5)


def evaluate_individual(indiv: Individual):
    """This will evaulate an indiviodual and return the arrays of errors at various positions.

    Args:
        indiv (Individual): Indivual object must have a fitness and a genome

    Returns:
        List,List,List: Will return three list of errors that occrued on the right diagonals, left diagionsal, and in the same row 
    """

    left_diagional = []
    right_diagional = []
    for col, row in enumerate(indiv["genome"]):
        row = int(row)
        if row - col == 0:
            left_diagional.append(0)
        elif row - col < 0:
            left_diagional.append((row - col))
        elif (row - col) > 0:
            left_diagional.append(row - col)
        right_diagional.append(row + col)
    right_diagional = [
        i if right_diagional.count(i) > 1 else None for i in right_diagional
    ]
    left_diagional = [i if left_diagional.count(i) > 1 else None for i in left_diagional]
    matching_row = [i if indiv["genome"].count(i) > 1 else None for i in indiv["genome"]]

    return right_diagional, left_diagional, matching_row


if __name__ == "__main__":
    # Initialing a random board size for testing 
    board_size = 8
    lst = range(0, board_size)
    # Draw a random board with the passed board size
    draw_board(Individual(genome=random.sample(lst, k=board_size), fitness=0))
