import pygame
from ..models.board import Board
from ..utils.constants import (
    TITLE_HEIGHT, WINDOW_HEIGHT, WINDOW_WIDTH,
    PADDING, CELL_SIZE
)

class Game:
    def __init__(self):
        """Initialize the game"""
        self.board = Board(initialize_pygame=True)
        self.running = True

    def handle_mouse_button_down(self, event):
        """Handle mouse button down events"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Left click
        if event.button == 1:
            # Check for reset button click
            if self.board.reset_button_rect and self.board.reset_button_rect.collidepoint(mouse_x, mouse_y):
                self.board.reset_board()
                self.board.has_won = False
                self.board.scroll_offset = 0  # Reset scroll
                self.board.target_scroll = 0  # Reset scroll target
                return
            
            # Only allow piece selection if game isn't won
            if not self.board.has_won:
                # Try to select a piece from the selection area
                piece = self.board.get_piece_at_position(mouse_x, mouse_y)
                if piece:
                    self.board.selected_piece = piece
                    self.board.dragging = True
                    self.board.drag_pos = (mouse_x, mouse_y)
        
        # Right click (rotate piece)
        elif event.button == 3 and self.board.selected_piece:
            self.board.selected_piece.rotate()

    def handle_mouse_motion(self, event):
        """Handle mouse motion events"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Update reset button hover state
        if self.board.reset_button_rect:
            self.board.reset_hover = self.board.reset_button_rect.collidepoint(mouse_x, mouse_y)
        
        # Update dragged piece position
        if self.board.dragging:
            self.board.drag_pos = (mouse_x, mouse_y)

    def handle_mouse_button_up(self, event):
        """Handle mouse button up events"""
        if event.button == 1 and self.board.dragging and not self.board.has_won:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check if piece is being dropped on the board
            if TITLE_HEIGHT <= mouse_y < WINDOW_HEIGHT + TITLE_HEIGHT:
                adjusted_x = mouse_x - (self.board.selected_piece.width * CELL_SIZE) // 2
                adjusted_y = mouse_y - (self.board.selected_piece.height * CELL_SIZE) // 2
                
                # Place piece if position is valid
                if self.board.is_valid_position(self.board.selected_piece, adjusted_x, adjusted_y):
                    self.board.place_piece(self.board.selected_piece, adjusted_x, adjusted_y)
                    self.board.available_pieces.remove(self.board.selected_piece)
                    
                    # Adjust scroll position to show remaining pieces
                    total_width = sum((piece.width + 1) * CELL_SIZE for piece in self.board.available_pieces) - CELL_SIZE
                    max_scroll = max(0, total_width - WINDOW_WIDTH + 2 * PADDING)
                    self.board.target_scroll = min(self.board.scroll_offset, max_scroll)
                    
                    # Check for win after placing piece
                    if self.board.check_win():
                        self.board.has_won = True
            
            # Reset drag state
            self.board.dragging = False
            self.board.selected_piece = None

    def handle_mouse_wheel(self, event):
        """Handle mouse wheel events"""
        if not self.board.dragging and not self.board.has_won:
            if event.button == 4:  # Scroll up
                self.board.cycle_piece_forward()
            elif event.button == 5:  # Scroll down
                self.board.cycle_piece_backward()

    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1, 3):  # Left or right click
                        self.handle_mouse_button_down(event)
                    elif event.button in (4, 5):  # Mouse wheel up/down
                        self.handle_mouse_wheel(event)
                
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_button_up(event)
            
            # Update display
            self.board.display()
        
        # Clean up
        pygame.quit()
