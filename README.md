# chinese-checker

special instructions:-

	Human play with		"O"
	computer play with	"X"

	Scenario of Game:-
		1)Player choose which marbel will be moved.
		2)Player choose which place marbel will be moved to.
		3)Player waiting for computer to play.
		4)Player will start again from step one.
---------------------------------------------------------------------
Description of Heuristic function:-
	This the function that will compare the different states of the players and
		Determine the validation of the next state,
	Heuristic function take 2 inputs(tile_origin, tile_destination) 
	*)Tile origin->current board
	*)Tile destination->board after one move in row 
	Check if tile destination of row greater than tile origin then tile origin will be tile destination (tile origin = tile destination) 
	By using MinMax && alpha Beta

important disclaimer
this was a team project and it was team of 5 including me

