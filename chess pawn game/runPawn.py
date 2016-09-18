import sys
import re
import Pawn
import datetime

# parse arguments
args = sys.argv
if len(args)<2:
	print("You need depth as an argument!")
	sys.exit()

print("Welcome to Pawned!")
depth = int(args[1])
if depth<1:
	print("Invalid argument!")
	sys.exit()
player1 = ''
player2 = ''
ifrandom = False
if len(args)==2:
	print("AI vs. AI")
if len(args)>2:
	if args[2] == 'R':
		print("AI vs. AI")
		print("AI moves are randomized!")
		ifrandom = True
	elif args[2] == 'W' or args[2] == 'RW':
		print("Human vs. AI")
		print("You are the white pawns!")
		player1 = 'W'
		if args[2] == 'RW':
			print("AI moves are randomized!")
			ifrandom = True
	elif args[2] == 'B' or args[2] == 'RB':
		print("Human vs. AI")
		print("You are the black pawns!")
		player1 = 'B'
		if args[2] == 'RB':
			print("AI moves are randomized!")
			ifrandom = True
	elif args[2] == 'BW':
		print("Human vs. Human")
		player1 = 'W'
		player2 = 'B'
	else:
		print("Invalid argument!")
		sys.exit()

# initialize the game
player = 'W'
size = 6
p = Pawn.Pawned(None,size,player)
p.display()

"""
# debugging stuffs
# place your game state here if you need to debug!
state = [(2, 1), (3, 2), (-1, -1), (-1, -1), (4, 5), (2, 6), (3, 1), (4, 2), (-1, -1), (6, 4), (4, 4), (3, 6)]
state = [(2, 1), (2, 2), (3, 3), (3, 4), (2, 5), (1, 6), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (4, 6)]
state = [(3, 1), (-1, -1), (4, 2), (3, 4), (2, 5), (1, 6), (-1, -1), (5, 2), (5, 3), (4, 4), (4, 5), (5, 6)]
p = Pawn.Pawned(state,size,player)
p.display()
move = []
ifprint = True
nextState = p.optimalSuccMM(depth, ifprint, ifrandom, move)
nextState = p.optimalSuccAB(depth, ifprint, ifrandom, move)

"""

# game loop
k=1
ifprint = False
while not p.isTerminal():
	print("")
	print("Step #%d" % k)
	if p.whoseTurn == 'B':
		print("Black's turn")
	else:
		print("White's turn")
	
	move = []
	#nextState = p.optimalSuccMM(depth, ifprint, ifrandom, move)
	nextState = p.optimalSuccAB(depth, ifprint, ifrandom, move)
	if nextState is not None and (p.whoseTurn == player1 or p.whoseTurn == player2):
		nextState = None
		while nextState is None:
			input = raw_input()
			r = re.compile('[ \t\n\r:]+')
			input = r.split(input)
			if len(input)!=2:
				print("Invalid input!")
				continue
			nextState = p.move(p.whoseTurn, int(input[0])-1, int(input[1]))
			if nextState is None:
				print("Invalid input!")
	elif nextState is not None:
		print(move)
	
	nextplayer = p.switchPlayer()
	if nextState is not None:
		p = Pawn.Pawned(nextState,size,nextplayer)
	else:
		p = Pawn.Pawned(p.gameState,size,nextplayer)
	p.display()
	print(p.gameState)
	print(datetime.datetime.now().time())
	#print("Utility for black: %d" % p.utilityP('B', True))
	#print("Utility for white: %d" % p.utilityP('W', True))
	#print("Utility for the board: %d" % p.utility())
	k+=1
	if k > 50: #infinite loop happens
		break

if p.winner == 'B':
	print("Black pawned!")
elif p.winner == 'W':
	print("White pawned!")
else:
	print("Stalemate!")
#"""