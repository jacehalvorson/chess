WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
# fps we're running at
CLOCK_RATE = 10

# Pre-defined colors so we don't have to use RGB directly
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
RED = ( 255, 0, 0 )
GREEN = ( 0, 255, 0 )
BLUE = ( 0, 0, 255 )
CYAN = ( 0, 255, 255 )
YELLOW = ( 255, 255, 0 )
PURPLE = ( 255, 0, 255 )

BLOCKS_IN_ROW = 8
BLOCKS_IN_COL = BLOCKS_IN_ROW
# Total number of blocks on the board
NUM_BLOCKS = BLOCKS_IN_ROW * BLOCKS_IN_ROW
# Width of one block
BLOCK_SIZE = ( WINDOW_WIDTH / BLOCKS_IN_ROW )
BLOCK_0_COLOR = BLACK
BLOCK_1_COLOR = ( 140, 110, 30 )

# Standards for the piece representation
# Percentage of the block that a piece's radius fills
RELATIVE_CIRCLE_SIZE = (3/8)
# Resulting circle radius
POTENTIAL_MOVE = 5
POTENTIAL_MOVE_COLOR = CYAN
POTENTIAL_MOVE_RADIUS = BLOCK_SIZE * (1/8)

# Border customizations
POTENTIAL_MOVE_BORDER_COLOR = WHITE
# Width of the piece borders in pixels
BORDER_WIDTH = 2
POTENTIAL_MOVE_BORDER_WIDTH = 1
