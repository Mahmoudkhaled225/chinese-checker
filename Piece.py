class Piece():
    PLAYER1_COLOR = "O"
    PLAYER2_COLOR = "X"

    def __init__(self, color) -> None:
        self.color = color
        
    def __str__(self) :
        return self.get_color()
    
    def get_color(self) :
        return self.color
    
    def is_player2_piece(self) :

        return self.color == Piece.PLAYER2_COLOR
        
    def is_player1_piece(self) :
        return self.color == Piece.PLAYER1_COLOR
