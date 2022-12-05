import pygame    
import random  
from typing import TypedDict


class Individual(TypedDict):
    genome: list
    fitness: int

### This file will cotnain the tools used for visualization
def draw_board(indiv:Individual, iteration=0):
    """ Draw a chess board with queens, as determined by the indivual genome. """

    pygame.init()                  
    colors = [(255,0,0), (0,0,0)]    # Set up colors [red, black]

    n = len(indiv['genome'])         # This is an NxN chess board.
    surface_sz = 480                                    
    sq_sz = surface_sz // n    # sq_sz is length of a square.          
    surface_sz = n * sq_sz     
    pygame.display.set_caption(f"Iteration {iteration}")
    # Create the surface of (width, height), and its window.
    surface = pygame.display.set_mode((surface_sz, surface_sz))

    queen = pygame.image.load("queen.png")
    queen = pygame.transform.scale(queen,(sq_sz,sq_sz))

    # Use an extra offset to centre the queen in its square.
    queen_offset = (sq_sz-queen.get_width()) // 2

    while True:

        # Look for an event from keyboard, mouse, etc.
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break;

        # Draw a fresh background (a blank chess board)
        for row in range(n):           # Draw each row of the board.
            c_indx = row % 2           # Alternate  color 
            for col in range(n):       
                the_square = (col*sq_sz, row*sq_sz, sq_sz, sq_sz)
                surface.fill(colors[c_indx], the_square) 
                c_indx = (c_indx + 1) % 2   

        # Now that squares are drawn, draw the queens.
        for (col, row) in enumerate(indiv['genome']):
          surface.blit(queen, 
                   (col*sq_sz+queen_offset,row*sq_sz+queen_offset))
        
        right_diagional,left_diagional,rpt_fit = eval_diagionals(indiv)
        # Now we will evaluate the solution and put lines showing
        # horizontal violations
        # line_offset =(sq_sz-queen.get_width()) // 2
        line_offset=sq_sz/2
        for (col, row) in enumerate(indiv['genome']):
            if right_diagional[col] != 0:
                indexs_of_error = [index for index, elem in enumerate(right_diagional) if elem == right_diagional[col]]
                if len(indexs_of_error) !=0:
                    pos1 = (indexs_of_error[-1]*sq_sz+line_offset,indiv['genome'][indexs_of_error[-1]]*sq_sz+line_offset)
                    endpoint = (indexs_of_error[0]*sq_sz+line_offset,indiv['genome'][indexs_of_error[0]]*sq_sz+line_offset)
                    pygame.draw.line(surface,(160,160,160),pos1,endpoint,5)
            if left_diagional[col] != 0:
                indexs_of_error = [index for index, elem in enumerate(left_diagional) if elem == left_diagional[col]]
                if len(indexs_of_error) !=0:
                    pos1 = (indexs_of_error[-1]*sq_sz+line_offset,indiv['genome'][indexs_of_error[-1]]*sq_sz+line_offset)
                    endpoint = (indexs_of_error[0]*sq_sz+line_offset,indiv['genome'][indexs_of_error[0]]*sq_sz+line_offset)
                    pygame.draw.line(surface,(160,160,160),pos1,endpoint,5)
            if rpt_fit[col] !=0:
                indexs_of_error = [index for index, elem in enumerate(rpt_fit) if elem == rpt_fit[col]]
                if len(indexs_of_error) !=0:
                    pos1 = (indexs_of_error[-1]*sq_sz+line_offset,indiv['genome'][indexs_of_error[-1]]*sq_sz+line_offset)
                    endpoint = (indexs_of_error[0]*sq_sz+line_offset,indiv['genome'][indexs_of_error[0]]*sq_sz+line_offset)
                    pygame.draw.line(surface,(160,160,160),pos1,endpoint,5)


        pygame.display.flip()


    pygame.quit()

def eval_diagionals(indiv:Individual):
    """
    This function will return a list of shared diagionals on the chessboard 
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
    right_diagional = [i if right_diagional.count(i) > 1 else 0 for i in right_diagional]
    left_diagional = [i if left_diagional.count(i) > 1 else 0 for i in left_diagional]
    rpt_fit = [i if indiv['genome'].count(i) > 1 else 0 for i in indiv['genome']]

    return right_diagional,left_diagional,rpt_fit




if __name__ == "__main__":
    board_size=8
    lst = range(0, board_size)

    draw_board(Individual(genome=random.sample(lst, k=board_size),fitness=0))    # 7 x 7 to test window size
    # draw_board(initialize_individual(genome=[9, 6, 0, 3, 10, 7, 2, 4, 12, 8, 11, 5, 1],fitness=0))  # 13 x 13
    # draw_board(initialize_individual(genome=[11, 4, 8, 12, 2, 7, 3, 15, 0, 14, 10, 6, 13, 1, 5, 9],fitness=0))