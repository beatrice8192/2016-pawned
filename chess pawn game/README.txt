CMPT317 A2
Yuqing Tan (Beatrice) (yut630, 11119129)

README file on how to run the code

Code files:
	Pawn.py: containing the game class and all algorithms it needs (e.g. alphabeta pruning)
	runPawn.py: the automation program that uses Pawn.py to create the game flow

The command:
python runPawn.py <depth> [R|W|RW|B|RB|BW]
	depth: the depth limit for minimax tree
	R: AI vs. AI; randomize moves
	W|RW: human vs. AI; human plays white
	B|RB: human vs. AI; human plays black
	BW: human vs. human

when depth is 1-5, the program can get fairly decent speed (less than 1 second per move)
when depth is 6-8, the program is slower but still tolerable (3-30 seconds per move)

a move is 2 integers separated by a space
	1st integer: which pawn to move; pawns are numbered and printed on board
	2nd integer: where to move; 0 - forward, 1 - left diagonal, 2 - right diagonal

Some test outputs:
	test1_fixed.txt: AI always chooses the first optimal move, without randomizing
		(i.e. it gets the same result every time it runs)
	test2_draw: an example of draw when I played white
	test3_blackwin: an example of using strategy to win when I played black
	test4_whitewin: an example of I was beaten by AI when I played black
