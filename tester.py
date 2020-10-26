# ON AIR sign for YouTube livestreaming
# Runs on Airlift Metro M4 with 64x32 RGB Matrix display & shield
 
import time
import random
import board
import displayio
import adafruit_display_text.label
from adafruit_matrixportal.matrix import Matrix

MATRIX_WIDTH=64
MATRIX_HEIGHT=32
COLORS=128

def gen_random(bitmap):
  #print("Generating bitmap")
  for row in range(0,MATRIX_WIDTH):
    for col in range(0,MATRIX_HEIGHT):
      bitmap[row,col] = random.randint(1,COLORS-1)

def gen_grid(bitmap,i):
  for col in range(0,MATRIX_WIDTH):
    for row in range(0,MATRIX_HEIGHT):
      if col % 7 == i % 7 or row % 4 == i % 4:
  	gridcolor = random.randint(1,COLORS-1)
      	bitmap[col,row] = gridcolor
      else:
      	bitmap[col,row] = 0


def gen_map(bitmap, i):
  #gen_random(bitmap)
  gen_grid(bitmap, i)

# Create a color palette
def gen_palette():
  color = displayio.Palette(COLORS)
  color[0] = (0,0,0)
  for i in range(1,COLORS):
    color[i] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

  return color

# --- Display setup ---
matrix = Matrix()
display = matrix.display

# --- Drawing setup ---
# Create a Group
group = displayio.Group(max_size=22)
# Create a bitmap object
bitmap = displayio.Bitmap(MATRIX_WIDTH, MATRIX_HEIGHT, COLORS)

gen_map(bitmap, 0)
color = gen_palette()

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=color)
# Add the TileGrid to the Group
group.append(tile_grid)
 
i=0
while True:
  gen_map(bitmap, i)
  display.show(group)
  i = (i + 1) % 28 # (7 * 4), really to keep i from overflowing
