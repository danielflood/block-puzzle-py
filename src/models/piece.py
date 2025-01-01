from ..utils.constants import PIECE_COLORS

class Piece:
    def __init__(self, shape=None, color=None):
        if shape is None:
            # Default shape (red S piece)
            self.shape = [
                [1, 1, 0],  # Top row
                [0, 1, 1]   # Bottom row
            ]
            self.color = PIECE_COLORS['RED_S']
        else:
            self.shape = shape
            self.color = color
            
        self.width = len(self.shape[0])
        self.height = len(self.shape)
    
    def rotate(self):
        # Create a new rotated shape (90 degrees clockwise)
        rotated = [[0 for _ in range(self.height)] for _ in range(self.width)]
        for row in range(self.height):
            for col in range(self.width):
                rotated[col][self.height - 1 - row] = self.shape[row][col]
        
        # Update shape and dimensions
        self.shape = rotated
        self.width, self.height = self.height, self.width

    @staticmethod
    def create_all_pieces():
        """Create all the initial game pieces"""
        return [
            Piece(shape=[[1, 1, 0],    # Red S piece
                        [0, 1, 1]],
                 color=PIECE_COLORS['RED_S']),
            Piece(shape=[[0, 1, 1],    # Green Z piece
                        [1, 1, 0]],
                 color=PIECE_COLORS['GREEN_Z']),
            Piece(shape=[[0, 1, 0],    # Purple T piece
                        [1, 1, 1]],
                 color=PIECE_COLORS['PURPLE_T']),
            Piece(shape=[[0, 0, 1],    # Orange L piece
                        [1, 1, 1]],
                 color=PIECE_COLORS['ORANGE_L']),
            Piece(shape=[[1, 1, 1],    # Dark blue reversed L piece
                        [0, 0, 1]],
                 color=PIECE_COLORS['BLUE_L']),
            Piece(shape=[[1, 1],       # Yellow square piece
                        [1, 1]],
                 color=PIECE_COLORS['YELLOW_SQUARE']),
            Piece(shape=[[1, 1, 1, 1]], # Light blue line piece
                 color=PIECE_COLORS['CYAN_LINE'])
        ]
