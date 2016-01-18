from Queue import PriorityQueue
from copy import deepcopy

from pegSolitaireUtils import game
import pegSolitaireUtils

# Board dimensions
ROWS = 7
COLUMNS = 7
reverse = []
# Stack to push and pop nodes in case of Iterative deepening
Stack = []

# Boolean flag variable to know if goal test is true
isGoalFound = False

# goal node for reference in case of goal test
goalNode = []

# goal path (to print the path)
goalPath = []

# For Pruning
visitedNodes = []

# Node that contains the data and traversed path
class TraversingNode(object):
	
	def __init__(self, data, direction):
		self.data = data
		self.direction = direction
		
	# Returns the node
	def getData(self):
		return self.data
	
	# Returns the traversed direction
	def getDirection(self):
		return self.direction
	

def ItrDeepSearch(pegSolitaireObject):
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	# 
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you 
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you 
	# reach goal using Iterative Deepening Search.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to save
	#
	#################################################
	#pegSolitaireUtils.game.getNextPosition(pegSolitaireObject.self, oldPos, direction)
	initialState(pegSolitaireObject)
	return True

# Pruning: Check if a node has already been visited.
def checkIfNodeIsVisited(node):
	# Scans the visited array for the given node. Perform 1 to 1 comparison
	for i in range(len(visitedNodes)):
		n = visitedNodes[i]
		x = 0
		for j in range(ROWS):
			for k in range(COLUMNS):
				if(n[j][k] == node[j][k]):
					x += 1
				else:
					break
		if(x == (ROWS * COLUMNS)):
			return True
	return False

# Performs depth limited search for a given depth
def doDepthLimitedSearch(pegSolitaireObject, parentNode, tillDepth):
	global Stack
	global visitedNodes
	global goalNode
	global isGoalFound
	global goalPath
	# if max depth is reached, quit
	if(tillDepth == 0):
		return
	# if goal test is success, quit
	if(isGoalFound == True):
		return True
	# Implementation of pruning. Do not expand the nodes that have already been expanded
	if(checkIfNodeIsVisited(parentNode.getData()) == True):
			return
	else:
		visitedNodes.append(parentNode.getData())
	# Push the node into stack
	Stack.append(parentNode);
	while (len(Stack) != 0):
		node = Stack.pop()
		# performs goal test
		# if goal test is success, empty the stack and quit
		if(checkGoalState(node.getData()) == True):
			isGoalFound = True
			# goalPath.append(deepcopy(parentNode))
			emptyStack()
			return
		if(tillDepth == 0):
			return
		# Performs successor function
		flag = successorFunction(pegSolitaireObject, node)
		if(flag == True):
			return
		elif (flag == None):
			# print("There is no result in depth: ", tillDepth)
			break
		else:
			leaves = flag
			# expand the nodes that are in the fringe list
			for k in range(len(leaves)):
				if(checkGoalState(leaves[k].getData()) == True):
					isGoalFound = True
					goalNode = deepcopy(leaves[k])
				doDepthLimitedSearch(pegSolitaireObject, leaves[k], tillDepth - 1)
				# if goal test is success, quit
				if(isGoalFound == True):
					goalPath.append(deepcopy(leaves[k]))
					emptyStack()
					return

# Checks if a peg is jumping to the valid location. Calls is_validMove method of pegSolitaireUtils
def checkIfValidMovesExist(pegSolitaireObject, oldPos, direction):
	return game.is_validMove(pegSolitaireObject, oldPos, direction)

# Defines the initial state of the board and starts IDS search
def initialState(pegSolitaireObject):
	try:
		depth = 0
		global goalPath
		node = list(pegSolitaireObject.gameState)
		sNode = deepcopy(node)
		tNode = TraversingNode(sNode, "")
		goalPath.append(tNode)
		global visitedNodes
		# Starts Iterative Deepening search for the increasing depths
		while (isGoalFound == False):
			visitedNodes = []
			doDepthLimitedSearch(pegSolitaireObject, tNode, depth)
			depth += 1
		global goalNode
		if(goalNode != None and goalNode.getDirection() != None):
			pegSolitaireObject.trace.append(goalNode.getDirection())
	except:
		print ("")
# left   : i, j - 2, direction (west) :  0, -1 
# right  : i, j + 2, direction (east) :  0,  1
# top    : i - 2, j, direction (north): -1,  0
# bottom : i + 2, j, direction (south):  1,  0
def successorFunction(pegSolitaireObject, parentNode):
	global Stack
	leaves = []
	node = parentNode.getData()
	for i in range(ROWS):
		for j in range(COLUMNS):
			if(node[i][j] == 1):
				oldPos = [i, j]
				
				# move left
				direction = [0, -1]
				pegSolitaireObject.gameState = deepcopy(node)
				if(checkIfValidMovesExist(pegSolitaireObject, oldPos, direction) == True):
					updatedStateLeft = pegSolitaireUtils.game.getNextState(pegSolitaireObject, oldPos, direction)
					if(updatedStateLeft != None):
						leftNode = deepcopy(updatedStateLeft)
						direction = parentNode.getDirection()
						# tracing the movements
						s = "(%d,%d),(%d,%d)," %(i, j, i, (j-2))
						tNode = TraversingNode(leftNode, deepcopy(direction + s))
						leaves.append(deepcopy(tNode))
				
				# move right
				direction = [0, 1]
				pegSolitaireObject.gameState = deepcopy(node)
				if(checkIfValidMovesExist(pegSolitaireObject, oldPos, direction) == True):
					updatedStateEast = pegSolitaireUtils.game.getNextState(pegSolitaireObject, oldPos, direction)
					if(updatedStateEast != None):
						rightNode = deepcopy(updatedStateEast)
						direction = parentNode.getDirection()
						# tracing the movements
						s = "(%d,%d),(%d,%d)," %(i, j, i, (j+2))
						tNode = TraversingNode(rightNode, deepcopy(direction + s))
						leaves.append(deepcopy(tNode))

				# move north
				direction = [-1, 0]
				pegSolitaireObject.gameState = deepcopy(node)
				if(checkIfValidMovesExist(pegSolitaireObject, oldPos, direction) == True):
					updatedStateNorth = pegSolitaireUtils.game.getNextState(pegSolitaireObject, oldPos, direction)
					if(updatedStateNorth != None):
						northNode = deepcopy(updatedStateNorth)
						direction = parentNode.getDirection()
						# tracing the movements
						s = "(%d,%d),(%d,%d)," %(i, j, (i-2), j)
						tNode = TraversingNode(northNode, deepcopy(direction + s))
						leaves.append(deepcopy(tNode))
				
				# move south
				direction = [1, 0]
				pegSolitaireObject.gameState = deepcopy(node)
				if(checkIfValidMovesExist(pegSolitaireObject, oldPos, direction) == True):
					updatedStateSouth = pegSolitaireUtils.game.getNextState(pegSolitaireObject, oldPos, direction)
					if(updatedStateSouth != None):
						southNode = deepcopy(updatedStateSouth)
						direction = parentNode.getDirection()
						# tracing the movements
						s = "(%d,%d),(%d,%d)," %(i, j, (i+2), j)
						tNode = TraversingNode(southNode, deepcopy(direction + s))
						leaves.append(deepcopy(tNode))
	return leaves
		
def checkGoalState(node):
	# See if node contains element '1' only at the center of the matrix
	midX = ROWS/2
	midY = COLUMNS/2;
	for i in range(0, ROWS):
		for j in range(0, COLUMNS):
			if(node[i][j] == 1):
				if(i == midX and j == midY):
					return True
				else:
					return False
	return False

# Empties the stack
def emptyStack():
	global Stack
	while(len(Stack) != 0):
		Stack.pop()

def aStarOne(pegSolitaireObject):
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	# 
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you 
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you 
	# reach goal using A-Star searching with first Heuristic
	# you used.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to return
	#
	#################################################
	# gameState = pegSolitaireObject.gameState
	try:
		global visitedNodes
		visitedNodes = []
		node = list(pegSolitaireObject.gameState)
		sNode = deepcopy(node)
		tNode = TraversingNode(sNode, "")
		# Priority queue for heuristic search
		pQueue = PriorityQueue()
		tPath = heuristicSearch(pegSolitaireObject, tNode, True, pQueue)
		
		if(tPath == None):
			print("No solution is found for the given board configuration")
			return False
		else:
			# Appending the trace
			pegSolitaireObject.trace.append(tPath)
			return True
	except:
		print ("")
# isFirstHeuristicSearch is True for AStarOne, False for AStarTwo
def heuristicSearch(pegSolitaireObject, parentNode, isFirstHeuristicSearch, pQueue):
	pQueue.put((1, parentNode))
	if(checkGoalState(parentNode.getData()) == True):
		return parentNode.getDirection()
	while (not pQueue.empty()): 
		queueItem = pQueue.get()
		pNode = queueItem[1]
		# Implementation of pruning. Do not expand the nodes that have already been expanded
		if(checkIfNodeIsVisited(pNode.getData()) == True):
				continue
		else:
			visitedNodes.append(pNode.getData())
		leaves = successorFunction(pegSolitaireObject, pNode);
		for i in range(len(leaves)):
			hValue = 0
			# Calculating the heuristic value
			if(isFirstHeuristicSearch == True):
				hValue = getFirstHeuristic(parentNode.getData(), leaves[i].getData())
			else:
				hValue = getSecondHeuristic(parentNode.getData(), leaves[i].getData())
			pQueue.put((hValue, leaves[i]))
			# Goal test
			if(checkGoalState(leaves[i].getData()) == True):
				return leaves[i].getDirection()
			# print("h: ", hValue)
	# print("No solution exists in the given board configuration")
	return

# Calculates F(n) = H(n) + G(n)
def getFirstHeuristic(parentNode, currentNode):
	# Calculates H(n)
	distance = getDistanceFromCenter(currentNode)
	# Calculates G(n)
	edgeCost = getEdgeCost(parentNode, currentNode)
	# print("distance: ", distance)
	# print("edgeCost: ", edgeCost)
	# print(currentNode)
	return distance + edgeCost
	
# Using Manhattan distance H(n)
def getDistanceFromCenter(node):
	x = 0;
	midX = ROWS/2
	midY = COLUMNS/2
	for i in range(ROWS):
		for j in range(COLUMNS):
			if(node[i][j] == 1):
				a = (midX - i)
				b = (midY - j)
				x += ((a if a > 0 else -a) + (b if b > 0 else -b))
	return x

# Calculating edge cost G(n)
def getEdgeCost(parentNode, currentNode):
	x = 0
	for i in range(ROWS):
		for j in range(COLUMNS):
			a = parentNode[i][j] - currentNode[i][j]
			x += a if a > 0 else -a
	return x

def aStarTwo(pegSolitaireObject):
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	# 
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you 
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you 
	# reach goal using A-Star searching with second Heuristic
	# you used.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to return
	#
	#################################################
	try:
		global visitedNodes
		visitedNodes = []	
		node = list(pegSolitaireObject.gameState)
		sNode = deepcopy(node)
		tNode = TraversingNode(sNode, "")	
		# Priority queue for heuristic search
		pQueue = PriorityQueue()
		tPath = heuristicSearch(pegSolitaireObject, tNode, False, pQueue)
		if(tPath == None):
			return False
		else:
			pegSolitaireObject.trace.append(tPath)
	except:
		print ("")	
def getSecondHeuristic(parentNode, currentNode):
	heuristic = getNoOfIsolatedNodesAndTotalNodes(currentNode)
	# print("heuristic: ", heuristic)
	return heuristic		

# Calculates second heuristic value H(N) for AStarTwo
# Finds number of isolated pegs which does not have any moves
# and total pegs in the board
def getNoOfIsolatedNodesAndTotalNodes(node):
	noOfPegs = 0
	noOfisolatedPegs = 0
	for i in range(ROWS):
		for j in range(COLUMNS):
			if(node[i][j] == 1):
				# total pegs on the board
				noOfPegs += 1
			# Starts calculating the isolated pegs
			# check west
				x = i
				y = j-1
				west = False
				isOutOfBoundary = (x < 0 or x >= ROWS or y < 0 or y >= COLUMNS) 
				if(isOutOfBoundary == False and node[x][y] == 0):
					west = True
			# check east
				x = i
				y = j+1
				east = False
				isOutOfBoundary = (x < 0 or x >= ROWS or y < 0 or y >= COLUMNS)
				if(isOutOfBoundary == False and node[x][y] == 0):
					east = True
			# check north
				x = i-1
				y = j
				north = False
				isOutOfBoundary = (x < 0 or x >= ROWS or y < 0 or y >= COLUMNS)
				if(isOutOfBoundary == False and node[x][y] == 0):
					north = True		
			# check south
				x = i+1
				y = j
				south = False
				isOutOfBoundary = (x < 0 or x >= ROWS or y < 0 or y >= COLUMNS)
				if(isOutOfBoundary == False and node[x][y] == 0):
					south = True
				
				if(east == True and west == True and north == True and south == True):
					noOfisolatedPegs += 1
	return noOfPegs + noOfisolatedPegs