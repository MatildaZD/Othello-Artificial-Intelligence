
import time
import random
import numpy as np
from numpy import inf
import dummyOthello
import humanOthello

SIZE = 8

def possibleMoves(board, turn, check=[-1,1]): #returns list of Possible Moves 
	lst = []
	turnSave = turn #actual turn
	for t in check: #check both playersif necessary
		turn = t
		for i in range(SIZE):
			for j in range(SIZE):
				#only run checkMove if spot is empty
				#since checkMove is expensive
				if board[i,j] == 0:
					if checkMove(board.copy(),i,j, turnSave):
						lst.append((i,j))
						turn = turnSave #restore correct turn
		turn = turnSave
		return lst 

def noMoves(board, turn, check=[-1,1]): #returns true and false if game state is over/not over
	lst = []
	turnSave = turn #actual turn
	for t in check: #check both playersif necessary
		turn = t
		for i in range(SIZE):
			for j in range(SIZE):
				#only run checkMove if spot is empty
				#since checkMove is expensive
				if board[i,j] == 0:
					if checkMove(board.copy(),i,j, turnSave):
						turn = turnSave #restore correct turn
						return False

	turn = turnSave #restore correct turn
	return True #use this to check if game is over #returns True if no legal moves Possible, False if more moves

def checkMove(board,row, col, turn):
		#position is not empty
		if board[row, col] != 0:
			return []
		stonesToFlip = []

		#8 directions
		#			  down	  up	  right	  left	  dr 	  dl	   ur		ul  
		directions = [(1,0), (-1, 0), (0,1), (0,-1), (1, 1), (1, -1), (-1,1), (-1, -1)]
		for d in directions:
			flank = False
			r = row + d[0]#first position we're checking
			c = col + d[1]#in the current direction

			#temporary list of positions to flip
			#don't know if accurate until we find that the stones are surrounded
			tempflips = []
			#while we're still on the board

			while r >= 0 and r < SIZE and c >= 0 and c < SIZE:
				#first we should find stones of opponts color
				if board[r,c] == -turn:
					flank = True
					tempflips.append((r,c))#opponent stones we might flip

				#then a stone of our color, so the line is surrounded
				elif board[r,c] == turn:
					if flank:#found stones of opponent color surrounded by our color
						stonesToFlip += tempflips
						break 

					else: #if no stones of opponents color
						break #break without adding any stones

				else: #found a blank spot when expecting something else
					break #break without adding any stones

				r += d[0] #next 
				c += d[1] #position

			#if we reached the end of the loop without finding flanked stones, no stones are added
		#We've searched all directions
		return stonesToFlip #list of stones to flip  #returns list of coordinates of stones to flip  ##returns a list of stones to flip

def makeMove(board, move, turn):  
	#-1 white
	#1 black
	stonesToflip = checkMove(board,move[0],move[1],turn) 
	newBoard = board.copy()
	if turn == 1:
		newBoard[move] = 1
		for i in stonesToflip:
			newBoard[i] = 1
		return newBoard
	else:
		newBoard[move] = -1
		for i in stonesToflip:
			newBoard[i] = -1
		return newBoard#returns a new board with a move made on it

def evaluate(board): #returns a score for a board state
	#if black add point - max
	#if white lower points - min 
	#black - positive
	#white negative 
	
	#update this when checking for things 
	#want to check for corners, danger zone pieces, number of pieces, how many moves are availible
	score = 0


	#---------------
	corners = [(0,0),(0,7),(7,7),(7,0)]#WANT ALL THE CORNERS --> SCORE GOES UP BIGTIME 
	for i in corners:
		if board[i] == 1:
			score+=1000
		if board[i]==-1:
			score-=1000
		else:
			pass
	#want center peices:
	center = []
	for i in range(2,6): 
		center.append((5,i))
		center.append((i,2))
		center.append((2,i))
		center.append((i,5))
		center.append((i,i))
		center.append((7-i,i))
	for i in center:
		if board[i] == 1:
			score += 5 #not too much tho - only adds small amount 
		if board[i] == -1:
			score -=5
	
	xSquares = [] #only want peices here if the corner has already been taken by your own color
	#otherwise having pieces here allows ur opponent to get a corner
	for i in range(1,2): 
		xSquares.append((0,i))
		xSquares.append((i,0))
	xSquares.append((1,1))
	for i in xSquares:
		if board[0,0] == 0 and board[i] == 1:
			score -= 50
		if board[0,0] == 0 and board[i] == -1:
			score += 50
		if board[0,0] == 1 and board[i] == 1:
			score += 40
		if board[0,0] == -1 and board[i] == -1:
			score -= 40
		if board[0,0] == 1 and board[i] == -1:
			score += 40
		if board[0,0] == -1 and board[i] == 1:
			score -= 40
	xSquares= [(0,6),(1,7),(1,6)]
	for i in xSquares:
		if board[0,7] == 0 and board[i] == 1:
			score -= 50
		if board[0,7] == 0 and board[i] == -1:
			score += 50
		if board[0,7] == 1 and board[i] == 1:
			score += 40
		if board[0,7] == -1 and board[i] == -1:
			score -= 40
		if board[0,7] == 1 and board[i] == -1:
			score += 40
		if board[0,7] == -1 and board[i] == 1:
			score -= 40
	xSquares= [(6,0),(7,1),(6,1)]
	for i in xSquares:
		if board[7,0] == 0 and board[i] == 1:
			score -= 50
		if board[7,0] == 0 and board[i] == -1:
			score += 50
		if board[7,0] == 1 and board[i] == 1:
			score += 40
		if board[7,0] == -1 and board[i] == -1:
			score -= 40
		if board[7,0] == 1 and board[i] == -1:
			score += 40
		if board[7,0] == -1 and board[i] == 1:
			score -= 40
	xSquares= [(6,7),(7,6),(6,6)]
	for i in xSquares:
		if board[7,7] == 0 and board[i] == 1:
			score -= 50
		if board[7,7] == 0 and board[i] == -1:
			score += 50
		if board[7,7] == 1 and board[i] == 1:
			score += 40
		if board[7,7] == -1 and board[i] == -1:
			score -= 40
		if board[7,7] == 1 and board[i] == -1:
			score += 40
		if board[7,7] == -1 and board[i] == 1:
			score -= 40


	innerEdges = [] #peices that arent xsquares but are inner edges - still risky 
	for i in range(2,6): 
		innerEdges.append((0,i))
		innerEdges.append((i,0))
		innerEdges.append((7,i))
		innerEdges.append((i,7))
	for i in innerEdges:
		if board[i] == 1:
			score -= 15
		if board[i] == -1:
			score += 15

	outerEdges = []
	for i in range(2,6): 
		outerEdges.append((1,i))
		outerEdges.append((i,1))
		outerEdges.append((6,i))
		outerEdges.append((i,6))
	for i in outerEdges:
		if i[1] == 0 or i[1]==7:
			if board[i] == 1 and (board[i[0]+1,i[1]] != -1 or board[i[0]-1,i[1]] != -1): 
				#tries to check for edge pieces but no piece directly next to it -  because you lose the edge 
				#if there is one next to it 
				score+=25
			elif board[i] == 1 and (board[i[0]+1,i[1]] == -1 or board[i[0]-1,i[1]] == -1):
				score -= 25
			elif board[i] == -1 and (board[i[0]+1,i[1]] != 1 or board[i[0]-1,i[1]] != 1): 
				score-=25
			elif board[i] == -1 and (board[i[0]+1,i[1]] == 1 or board[i[0]-1,i[1]] == 1):
				score += 25
			else:
				pass
		elif i[0] == 0 or i[0]==7: #does this for both the columns and rows - peices next to will be different
			if board[i] == 1 and (board[i[0],i[1]+1] != -1 or board[i[0],i[1]-1] != -1): 
				score+=25
			elif board[i] == 1 and (board[i[0],i[1]+1] == -1 or board[i[0],i[1]-1] == -1):
				score -= 25
			elif board[i] == -1 and (board[i[0],i[1]+1] != 1 or board[i[0],i[1]-1] != 1): 
				score-=25
			elif board[i] == -1 and (board[i[0],i[1]+1] == 1 or board[i[0],i[1]-1] == 1):
				score += 25
			else:
				pass

	
	blackPos = possibleMoves(board, 1, check=[-1,1])
	whitePos = possibleMoves(board, -1, check=[-1,1])
	if len(blackPos) == 0:
		score -= 40 #no possible moves = bad 
	elif len(whitePos) == 0:
		score += 40
	#score += len(blackPos)
	#score -= len(whitePos)
	
	return score

def ABPrune(board, A, B, turn, depth):
	possible_Moves = possibleMoves(board, turn)
	depth+=1
	if depth>=4:
		return evaluate(board) #Which will be from the hueristic 
	elif noMoves(board,turn) == True:
		if board.sum()>0:
			return 10000
		elif board.sum()<0:
			return -10000
		else:
			return 0

	#elif noMoves(board, [turn]):
		#return ABPrune(board.copy(),A,B,-1*turn,depth+1)

	alpha = A 
	beta = B 
	#print("alpha: " + str(alpha))
	#print("beta: "+ str(beta))
	if turn == 1: #Black
		
		if len(possible_Moves) ==0:
			newBoard = board.copy()
			alpha = max(alpha, ABPrune(newBoard,alpha, beta, -1,depth))

		#for each child from check Move 
		for i in possible_Moves: #--> find possible moves 
			temp = makeMove(board,i,turn)
			alpha = max(alpha, ABPrune(temp,alpha, beta, -1,depth))
			if alpha >= beta:
				return alpha 
		return alpha 
	else: #white --> -1
		if len(possible_Moves) ==0:
			newBoard = board.copy()
			alpha = max(alpha, ABPrune(newBoard,alpha, beta, 1,depth))
		#for each child from check Move 
		for i in possible_Moves: #--> find possible moves
			temp = makeMove(board,i,turn) 
			beta = min(beta, ABPrune(temp,alpha, beta, 1,depth))
			if alpha >= beta:
				return beta

		return beta #Minimax function  #The minimax algorithm#MiniMax Alpha Beta Pruning Algorithm

def getMove(board,turn):

	#need to return -1,-1 to pass if no legal moves are availible 


	bestScore = None
	bestMove = None 
	depth = 0
	possible_Moves = possibleMoves(board, turn)
	alpha = -inf 
	beta = inf
	if len(possible_Moves)==0:
		return (-1,-1)
	if turn == 1: #Black
		#for each child from check Move 
		for i in possible_Moves: #--> find possible moves 
			temp = makeMove(board,i,turn)
			alpha = max(alpha, ABPrune(temp,alpha, beta, -1,depth))
			if bestScore == None or alpha > bestScore:
				bestScore = alpha
				bestMove = i

	else: #white --> 1
		#for each child from check Move 
		for i in possible_Moves: #--> find possible moves
			temp = makeMove(board,i,turn) 
			beta = min(beta, ABPrune(temp,alpha, beta, 1,depth))
			if bestScore == None or beta < bestScore:
				bestScore=beta
				bestMove = i

	return bestMove #returns the best move - calls alpha beta pruning
	




