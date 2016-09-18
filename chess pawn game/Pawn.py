import random

######
# Section1: pure MiniMax and MiniMax with AlphaBeta pruning

def getV(u, w, ifrandom):
	v = -1
	vlist = []
	for i in range(0, len(w)):
		if w[i] == u:
			vlist.append(i)
	if len(vlist) > 0:
		if ifrandom:
			rand = int(random.random()*len(vlist))
			v = vlist[rand]
		else:
			v = vlist[0]
	return v

def minimax(node, ifrandom):
	# pure minimax without alphabeta pruning
	# param:
	#	node: a game instance
	#	ifrandom: return a random or the first index value of its children
	# return: a minimax tree of 4-tuple at each node
	#	(minimaxValue, index, childValue[], children[])
	v = -1
	w = []
	x = []
	if node.isTerminal():
		u = node.utility()
		return MinimaxTree(u,v,w,x)
	#else:
	x = [minimax(c, ifrandom) for c in node.successors()]
	for i in range(0, len(x)):
		w.append(x[i].mmValue)
	if node.isMaxNode():
		u = max(w)
	elif node.isMinNode():
		u = min(w)
	else:
		return None
	v = getV(u, w, ifrandom)
	return MinimaxTree(u,v,w,x)

def alphabeta(node, alpha, beta, depth, origdepth, ifrandom):
	# minimax algorithm with alphabeta pruning
	# param:
	#	node: a game instance
	#	alpha: low bound
	#	beta: high bound
	#	depth: limit
	#	ifrandom: return a random or the first index value of its children
	# return: a minimax tree of 4-tuple at each node
	#	(minimaxValue, index, childValue[], children[])
	v = -1
	w = []
	x = []
	if depth == 0:
		u = node.utility()
	elif node.checkmate():
		if node.utility()>0:
			u = node.utility() - (origdepth-depth)
		else:
			u = node.utility() + (origdepth-depth)
	elif node.isTerminal():
		if node.utility()>0:
			u = node.utility() - (origdepth-depth)*node.boardSize
		else:
			u = node.utility() + (origdepth-depth)*node.boardSize
	elif node.isMaxNode():
		u = -1000
		for child in node.successors():
			newNode = Pawned(child, node.boardSize, node.switchPlayer())
			abtree = alphabeta(newNode, alpha, beta, depth-1, origdepth, ifrandom)
			x.append(abtree)
			w.append(abtree.mmValue)
			u = max(u, abtree.mmValue)
			alpha = max(alpha, u)
			if beta <= alpha:
				break
	elif node.isMinNode():
		u = 1000
		for child in node.successors():
			newNode = Pawned(child, node.boardSize, node.switchPlayer())
			abtree = alphabeta(newNode, alpha, beta, depth-1, origdepth, ifrandom)
			x.append(abtree)
			w.append(abtree.mmValue)
			u = min(u, abtree.mmValue)
			beta = min(beta, u)
			if beta <= alpha:
				break
	else:
		return None
	#v = getV(u, w, ifrandom)
	return MinimaxTree(u,v,w,x)

# End of Section1
######

class Pawned:

	######
	# Section2: basic definitions of a game object
	
	def __init__(self, state, size, player):
		# size will be 6 for this assignment
		self.boardSize = size
		self.whoseTurn = player
		self.winner = None
		if state is None:
			# gameState is a list of pawn positions (tuples) of both sides
			# black pawns: 0 to boardSize-1
			# white pawns: boardSize to boardSize*2-1
			# positive tuple means on board
			# negative tuple means knocked off
			self.gameState = []
			for c in range(1,self.boardSize+1):
				self.gameState.append((1,c))
			for c in range(1,self.boardSize+1):
				self.gameState.append((self.boardSize,c))
		else:
			self.gameState = state

	def isTerminal(self):
		# checks win or draw
		Bcount = 0
		Wcount = 0
		for i in range(0,self.boardSize):
			if self.gameState[i][0]!=-1:
				Bcount+=1
			if self.gameState[i][0]==self.boardSize:
				self.winner = 'B'
				return True
		for i in range(self.boardSize,self.boardSize*2):
			if self.gameState[i][0]!=-1:
				Wcount+=1
			if self.gameState[i][0]==1:
				self.winner = 'W'
				return True
		moves = []
		if len(self.successorsP(self.whoseTurn,moves))==0 and len(self.successorsP(self.switchPlayer(),moves))==0:
			if Bcount>Wcount:
				self.winner = 'B'
			elif Bcount<Wcount:
				self.winner = 'W'
			else:
				self.winner = None
			return True
		return False

	def isMaxNode(self):
		if self.whoseTurn == 'B':
			return True
		else:
			return False

	def isMinNode(self):
		if self.whoseTurn == 'W':
			return True
		else:
			return False

	def switchPlayerP(self, player):
		if player == 'B':
			return 'W'
		else:
			return 'B'

	def switchPlayer(self):
		return self.switchPlayerP(self.whoseTurn)

	def direction(self, player):
		if player == 'B':
			return 1
		else:
			return -1

	def range(self, player):
		if player == 'B':
			return (0, self.boardSize)
		else:
			return (self.boardSize, self.boardSize*2)

	# End of Section2
	######

	######
	# Section3: heuristic evaluation (game utility)

	def safeAppend(self, list, tuple):
		if tuple[0] < 1 or tuple[1] < 1 or tuple[0] > self.boardSize or tuple[1] > self.boardSize:
			return
		i = len(list)-1
		while (i > -1):
			if list[i][0]==tuple[0] and list[i][1]==tuple[1]:
				return
			i-=1
		list.append(tuple)
		return

	def safeRemove(self, list, tuple):
		if tuple[0] < 1 or tuple[1] < 1 or tuple[0] > self.boardSize or tuple[1] > self.boardSize:
			return
		for i in range(0, len(list)):
			if list[i][0]==tuple[0] and list[i][1]==tuple[1]:
				list.remove(tuple)
				return
		return

	def utilityP(self, player, ifprint):
		# heuristic evaluation for a player
		# home row: 1 for black, boardSize for white
		homeRow = self.range(player)[0] * (self.boardSize-1) / self.boardSize + 1
		oppoRow = self.boardSize+1-homeRow
		homeRangeL = self.range(player)[0]
		homeRangeH = self.range(player)[1]
		oppoRangeL = self.range(self.switchPlayerP(player))[0]
		oppoRangeH = self.range(self.switchPlayerP(player))[1]

		# number of pieces on the board (they weigh the same since they are all pawns)
		# sum of steps of all pieces away from home row
		# sum of controlled squares (not as useful as in chess)
		# non blocking bonus (nothing blocks it to reach the opposite home row)
		pieceCount = 0
		sumStep = 0
		controled = []
		nonBlockBonus = 0
		for i in range(homeRangeL, homeRangeH):
			if self.gameState[i][0] > 0:
				pieceCount+=1
				sumStep+=abs(self.gameState[i][0]-homeRow)

		"""
				# adding controlled squares
				if self.gameState[i][1] == 1:
					self.safeAppend(controled, ( self.gameState[i][0]+self.direction(player), self.gameState[i][1]+1 ))
				elif self.gameState[i][1] == self.boardSize:
					self.safeAppend(controled, ( self.gameState[i][0]+self.direction(player), self.gameState[i][1]-1 ))
				else:
					self.safeAppend(controled, ( self.gameState[i][0]+self.direction(player), self.gameState[i][1]-1 ))
					self.safeAppend(controled, ( self.gameState[i][0]+self.direction(player), self.gameState[i][1]+1 ))

		# removing useless controlled squares
		for i in range(homeRangeL, homeRangeH):
			if self.gameState[i][0] > 0:
				j = self.gameState[i][0]-self.direction(player)
				while abs(homeRow-j) > 0 and j >=1 and j <= self.boardSize:
					self.safeRemove(controled, (j, self.gameState[i][1]))
					j-=self.direction(player)
		for i in range(oppoRangeL, oppoRangeH):
			if self.gameState[i][0] > 0:
				j = self.gameState[i][0]+self.direction(player)
				while abs(oppoRow-j) > 0 and j >=1 and j <= self.boardSize:
					self.safeRemove(controled, (j, self.gameState[i][1]))
					j+=self.direction(player)
		controled = sorted(controled)
		#print(controled)
		sumControl = len(controled)
		"""
		
		move = []
		numSucc = len(self.successorsP(player, move))
		if ifprint:
			print("%d * 2 + %d + %d" % (pieceCount, sumStep, numSucc))
		return pieceCount*2 + sumStep + numSucc
		#return pieceCount + sumStep + sumControl + nonBlockBonus

	def utility(self):
		# utility for the board, black is max, white is min
		if self.isTerminal():
			if self.winner == 'B':
				return self.boardSize**3
			elif self.winner == 'W':
				return -self.boardSize**3
			else:
				return 0
		elif self.checkmate():
			cmB = self.checkmateP('B')[1]
			cmW = self.checkmateP('W')[1]
			if cmB < cmW:
				return self.boardSize**2 - cmB
			elif cmB > cmW:
				return -self.boardSize**2 + cmW
			else:
				return self.utilityP('B', False) - self.utilityP('W', False)
		else:
			return self.utilityP('B', False) - self.utilityP('W', False)

	def nonBlockCheck(self, i, player):
		# if anything blocks in the front
		j = 0
		while j < self.boardSize*2:
			if ( (self.gameState[j][0]-self.gameState[i][0])/self.direction(player)>0 and 
				self.gameState[j][1]==self.gameState[i][1] ):
				return -2
			j+=1
		return -1
		
	def diagonalCheck(self, i, player):
		# if anything blocks in the diagonal
		oppoRangeL = self.range(self.switchPlayerP(player))[0]
		oppoRangeH = self.range(self.switchPlayerP(player))[1]
		k = oppoRangeL
		while k < oppoRangeH:
			if abs(self.gameState[k][1]-self.gameState[i][1])==1:
				dist = (self.gameState[k][0]-self.gameState[i][0])/self.direction(player)
				if dist==1:
					return k
				elif dist>1:
					return -2
			k+=1
		return -1
		
	def checkmateP(self, player):
		# decide if a player is about to win
		# return: a triple (pawnIndex, pawnDistance, type)
		#	type 1 - nothing blocks front and diagonal
		#	type 2 - something blocks the diagonal
		homeRow = self.range(player)[0] * (self.boardSize-1) / self.boardSize + 1
		oppoRow = self.boardSize+1-homeRow
		homeRangeL = self.range(player)[0]
		homeRangeH = self.range(player)[1]
		minI = -1
		minDist = self.boardSize
		type = -1
		for i in range(homeRangeL, homeRangeH):
			if self.gameState[i][0] > 0:
				diagonal = self.diagonalCheck(i,player)
				nonBlock = self.nonBlockCheck(i,player)
				if ( ((nonBlock==-1 and diagonal==-1) or
					(diagonal>-1 and self.nonBlockCheck(diagonal,player)==-1 and self.diagonalCheck(diagonal,player)==-1)) and
					(abs(oppoRow - self.gameState[i][0]) < minDist) ):
					minI = i
					minDist = abs(oppoRow - self.gameState[i][0])
					if nonBlock==-1 and diagonal==-1:
						type = 1
					else:
						type = 2

		if minI>=self.boardSize:
			minI-=self.boardSize
		return (minI,minDist,type)

	def checkmate(self):
		# alphabeta pruning won't work after the game enters checkmate state
		# type 1 checkmate can bring the game to checkmate state
		# type 2 checkmate only works when the player that checks is the one that has the turn
		if ( (self.checkmateP('B')[2]==1 and self.checkmateP('B')[0]!=-1) or
			(self.checkmateP('W')[2]==1 and self.checkmateP('W')[0]!=-1) ):
			return True
		elif self.checkmateP(self.whoseTurn)[2]==2:
			return True
		else:
			return False

	# End of Section3
	######

	######
	# Section4: possible moves and successors (game states)

	def dupState(self):
		newGS = []
		for i in range(0,len(self.gameState)):
			newGS.append(self.gameState[i])
		return newGS

	def move(self,who,which,where):
		# move a pawn on the board
		# params:
		#	who: the player
		#	which[0,5]: which pawn to move
		#	where[0,2]: where to move the pawn
		#		0 - move forward
		#		1 - attack left diagonal
		#		2 - attack right diagonal
		# return: None if the move is invalid; otherwise a new game state
		oppoStart = self.range( self.switchPlayerP(who) )[0]
		oppoEnd = self.range( self.switchPlayerP(who) )[1]
		offset = which+self.range(who)[0]
		newGS = self.dupState()
		if offset<0 or offset>=self.boardSize*2:
			return None
		curPos = newGS[offset]
		nextPos = (-1,-1)

		if where == 0:
			nextPos = (curPos[0]+self.direction(who),curPos[1])
		elif where == 1:
			nextPos = (curPos[0]+self.direction(who),curPos[1]-1)
		elif where == 2:
			nextPos = (curPos[0]+self.direction(who),curPos[1]+1)
		else:
			return None

		if curPos[0] == -1:
			#already knocked out
			return None
		if nextPos[0] < 1 or nextPos[0] > self.boardSize or nextPos[1] < 1 or nextPos[1] > self.boardSize:
			#out of bound
			return None
		if where == 0:
			for i in range(0,self.boardSize*2):
				if self.gameState[i][0] == nextPos[0] and self.gameState[i][1] == nextPos[1]:
					#front blocked
					return None
		if where == 1 or where == 2:
			i = oppoStart
			while i < oppoEnd:
				if self.gameState[i][0] == nextPos[0] and self.gameState[i][1] == nextPos[1]:
					newGS[i] = (-1,-1)
					break
				i+=1
			if i == oppoEnd:
				#nothing to attack
				return None

		# if all of the above passed, then it's a valid move
		newGS[offset] = nextPos
		return newGS

	def successorsP(self, player, moves):
		# return: all possible moves (game states) for a player
		succ = []
		for which in range(0,self.boardSize):
			for where in range(0,3):
				newstate = self.move(player,which,where)
				if newstate is not None:
					succ.append(newstate)
					moves.append((which,where))
		return succ

	def successors(self):
		moves = []
		return self.successorsP(self.whoseTurn, moves)

	# End of Section4
	######

	######
	# Section5: generate optimal move

	def generateWholeTree(self, depth, origdepth):
		# return: a whole game tree with limited depth in GameTree structure
		if self.whoseTurn == 'B':
			player = 'MAX'
		else:
			player = 'MIN'

		if depth == 0:
			return GameTree(self.utility(),self.gameState,'TER')
		elif self.isTerminal():
			if self.utility()>0:
				u = self.utility() - (origdepth-depth)*self.boardSize
			else:
				u = self.utility() + (origdepth-depth)*self.boardSize
			return GameTree(u,self.gameState,'TER')
		elif len(self.successors())==0:
			return GameTree(self.utility(),self.gameState,'TER')
		else:
			succ = self.successors()
			treesucc = []
			for i in range(0,len(succ)):
				gs = Pawned(succ[i],self.boardSize,self.switchPlayer())
				b = gs.generateWholeTree(depth-1, origdepth)
				treesucc.append(b)
			return GameTree(treesucc,self.gameState,player)

	def printWholeTree(self, tree, depth):
		# print out a whole game tree in GameTree structure
		if isinstance(tree.gameUtil, int):
			return
		s = ''
		for j in range(0,depth):
			s += '  '
		s += str(tree.player) + ' '
		if not isinstance(tree.gameUtil[0].gameUtil, int):
			print(s)
		for i in range(0,len(tree.gameUtil)):
			if isinstance(tree.gameUtil[i].gameUtil, int):
				s += str(tree.gameUtil[i].gameUtil) + ' '
			else:
				self.printWholeTree(tree.gameUtil[i], depth+1)
		if isinstance(tree.gameUtil[0].gameUtil, int):
			print(s)
		if depth==1:
			print("")
		return

	def printMMTree(self, tree, depth):
		# print out a minimax tree in MinimaxTree structure
		if len(tree.mmChildren) == 0:
			return
		s = ''
		for j in range(0,depth):
			s += '  '
		s += 'depth '
		s += str(depth) + ': '
		s += str(tree.mmValue) + ' '
		s += str(tree.mmIndex) + ' '
		s += str(tree.mmChildValue)
		print(s)
		for i in range(0, len(tree.mmChildren)):
			self.printMMTree(tree.mmChildren[i],depth+1)
		if depth==1:
			print("")
		return

	def printMMSteps(self, tree, mmtree, depth):
		# print out boards step by step from whole game tree and minimax tree
		if isinstance(tree.gameUtil, int):
			return
		i = mmtree.mmIndex
		gs = Pawned(tree.gameUtil[i].gameState, self.boardSize, self.switchPlayer())
		gs.display()
		self.printMMSteps(tree.gameUtil[i], mmtree.mmChildren[i],depth+1)

	def printABSteps(self, node, abtree, ifprint):
		# print out boards step by step from alphabeta pruned minimax tree
		if self.whoseTurn == 'B':
			player = 'MAX'
		else:
			player = 'MIN'
		if len(abtree.mmChildren) == 0:
			a = GameTree(node.utility(),node.gameState,'TER')
			return a
		succ = node.successors()
		index = abtree.mmIndex
		if index>=len(succ):
			print(index)
			print(succ)
		newNode = Pawned(succ[index], node.boardSize, node.switchPlayer())
		if ifprint:
			newNode.display()
		b = node.printABSteps(newNode, abtree.mmChildren[index], ifprint)
		return GameTree([b],node.gameState,player)

	def optimalSuccMM(self, depth, ifprint, ifrandom, move):
		# decide optimal successor using pure Minimax with limited depth
		gs = None
		moves = []
		succ = self.successorsP(self.whoseTurn, moves)
		if len(succ)==0:
			print("cannot move, skip the turn")
			return gs

		wtree = self.generateWholeTree(depth, depth)
		mmtree = minimax(wtree, ifrandom)
		if ifprint:
			print("whole game tree");
			self.printWholeTree(wtree,0)
			print("minimax tree")
			self.printMMTree(mmtree,0)
			self.printMMSteps(wtree,mmtree,0)
		gs = succ[mmtree.mmIndex]
		m = moves[mmtree.mmIndex]
		move.append(m[0]+1)
		move.append(m[1])
		return gs

	def optimalSuccAB(self, depth, ifprint, ifrandom, move):
		# decide optimal successor using AlphaBeta pruning with limited depth
		gs = None
		moves = []
		succ = self.successorsP(self.whoseTurn, moves)
		if len(succ)==0:
			print("cannot move, skip the turn")
			return gs

		# if someone checkmate
		if self.checkmate():
			selfCheck = self.checkmateP(self.whoseTurn)
			oppoCheck = self.checkmateP(self.switchPlayer())
			#if oppoCheck[0]!=-1:
			#	print(("oppoCheck",oppoCheck))
			#if selfCheck[0]!=-1:
			#	print(("selfCheck",selfCheck))
			
			gs = self.move(self.whoseTurn,selfCheck[0],0)
			m = (selfCheck[0],0)
			if oppoCheck[1]<selfCheck[1] or selfCheck[2]==2 or gs == None:
				#print("opposite checkmate!")
				wtree = self.generateWholeTree(depth, depth)
				mmtree = minimax(wtree, ifrandom)
				gs = succ[mmtree.mmIndex]
				m = moves[mmtree.mmIndex]
			#else:
				#print("self checkmate!")
			move.append(m[0]+1)
			move.append(m[1])
			return gs

		# must know exact values at 2nd level, in order to randomize moves
		abtree = []
		for i in range(0,len(succ)):
			p = Pawned(succ[i],self.boardSize,self.switchPlayer())
			ab = alphabeta(p, -1000, 1000, depth-1, depth-1, ifrandom)
			abtree.append(ab)
			if ifprint:
				print("minimax tree with alphabeta pruning")
				self.printMMTree(ab,0)

		# do the 1st level by hand
		if self.whoseTurn == 'B':
			mmvalue=-1000
			mmlist=[]
			for i in range(0,len(abtree)):
				if abtree[i].mmValue>mmvalue:
					mmvalue = abtree[i].mmValue
					mmlist=[i]
				elif abtree[i].mmValue==mmvalue:
					mmlist.append(i)
		else:
			mmvalue=1000
			mmlist=[]
			for i in range(0,len(abtree)):
				if abtree[i].mmValue<mmvalue:
					mmvalue = abtree[i].mmValue
					mmlist=[i]
				elif abtree[i].mmValue==mmvalue:
					mmlist.append(i)

		if ifrandom:
			rand = int(random.random()*len(mmlist))
		else:
			rand = 0
		mmindex = mmlist[rand]
		gs = succ[mmindex]
		m = moves[mmindex]
		self.printABSteps(self, abtree[mmindex], ifprint)

		move.append(m[0]+1)
		move.append(m[1])
		return gs

	# End of Section5
	######

	def display(self):
		# draw out the board and place all the pieces
		board = []
		for i in range(0,self.boardSize):
			board.insert(0,[])
			for j in range(0,self.boardSize):
				board[0].insert(0,'  ')
		for i in range(0,self.boardSize):
			bp = self.gameState[i]
			wp = self.gameState[i+self.boardSize]
			if bp[0] != -1:
				board[bp[0]-1][bp[1]-1] = 'B'+str(i+1)
			if wp[0] != -1:
				board[wp[0]-1][wp[1]-1] = 'W'+str(i+1)
		s1 = '+'
		for c in range(0,self.boardSize):
			s1 += '--+'
		print(s1)
		for r in range(0,self.boardSize):
			s2 = '|'
			for c in range(0,self.boardSize):
				s2 += board[r][c]
				s2 += '|'
			print(s2)
			print(s1)

######
# Section6: some tree structures to store output from minimax algorithm
class MinimaxTree:
	def __init__(self, value, index, cv, children):
		self.mmValue = value
		self.mmIndex = index
		self.mmChildValue = cv
		self.mmChildren = children

class GameTree:
	def __init__(self, util, state, who):
		self.gameUtil = util # both the utility and a list of successors
		self.gameState = state # a state that describes each piece's position
		self.player = who # 'MIN' ''MAX' 'TER'
		return

	def isMinNode(self):
		if self.player == 'MIN':
			return True
		else:
			return False

	def isMaxNode(self):
		if self.player == 'MAX':
			return True
		else:
			return False

	def isTerminal(self):
		if self.player == 'TER':
			return True
		else:
			return False

	def successors(self):
		return self.gameUtil

	def utility(self):
		return self.gameUtil

# End of Section6
######
