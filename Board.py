from Tile import Tile
from Piece import Piece

class Board():
    def __init__(self) :

        self.board_row_tiles = self.generate_board_rows()
        self.board_tiles = self.rows_to_board()
        self.pieces = self.generate_pieces()
        self.add_neighbouring_tiles()
        self.place_pieces_in_board()
        self.calculate_tiles_scores()
    

    def generate_board_rows(self) :
        TILES_PER_ROW = [1, 2, 3, 4, 13, 12, 11, 10, 9, 10, 11, 12, 13, 4, 3, 2, 1]
        board_rows = []
        for i in range(len(TILES_PER_ROW)):
            board_rows.append([Tile() for _ in range(TILES_PER_ROW[i])])
        return board_rows
    
    def rows_to_board(self) :
        board = []
        for row in self.board_row_tiles:
            board.extend(row)
        return board

    def generate_pieces(self) :
        return [Piece(Piece.PLAYER1_COLOR) for _ in range(10)] + [Piece(Piece.PLAYER2_COLOR) for _ in range(10)]


    def add_neighbouring_tiles(self) :
        for row in self.board_row_tiles:
            for i in range(0, len(row)-1):
                row[i].add_neighbour("R", row[i+1])
            for i in range(1, len(row)):
                row[i].add_neighbour("L", row[i-1])


        for row_index in [0, 1, 2, 8, 9, 10, 11]:
            for tile_index in range(len(self.board_row_tiles[row_index])):
                self.board_row_tiles[row_index][tile_index].add_neighbour("DL", self.board_row_tiles[row_index+1][tile_index])
                self.board_row_tiles[row_index][tile_index].add_neighbour("DR", self.board_row_tiles[row_index+1][tile_index+1])
                self.board_row_tiles[row_index + 1][tile_index].add_neighbour("UR", self.board_row_tiles[row_index][tile_index])
                self.board_row_tiles[row_index + 1][tile_index + 1].add_neighbour("UL", self.board_row_tiles[row_index][tile_index])


        for row_index in [5, 6, 7, 8, 14, 15, 16]:
            for tile_index in range(len(self.board_row_tiles[row_index])):
                self.board_row_tiles[row_index][tile_index].add_neighbour("UL", self.board_row_tiles[row_index - 1][tile_index])
                self.board_row_tiles[row_index][tile_index].add_neighbour("UR", self.board_row_tiles[row_index - 1][tile_index+1])
                self.board_row_tiles[row_index - 1][tile_index].add_neighbour("DR", self.board_row_tiles[row_index][tile_index])
                self.board_row_tiles[row_index - 1][tile_index + 1].add_neighbour("DL", self.board_row_tiles[row_index][tile_index])


        for tile_index in range(len(self.board_row_tiles[3])):
            self.board_row_tiles[3][tile_index].add_neighbour("DL", self.board_row_tiles[4][tile_index + 4])
            self.board_row_tiles[3][tile_index].add_neighbour("DR", self.board_row_tiles[4][tile_index + 5])
            self.board_row_tiles[4][tile_index + 4].add_neighbour("UR", self.board_row_tiles[3][tile_index])
            self.board_row_tiles[4][tile_index + 5].add_neighbour("UL", self.board_row_tiles[3][tile_index])


        for tile_index in range(len(self.board_row_tiles[13])):
            self.board_row_tiles[13][tile_index].add_neighbour("UL", self.board_row_tiles[12][tile_index + 4])
            self.board_row_tiles[13][tile_index].add_neighbour("UR", self.board_row_tiles[12][tile_index + 5])
            self.board_row_tiles[12][tile_index + 4].add_neighbour("DR", self.board_row_tiles[13][tile_index])
            self.board_row_tiles[12][tile_index + 5].add_neighbour("DL", self.board_row_tiles[13][tile_index])

    def place_pieces_in_board(self) :
        i = 0
        for piece in self.get_player1_pieces():
            self.board_tiles[i].set_piece(piece)
            i += 1
        
        for piece in self.get_player2_pieces():
            self.board_tiles[-i].set_piece(piece)
            i -= 1

    def get_player1_tiles(self):
        return filter(lambda t: not t.is_empty()  and  t.get_piece().is_player1_piece(), self.board_tiles)

    def get_player2_tiles(self):
        return filter(lambda t: not t.is_empty()  and  t.get_piece().is_player2_piece(), self.board_tiles)
        
    def get_player1_pieces(self):
        return filter(lambda p: p.is_player1_piece(), self.pieces)

    def get_player2_pieces(self):
        return filter(lambda p: p.is_player2_piece(), self.pieces)

    def has_player1_reached_destination(self) :
        return all(not tile.is_empty() for tile in self.get_bottom_triangle_tiles())  and  any(tile.get_piece().is_player1_piece() for tile in self.get_bottom_triangle_tiles())

    def has_player2_reached_destination(self) :
        return all(not tile.is_empty() for tile in self.get_top_triangle_tiles())  and  any(tile.get_piece().is_player2_piece() for tile in self.get_top_triangle_tiles())

    def can_player1_move(self) :
        return any(filter(lambda t: any(self.get_all_valid_moves(t)), self.get_player1_tiles()))

    def can_player2_move(self)  :
        return any(filter(lambda t: any(self.get_all_valid_moves(t)), self.get_player2_tiles()))

    def has_player1_won(self) :
        return self.has_player1_reached_destination()

    def has_player2_won(self) :
        return self.has_player2_reached_destination()

    def has_game_ended(self) :
        return self.has_player2_won() or self.has_player1_won()

    def get_score(self, is_player1_turn, use_eval_func_1) :
        if (is_player1_turn  and  self.has_player1_won())  or  (not is_player1_turn  and  self.has_player2_won()):
            return 1000000
        if (is_player1_turn  and  self.has_player2_won())  or  (not is_player1_turn  and  self.has_player1_won()):
            return -1000000
         
        if use_eval_func_1:
            score_player_1 = sum(t.get_score1() for t in self.get_player1_tiles()) * (1 if is_player1_turn else -1)
            score_player_2 = sum(t.get_score1() for t in self.get_player2_tiles()) * (-1 if is_player1_turn else 1)
            return score_player_1 + score_player_2
        else:
            score_player_1 = sum(t.get_score2() for t in self.get_player1_tiles()) * (1 if is_player1_turn else -1)
            score_player_2 = sum(t.get_score2() for t in self.get_player2_tiles()) * (-1 if is_player1_turn else 1)
            return score_player_1 + score_player_2
    
    def get_all_possible_tiles_to_move(self, tile, only_jumps = False, already_jumped_from = None, already_returned = None):
        if already_jumped_from is None:
            already_jumped_from = set()
            already_returned = set()
        
        if tile not in already_jumped_from:
            already_jumped_from.add(tile)

            for (neighbour_direction, neighbour_tile) in tile.get_neighbours().items():
                if neighbour_tile.is_empty():
                    if not only_jumps:
                        yield neighbour_tile
                else:
                    neighbours_neighbour: Tile = neighbour_tile.get_neighbours().get(neighbour_direction, None)
                    if neighbours_neighbour is not None:
                        if neighbours_neighbour.is_empty():
                            if neighbours_neighbour not in already_returned:
                                yield neighbours_neighbour
                                already_returned.add(neighbours_neighbour)
                            for move in self.get_all_possible_tiles_to_move(neighbours_neighbour, True, already_jumped_from, already_returned):
                                yield move
                                already_returned.add(move)
    
    def get_top_triangle_tiles(self):
        return self.board_tiles[:10]

    def get_bottom_triangle_tiles(self):
        return self.board_tiles[-10:]
    
    def get_all_valid_moves(self, tile_origin):
        for move in self.get_all_possible_tiles_to_move(tile_origin):
            if tile_origin.get_piece().is_player2_piece()  and  tile_origin in self.get_top_triangle_tiles()  and   move not in self.get_top_triangle_tiles():
                continue
            elif tile_origin.get_piece().is_player1_piece()  and  tile_origin in self.get_bottom_triangle_tiles()  and  move not in self.get_bottom_triangle_tiles():
                continue
            else:
                yield move
    
    def get_all_valid_logical_moves(self, tile_origin, heuristic_function):
        for tile_destination in self.get_all_valid_moves(tile_origin):
            if heuristic_function(tile_origin, tile_destination):
                yield tile_destination

                                    
    def move_piece_to_tile(self, tile_origin, destination_tile: Tile) :
        if not destination_tile.is_empty():
            return False
        
        destination_tile.set_piece(tile_origin.get_piece())
        tile_origin.set_empty()

        return True

    def calculate_tiles_scores(self) :
        pending_of_exploring: list[Tile]

        pending_of_exploring = [self.board_tiles[-1]]
        pending_of_exploring[0].set_score1_for_player1(16)
        while any(pending_of_exploring):
            exploring_tile, pending_of_exploring = pending_of_exploring[0], pending_of_exploring[1:]
            pending_of_exploring.extend( [tile for tile in exploring_tile.get_neighbours().values() if tile.set_score1_for_player1(exploring_tile.get_score1_for_player1() - 1)] )
        for tile in self.get_bottom_triangle_tiles():
            tile.set_score1_for_player1(5 + tile.get_score1_for_player1())
        
        pending_of_exploring = [self.board_tiles[0]]
        pending_of_exploring[0].set_score1_for_player2(16)
        while any(pending_of_exploring):
            exploring_tile, pending_of_exploring = pending_of_exploring[0], pending_of_exploring[1:]
            pending_of_exploring.extend( [tile for tile in exploring_tile.get_neighbours().values() if tile.set_score1_for_player2(exploring_tile.get_score1_for_player2() - 1)] )
        for tile in self.get_top_triangle_tiles():
            tile.set_score1_for_player2(5 + tile.get_score1_for_player2())

        for i in range(len(self.board_row_tiles)):
            row = self.board_row_tiles[i]
            for j in range(len(row)):
                if len(row) % 2 == 0:
                    row[j].set_score2_for_player1(1*10 - abs(int((len(row)-1)/2 - j)))
                else:
                    row[j].set_score2_for_player1(i*10 - abs(len(row)//2 - j))
        for tile in self.get_bottom_triangle_tiles():
            tile.set_score2_for_player1(tile.get_score2_for_player1() + 50)
        for i in range(len(self.board_row_tiles)):
            row = self.board_row_tiles[i]
            for j in range(len(row)):
                if len(row) % 2 == 0:
                    row[j].set_score2_for_player2((16-i)*10 - abs(int((len(row)-1)/2 - j)))
                else:
                    row[j].set_score2_for_player2((16-i)*10 - abs(len(row)//2 - j))
        for tile in self.get_top_triangle_tiles():
            tile.set_score2_for_player2(tile.get_score2_for_player2() + 50)

    def print_board(self, numbered_tiles=None, characters="123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> None:
        print(self.to_string(numbered_tiles, characters))

    def to_string(self, numbered_tiles=None, characters="123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
        res = ""
        numbered_tiles = [] if numbered_tiles is None else list(numbered_tiles)
        max_length: int = max( (len(row) for row in self.board_row_tiles))

        res += "CURRENT BOARD:\n"
        for row in self.board_row_tiles:
            res += " "*(max_length-len(row))
            tile: Tile
            for tile in row:
                if tile in numbered_tiles:
                    res += f"{characters[numbered_tiles.index(tile)]} "
                else:
                    res += f"{str(tile)} "
            res += "\n"
        res += "\n"

        return res

    
    def get_row_index(self, tile) :
        for i in range(len(self.board_row_tiles)):
            if tile in self.board_row_tiles[i]:
                return i
    
    def get_tile(self, piece):
        return next(tile for tile in self.board_tiles if tile.get_piece() is piece)
