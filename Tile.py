from Piece import Piece

class Tile():
    VALID_DIRECTIONS: list[str] = ["L", "R", "UL", "UR", "DL", "DR"]
    EMPTY_TYLE_STR = "."
    DEFAULT_SCORE = -1

    def __init__(self) :
        self.piece = None
        self.neighbours: dict[str, Tile] = {}
        self.score1_for_player1 = Tile.DEFAULT_SCORE
        self.score1_for_player2 = Tile.DEFAULT_SCORE
        self.score2_for_player1 = Tile.DEFAULT_SCORE
        self.score2_for_player2 = Tile.DEFAULT_SCORE
    
    def __str__(self) :
        return Tile.EMPTY_TYLE_STR if self.is_empty() else str(self.get_piece())
    
    def set_piece(self, new_piece) :
        self.piece = new_piece
    
    def set_empty(self):
        self.set_piece(None)

    def set_score1_for_player1(self, new_score) :
        if self.score1_for_player1 == Tile.DEFAULT_SCORE  or  (new_score > self.score1_for_player1):
            self.score1_for_player1 = new_score
            return True
        return False

    def set_score1_for_player2(self, new_score) :
        if self.score1_for_player2 == Tile.DEFAULT_SCORE  or  (new_score > self.score1_for_player2):
            self.score1_for_player2 = new_score
            return True
        return False

    def set_score2_for_player1(self, new_score) :
        self.score2_for_player1 = new_score

    def set_score2_for_player2(self, new_score) :
        self.score2_for_player2 = new_score
    
    def get_score1_for_player1(self) :
        return self.score1_for_player1

    def get_score1_for_player2(self) :
        return self.score1_for_player2
    
    def get_score2_for_player1(self) :
        return self.score2_for_player1

    def get_score2_for_player2(self) :
        return self.score2_for_player2

    def get_score1(self) :
        if self.get_piece().is_player2_piece():
            return self.get_score1_for_player2()
        else:
            return self.get_score1_for_player1()
        
    def get_score2(self) :
        if self.get_piece().is_player2_piece():
            return self.get_score2_for_player2()
        else:
            return self.get_score2_for_player1()
    
    def add_neighbour(self, direction, neighbour_tile) :
        self.neighbours[direction] = neighbour_tile

    def get_neighbours(self) :
        return self.neighbours

    def get_piece(self) :
        return self.piece
    
    def is_empty(self) :
        return self.get_piece() is None
