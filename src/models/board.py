import pygame
from .piece import Piece
from ..utils.constants import (
    CELL_SIZE, GRID_COLOR, BG_COLOR, EMPTY_COLOR,
    SELECTION_HEIGHT, TITLE_HEIGHT, PADDING, BOTTOM_PADDING,
    BUTTON_PADDING, BUTTON_RADIUS, BUTTON_COLOR, BUTTON_HOVER_COLOR,
    WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT
)

class Board:
    def __init__(self, initialize_pygame=True):
        # Non-pygame dependent initialization
        self.dragging = False
        self.selected_piece = None
        self.drag_pos = None
        self.has_won = False
        self.reset_button_rect = None
        self.reset_hover = False
        
        # Initial pieces list (store for reset)
        self.initial_pieces = Piece.create_all_pieces()
        
        # Reset the board to initial state
        self.reset_board()
        
        if initialize_pygame:
            # Initialize Pygame
            pygame.init()
            
            # Initialize display
            self.screen = pygame.display.set_mode(
                (WINDOW_WIDTH, WINDOW_HEIGHT + SELECTION_HEIGHT + TITLE_HEIGHT)
            )
            pygame.display.set_caption("Tetris Puzzle")
            
            # Initialize fonts
            self.title_font = pygame.font.Font(None, 60)
            self.button_font = pygame.font.Font(None, 36)
            self.win_font = pygame.font.Font(None, 74)

        # Add scroll variables
        self.scroll_offset = 0
        self.target_scroll = 0
        self.scroll_speed = 15  # Pixels per frame
        self.max_scroll = 0

    def reset_board(self):
        """Reset the board to its initial state"""
        # Reset grid
        self.grid = [
            [None, 0, 0, 0, None],    # Top row with corners missing
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]           # Now 6 rows
        ]
        # Reset available pieces
        self.available_pieces = Piece.create_all_pieces()
        self.dragging = False
        self.selected_piece = None
        self.has_won = False

    def is_valid_position(self, piece, start_x, start_y):
        """Check if a piece can be placed at the given position"""
        # Convert pixel coordinates to grid coordinates
        grid_x = (start_x - PADDING) // CELL_SIZE
        grid_y = (start_y - TITLE_HEIGHT) // CELL_SIZE
        
        # Check each cell of the piece
        for row in range(piece.height):
            for col in range(piece.width):
                if piece.shape[row][col]:
                    board_row = grid_y + row
                    board_col = grid_x + col
                    
                    # Check bounds
                    if (board_row < 0 or board_row >= BOARD_HEIGHT or
                        board_col < 0 or board_col >= BOARD_WIDTH or
                        self.grid[board_row][board_col] is None or
                        self.grid[board_row][board_col] != 0):
                        return False
        return True

    def place_piece(self, piece, x, y):
        """Place a piece on the board at the given position"""
        grid_x = (x - PADDING) // CELL_SIZE
        grid_y = (y - TITLE_HEIGHT) // CELL_SIZE
        
        # Place each cell of the piece
        for row in range(piece.height):
            for col in range(piece.width):
                if piece.shape[row][col]:
                    self.grid[grid_y + row][grid_x + col] = piece.color

    def get_piece_at_position(self, x, y):
        """Get the piece at the given selection area position"""
        if y < WINDOW_HEIGHT + TITLE_HEIGHT:  # Check if click is above selection area
            return None
            
        # Calculate total width of all pieces
        total_pieces_width = sum((piece.width + 1) * CELL_SIZE for piece in self.available_pieces) - CELL_SIZE
        
        # Calculate piece positions with scroll offset
        piece_x = PADDING - self.scroll_offset
        
        # Check each piece's bounds
        for piece in self.available_pieces:
            piece_width = piece.width * CELL_SIZE
            piece_height = piece.height * CELL_SIZE
            
            # Define piece bounds in selection area
            piece_bounds = pygame.Rect(
                piece_x,
                WINDOW_HEIGHT + TITLE_HEIGHT + 20,
                piece_width,
                piece_height
            )
            
            # Check if click is within piece bounds
            if piece_bounds.collidepoint(x, y):
                return piece
                
            piece_x += (piece.width + 1) * CELL_SIZE
        
        return None

    def display(self):
        """Draw the game state"""
        # Fill background
        self.screen.fill(BG_COLOR)
        
        # Draw title
        title_surface = self.title_font.render("TETRIS", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, TITLE_HEIGHT // 2))
        self.screen.blit(title_surface, title_rect)
        
        # Draw reset button
        button_surface = self.button_font.render("Reset", True, (255, 255, 255))
        button_text_rect = button_surface.get_rect()
        
        # Create button rectangle with padding
        self.reset_button_rect = pygame.Rect(
            WINDOW_WIDTH - button_text_rect.width - BUTTON_PADDING * 3,
            BUTTON_PADDING,
            button_text_rect.width + BUTTON_PADDING * 2,
            button_text_rect.height + BUTTON_PADDING
        )
        
        # Draw button with hover effect
        button_color = BUTTON_HOVER_COLOR if self.reset_hover else BUTTON_COLOR
        pygame.draw.rect(self.screen, button_color, self.reset_button_rect, border_radius=BUTTON_RADIUS)
        
        # Center text on button
        button_text_rect.center = self.reset_button_rect.center
        self.screen.blit(button_surface, button_text_rect)
        
        # Draw board grid
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                x = col * CELL_SIZE + PADDING
                y = row * CELL_SIZE + TITLE_HEIGHT
                
                if self.grid[row][col] is not None:
                    # Draw cell
                    color = self.grid[row][col] if self.grid[row][col] != 0 else EMPTY_COLOR
                    pygame.draw.rect(self.screen, color,
                                  (x, y, CELL_SIZE, CELL_SIZE))
                    # Draw cell border
                    pygame.draw.rect(self.screen, GRID_COLOR,
                                  (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw selection area
        pygame.draw.rect(self.screen, (40, 40, 40),
                        pygame.Rect(0, WINDOW_HEIGHT + TITLE_HEIGHT,
                                  WINDOW_WIDTH, SELECTION_HEIGHT))
        pygame.draw.line(self.screen, GRID_COLOR,
                        (0, WINDOW_HEIGHT + TITLE_HEIGHT),
                        (WINDOW_WIDTH, WINDOW_HEIGHT + TITLE_HEIGHT), 2)
        
        # Calculate total width of all pieces
        total_pieces_width = sum((piece.width + 1) * CELL_SIZE for piece in self.available_pieces) - CELL_SIZE
        
        # Create clipping rect for selection area (now using full width)
        selection_rect = pygame.Rect(0, WINDOW_HEIGHT + TITLE_HEIGHT,
                                   WINDOW_WIDTH, SELECTION_HEIGHT)
        self.screen.set_clip(selection_rect)
        
        # Draw available pieces in selection area with scroll offset
        piece_x = PADDING - self.scroll_offset
        
        for piece in self.available_pieces:
            if piece == self.selected_piece and self.dragging:
                piece_x += (piece.width + 1) * CELL_SIZE
                continue
            
            for row in range(piece.height):
                for col in range(piece.width):
                    if piece.shape[row][col]:
                        x = piece_x + col * CELL_SIZE
                        y = WINDOW_HEIGHT + TITLE_HEIGHT + 20 + row * CELL_SIZE
                        
                        # Only draw if within the window
                        if 0 <= x < WINDOW_WIDTH:
                            pygame.draw.rect(self.screen, piece.color,
                                          (x, y, CELL_SIZE, CELL_SIZE))
                            pygame.draw.rect(self.screen, GRID_COLOR,
                                          (x, y, CELL_SIZE, CELL_SIZE), 1)
            
            piece_x += (piece.width + 1) * CELL_SIZE
        
        # Reset clipping
        self.screen.set_clip(None)
        
        # Update scroll position
        self.update_scroll()
        
        # Draw dragged piece
        if self.dragging and self.selected_piece and self.drag_pos:
            self._draw_dragged_piece()
        
        # Draw win message if game is won
        if self.has_won:
            self._draw_win_message()
        
        pygame.display.flip()

    def _draw_piece_in_selection(self, piece, x_pos):
        """Draw a piece in the selection area"""
        piece_width = piece.width * CELL_SIZE
        piece_height = piece.height * CELL_SIZE
        start_x = x_pos - piece_width // 2
        start_y = WINDOW_HEIGHT + TITLE_HEIGHT + (SELECTION_HEIGHT - piece_height) // 2
        
        for row in range(piece.height):
            for col in range(piece.width):
                if piece.shape[row][col]:
                    pygame.draw.rect(self.screen, piece.color,
                                  (start_x + col * CELL_SIZE,
                                   start_y + row * CELL_SIZE,
                                   CELL_SIZE, CELL_SIZE))

    def _draw_dragged_piece(self):
        """Draw the piece being dragged"""
        mouse_x, mouse_y = self.drag_pos
        piece_width = self.selected_piece.width * CELL_SIZE
        piece_height = self.selected_piece.height * CELL_SIZE
        start_x = mouse_x - piece_width // 2
        start_y = mouse_y - piece_height // 2
        
        # Define board boundaries
        board_left = PADDING
        board_right = PADDING + BOARD_WIDTH * CELL_SIZE
        board_top = TITLE_HEIGHT
        board_bottom = TITLE_HEIGHT + BOARD_HEIGHT * CELL_SIZE
        
        # Check if mouse is within board boundaries
        is_over_board = (board_left <= mouse_x <= board_right and 
                        board_top <= mouse_y <= board_bottom)
        
        # Draw the actual dragged piece with transparency
        surface = pygame.Surface((piece_width, piece_height), pygame.SRCALPHA)
        for row in range(self.selected_piece.height):
            for col in range(self.selected_piece.width):
                if self.selected_piece.shape[row][col]:
                    color = (*self.selected_piece.color, 128)  # Semi-transparent
                    pygame.draw.rect(surface, color,
                                  (col * CELL_SIZE,
                                   row * CELL_SIZE,
                                   CELL_SIZE, CELL_SIZE))
        self.screen.blit(surface, (start_x, start_y))
        
        # Draw preview on board only if over the board
        if is_over_board:
            grid_x = (start_x - PADDING) // CELL_SIZE
            grid_y = (start_y - TITLE_HEIGHT) // CELL_SIZE
            
            # Check if position is valid
            is_valid = self.is_valid_position(self.selected_piece, start_x, start_y)
            
            # Draw preview outline
            preview_color = (0, 255, 0) if is_valid else (255, 0, 0)
            for row in range(self.selected_piece.height):
                for col in range(self.selected_piece.width):
                    if self.selected_piece.shape[row][col]:
                        x = (grid_x + col) * CELL_SIZE + PADDING
                        y = (grid_y + row) * CELL_SIZE + TITLE_HEIGHT
                        # Only draw preview if the cell would be on the board
                        if (PADDING <= x < board_right and 
                            TITLE_HEIGHT <= y < board_bottom):
                            pygame.draw.rect(self.screen, preview_color,
                                          (x, y, CELL_SIZE, CELL_SIZE), 2)

    def _draw_win_message(self):
        """Draw the win message overlay"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + SELECTION_HEIGHT + TITLE_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw win message
        win_text = self.win_font.render("Puzzle Complete!", True, (255, 255, 255))
        win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT + TITLE_HEIGHT) // 2))
        self.screen.blit(win_text, win_rect)

    def check_win(self):
        """Check if the puzzle is complete"""
        # Check if all pieces have been placed
        if not self.available_pieces:
            # Check if all grid spaces are filled
            for row in range(len(self.grid)):
                for col in range(len(self.grid[0])):
                    cell = self.grid[row][col]
                    # Only check cells that should be filled (not None)
                    if cell is not None and cell == 0:
                        return False
            return True
        return False

    def cycle_piece_forward(self):
        """Scroll pieces to the right"""
        if len(self.available_pieces) > 1:
            total_width = sum((piece.width + 1) * CELL_SIZE for piece in self.available_pieces) - CELL_SIZE
            max_scroll = max(0, total_width - WINDOW_WIDTH + 2 * PADDING)
            
            if self.target_scroll < max_scroll:
                self.target_scroll = min(self.target_scroll + CELL_SIZE * 2, max_scroll)
                self.max_scroll = max_scroll

    def cycle_piece_backward(self):
        """Scroll pieces to the left"""
        if len(self.available_pieces) > 1:
            if self.target_scroll > 0:
                self.target_scroll = max(self.target_scroll - CELL_SIZE * 2, 0)

    def update_scroll(self):
        """Update scroll position with smooth transition"""
        if self.scroll_offset < self.target_scroll:
            self.scroll_offset = min(self.scroll_offset + self.scroll_speed, self.target_scroll)
        elif self.scroll_offset > self.target_scroll:
            self.scroll_offset = max(self.scroll_offset - self.scroll_speed, self.target_scroll)
