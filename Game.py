from random import choice
from Board import Board
from Players import Player_Computer, Player_Person


def computerPlayer(board, name) :
    res = input("Choose difficulty 1:Easy 2:Medium 3:Difficult: ").strip().lower()
    if (res == 1):
         res = 2
    elif (res == 2):
         res = 4
    elif (res == 3):
         res = 9
    depth = int(res)

    player = Player_Computer(name, 1, depth)

    player.set_heuristic(get_heuristic(board, player.is_player1()) )

    return player


def createPlayer(board):
    player1, player2 = None, None

    # Player 1
    while player1 is None:
        player1 = Player_Person("Player1")

    print()

    # Player 2
    while player2 is None:
        player2 = computerPlayer(board, "Player2")

    return player1, player2

def get_heuristic(b, turn1):
    def h1(tile_origin, tile_destination) :
        if turn1:
            return board.get_row_index(tile_destination) >= board.get_row_index(tile_origin)
        else:
            return board.get_row_index(tile_destination) <= board.get_row_index(tile_origin)
    return h1

# -----------------------------------------------------------------------------------

if __name__ == "__main__":
    board = Board()
    players = createPlayer(board)

    playerIndex = choice([0, 1])
    print("\n----------------------------------------------------")
    print(f"{players[playerIndex].get_name()} starts\n")

    while not board.has_game_ended():
        player = players[playerIndex]
        tile_origin, tile_destination = player.get_move(board)
        board.move_piece_to_tile(tile_origin, tile_destination)
        board.print_board()
        playerIndex = (playerIndex + 1) % len(players)
    
    if board.has_player1_won():
        print("Player1 has won")
    else:
        print("Player2 has won")
