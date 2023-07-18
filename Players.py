from Board import Board
from Tile import Tile

CHARACTERS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZ"

def askpiece(board, is_player1) :
    tiles_with_movable_pieces = list(filter(
        lambda t: any(board.get_all_valid_moves(t)), board.get_player1_tiles() if is_player1 else board.get_player2_tiles()
    ))
    board.print_board(tiles_with_movable_pieces, "".join(CHARACTERS))

    while True:
        n = input(f"Your turn...!\nChoose piece ({CHARACTERS[0]} - {CHARACTERS[len(tiles_with_movable_pieces)-1]})").strip().upper()
        if len(n) != 1:
            continue
        if n in CHARACTERS[ : len(tiles_with_movable_pieces)]:
            selected_tile = tiles_with_movable_pieces[CHARACTERS.index(n)]
            return selected_tile

def askDestination(board, tile_origin) :
    available_tile_destinations: list[Tile] = [tile for tile in board.get_all_valid_moves(tile_origin)]

    board.print_board(available_tile_destinations, CHARACTERS)

    while True:
        n = input(f"Select a tile to move to ({CHARACTERS[0]} - {CHARACTERS[len(available_tile_destinations)-1]})").strip().upper()
        if len(n) != 1:
            continue
        if n in CHARACTERS[ : len(available_tile_destinations)]:
            destination_tile = available_tile_destinations[ CHARACTERS.index(n) ]
            return destination_tile

def minimax(board, depth, is_player1_turn, heuristic, use_eval_func_1, maximizing = True, alpha = -1000000000, beta = 1000000000) :
    if depth==0 or board.has_game_ended():
        return board.get_score(is_player1_turn, use_eval_func_1)+depth, None, None
    if maximizing:
        max_points, better_origin, better_destination = float('-inf'), None, None
        for tile_origin in board.get_player1_tiles() if is_player1_turn else board.get_player2_tiles():
            for tile_destination in board.get_all_valid_logical_moves(tile_origin, heuristic):
                board.move_piece_to_tile(tile_origin, tile_destination)
                res_points, _1, _2 = minimax(board, depth - 1, is_player1_turn, heuristic, use_eval_func_1, not maximizing, alpha, beta)
                board.move_piece_to_tile(tile_destination, tile_origin)

                if res_points > max_points:
                    max_points, better_origin, better_destination = res_points, tile_origin, tile_destination
                alpha = max(alpha, res_points)
                if beta <= alpha:
                    break

            if beta <= alpha:
                break

        return max_points, better_origin, better_destination
    
    else:
        min_points, better_origin, better_destination = float('inf'), None, None
        for tile_origin in board.get_player2_tiles() if is_player1_turn else board.get_player1_tiles():
            for tile_destination in board.get_all_valid_logical_moves(tile_origin, heuristic):
                board.move_piece_to_tile(tile_origin, tile_destination)
                res_points, _1, _2 = minimax(board, depth - 1, is_player1_turn, heuristic, use_eval_func_1, not maximizing, alpha, beta)
                board.move_piece_to_tile(tile_destination, tile_origin)

                if res_points < min_points:
                    min_points, better_origin, better_destination = res_points, tile_origin, tile_destination
                beta = min(beta, res_points)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return min_points, better_origin, better_destination
class Player():
    def __init__(self, name) :
        self.name = name
    
    def get_name(self) :
        return self.name
    
    def is_player1(self) :
        return "1" in self.get_name()


class Player_Computer(Player):
    DEFAULT_HEURISTIC = lambda x, y: True
    def __init__(self, name, eval_func_int, depth) :
        super().__init__(name)
        self.eval_func = eval_func_int
        self.heuristic = Player_Computer.DEFAULT_HEURISTIC
        self.depth = depth
    
    def set_heuristic(self, f):
        self.heuristic = f

    def get_move(self, board: Board) :
        _, tile_origin, tile_destination = minimax(board, self.depth, self.is_player1(), self.get_heuristic(), self.uses_eval_func_1())
        return (tile_origin, tile_destination)

    def get_heuristic(self):
        return self.heuristic
    
    def get_eval_func(self) :
        return self.eval_func
    
    def uses_eval_func_1(self) :
        return self.eval_func == 1

class Player_Person(Player):
    def __init__(self, name) :
        super().__init__(name)

    def get_move(self, board) :
        tile_origin = askpiece(board, "1" in self.get_name())
        tile_destination = askDestination(board, tile_origin)
        return (tile_origin, tile_destination)
