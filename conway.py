# Conway's Game of Life 

import time
import random
import displayio
from adafruit_matrixportal.matrix import Matrix

MATRIX_WIDTH=64
MATRIX_HEIGHT=32

# --- Drawing setup ---
matrix = Matrix()
display = matrix.display

# Create a Group
group = displayio.Group(max_size=22)

# Create a bitmap object
bitmap = displayio.Bitmap(MATRIX_WIDTH, MATRIX_HEIGHT, 2)

color = displayio.Palette(2)
color[0] = (0,0,0)
color[1] = (128,0,128)

group.append(displayio.TileGrid(bitmap, pixel_shader=color))
# ---------------------

patterns = {
    'Glider': [(8,28),(9,29),(7,30),(8,30),(9,30)],
    'RIP Conway': [(16,10),(16,11),(16,12),(17,10),(17,12),(18,10),(18,12),(19,11),(20,8),(20,10),(20,11),(20,12),(21,9),(21,11),(21,13),(22,11),(22,14),(23,10),(23,12),(24,10),(24,12)]
    'R-Pentomino': [(14,32),(14,33),(15,31),(15,32),(16,32)],
    "Gosper's Glider Gun": [(5,35),(6,33),(6,35),(7,23),(7,24),(7,31),(7,32),(7,45),(7,46),(8,22),(8,26),(8,31),(8,32),(8,45),(8,46),(9,11),(9,12),(9,21),(9,27),(9,31),(9,32),(10,11),(10,12),(10,21),(10,25),(10,27),(10,28),(10,33),(10,35),(11,21),(11,27),(11,35),(12,22),(12,26),(13,23),(13,24)],
    #'puffer train': [],
    'random': []
}

def get_blank_grid():
    return [[0]*MATRIX_WIDTH for i in range(0,MATRIX_HEIGHT)]

def get_starting_grid():
    grid = get_blank_grid()
    name,coords = random.choice(list(patterns.items()))
    if name is 'random':
      for row in range(0,MATRIX_HEIGHT):
        for col in range(0,MATRIX_WIDTH):
          grid[row][col] = random.randint(0,1)
    else:
        for c in coords:
            grid[c[0]][c[1]] = 1

    return grid

def live_cells(row, col, grid):
    neighbors = 0
    min_col = col - 1 if col > 0 else col
    if row > 0:
        neighbors += sum(grid[row-1][min_col:col+2])

    neighbors += sum(grid[row][min_col:col+2])
    neighbors -= grid[row][col] # remove the middle

    if row < MATRIX_HEIGHT - 1:
        neighbors += sum(grid[row+1][min_col:col+2])

    return neighbors
    

def next_population(g):
    # seems naive
    new_grid = get_blank_grid()
    for row in range(0,MATRIX_HEIGHT):
        for col in range(0,MATRIX_WIDTH):
            alive = bool(grid[row][col])
            new_grid[row][col] = int(
                (alive and live_cells(row, col, g) in [2,3]) or
                (not alive and live_cells(row, col, g) == 3))
    return new_grid

def display_grid(grid):
    # seems naive - better to only change the pixels that have changed
    global bitmap
    global display

    for row in range(0,MATRIX_HEIGHT):
        for col in range(0,MATRIX_WIDTH):
      	    bitmap[col,row] = grid[row][col]

    display.show(group)


#####################################################
# Start the hot Conway action!
#####################################################
grid = get_starting_grid()
prev_grid = grid        # detect equilibrium
prev_prev_grid = None   # detect simple cycle

starting = True
while True:
    # Check for button presses
    display_grid(grid)
    if starting:
        time.sleep(5)
        starting = False

    #time.sleep(30)
    prev_prev_grid = prev_grid
    prev_grid = grid
    grid = next_population(grid)
    if prev_prev_grid == grid:
        print("Cycle Reached")
    if prev_grid == grid:
        print("Equilibrium Reached")
        grid = get_starting_grid()
        starting = True
