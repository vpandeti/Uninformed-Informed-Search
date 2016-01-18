from _ast import Return
from operator import pos

import readGame


#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################
class game:
	# Size of the board ROWS X COLUMNS
	ROWS = 7
	COLUMNS = 7
	def __init__(self, filePath):
    		self.gameState = readGame.readGameState(filePath)
            	self.nodesExpanded = 0
		self.trace = []	
	
	def is_corner(self, pos):
		########################################
		# You have to make changes from here
		# check for if the new position is a corner or not
		# return true if the position is a corner
		
		# Checking boundary conditions on the matrix
		if(self.checkBoundaries(pos) == False):
			return True
		# If element is -1, it is corner
		if (self.gameState[pos[0]][pos[1]] == -1):
			return True
		else:
			return False	
	
	# Returns new element based on the direction
	def getNextPosition(self, oldPos, direction):
		#########################################
		# YOU HAVE TO MAKE CHANGES HERE
		# See DIRECTION dictionary in config.py and add
		# this to oldPos to get new position of the peg if moved
		# in given direction , you can remove next line
		newPosition = [oldPos[0], oldPos[1]];
		# Direction: South, move 2 places down
		if(direction[0] == 1 and direction[1] == 0):
			newPosition[0] = newPosition[0] + 2
		# Direction: North, move 2 places up
		elif(direction[0] == -1 and direction[1] == 0):
			newPosition[0] = newPosition[0] - 2
		# Direction: east, move 2 places right
		elif(direction[0] == 0 and direction[1] == 1):
			newPosition[1] = newPosition[1] + 2
		# Direction: South, move 2 places left
		else:
			newPosition[1] = newPosition[1] - 2
		return newPosition
	
	# Check if it is a valid move
	def is_validMove(self, oldPos, direction):
		#########################################
		# DONT change Things in here
		# In this we have got the next peg position and
		# below lines check for if the new move is a corner
		
		newPos = self.getNextPosition(oldPos, direction)
		# Checking the boundary condition of matrix
		isBoundary = self.checkBoundaries(newPos)
		if(isBoundary == False):
			return False
		#########################################
		
		########################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# check for cases like:
		# if new move is already occupied
		# or new move is outside peg Board
		# Remove next line according to your convenience
		
		# Checking if the newPos is a corner
		if self.is_corner(newPos):
			return False
		# Checking if newPos is empty, if newPos is not empty return false
		try:
			if(self.gameState[newPos[0]][newPos[1]] != 0):
				return False
		except IndexError:
			print("Error, Index error in is_validMove") 
			return False
		# Checking if it is trying to delete a peg
		try:
			southX = oldPos[0] + 1
			southY = oldPos[1]
			northX = oldPos[0] - 1
			northY = oldPos[1]
			eastX = oldPos[0]
			eastY = oldPos[1] + 1
			westX = oldPos[0]
			westY = oldPos[1] - 1
			# Direction: South
			if(direction[0] == 1 and direction[1] == 0 and self.gameState[southX][southY] == 1):
				return True
			# Direction: North
			elif(direction[0] == -1 and direction[1] == 0 and self.gameState[northX][northY] == 1):
				return True
			# Direction: East
			elif(direction[0] == 0 and direction[1] == 1 and self.gameState[eastX][eastY] == 1):
				return True
			# Direction: West
			elif(direction[0] == 0 and direction[1] == -1 and self.gameState[westX][westY] == 1):
				return True
			else:
				return False
		except IndexError:
			return False
	
	def getNextState(self, oldPos, direction):
		###############################################
		# DONT Change Things in here
		self.nodesExpanded += 1
		if not self.is_validMove(oldPos, direction):
			print("Error, You are not checking for valid move")
			exit(0)
		###############################################
		
		###############################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# Update the gameState after moving peg
		# eg: remove crossed over pegs by replacing it's
		# position in gameState by 0
		# and updating new peg position as 1
		
		newPos = self.getNextPosition(oldPos, direction)
		# Set element to which the peg jumped to 1
		self.gameState[newPos[0]][newPos[1]] = 1;
		# Set element from which the peg jumped to 0
		self.gameState[oldPos[0]][oldPos[1]] = 0;
		try:
			southX = oldPos[0] + 1
			southY = oldPos[1]
			northX = oldPos[0] - 1
			northY = oldPos[1]
			eastX = oldPos[0]
			eastY = oldPos[1] + 1
			westX = oldPos[0]
			westY = oldPos[1] - 1
			# Set element to which has been removed by the current move to 0
			if(direction[0] == 1 and direction[1] == 0):
				self.gameState[southX][southY] = 0
			elif(direction[0] == -1 and direction[1] == 0):
				self.gameState[northX][northY] = 0
			elif(direction[0] == 0 and direction[1] == 1):
				self.gameState[eastX][eastY] = 0
			elif(direction[0] == 0 and direction[1] == -1):
				self.gameState[westX][westY] = 0
		except IndexError:
			print("Error, You are not checking for valid move - Index error")
		return self.gameState

	# This function checks if the peg is moving out of the boundaries
	def checkBoundaries(self, pos):
	###############################################
	# Checking the boundary conditions
		if(pos[0] < 0):
			return False
		if(pos[0] >= self.ROWS):
			return False
		if(pos[1] < 0):
			return False
		if(pos[1] >= self.COLUMNS):
			return False
		return True