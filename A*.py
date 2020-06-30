############################################################	
###     		Traffic Jam Puzzle AI Solver			 ###
###		Authors: Abdul Qadeer Rehan and Mahad Bhatti	 ###
###					Date: Feb 6,2020        			 ###
############################################################	
import copy
import math

# E = Empty 
# V = VERTICAL CAR
# v = VERTICAL CAR ABOVE OR BELOW A VERTICAL CAR allows to distinguish between the car
# H = HORIZONTAL CAR
# h = HORIZONTAL CAR TO THE LEFT OR RIGHT OF A HORIZONTAL CAR allows to distinguish between the car
# G = red car (the car we want to move to the exit)

#initial state 1
input1 = [['E','E','E','V','H','H'], ['E','E','E','V','H','H'], ['V','H','H','H','h','h'], ['V','E','E','E','E','G'], ['E','E','H','H','H','G'], ['E','E','E','E','E','E']]
#cell coordinates of the cell with the door on one of its edges 
goal1 = [5,0]

#initial state 2
input2 = [['V','V','V','H','H','H'], ['V','V','V','H','H','H'], ['V','V','H','H','h','h'], ['H','H','E','E','G','E'], ['E','E','E','E','G','E'], ['E','E','H','H','E','E']]
#cell coordinates of the cell with the door on one of its edges 
goal2 = [4,0]

#initial state 3
input3 = [['E','E','V','H','H','H'], ['E','E','V','V','H','H'], ['E','V','V','V','E','G'], ['V','V','H','H','H','G'], ['V','V','E','H','H','H'], ['V','E','E','E','E','E']]
#cell coordinates of the cell with the door on one of its edges 
goal3 = [5,0]


###########################################################	
# Goal Testing method:                                    #
# for a given 2d matrix determines whether it is the goal #
# state or not by checking if the red car occupies the    #
# cell with the door on one of its edges                  #
# Paramters:                                              #
# 1) row: row number of the cell with the door on one of  #
#         its edges                                       #
# 2) col: col number of the cell with the door on one of  #
#         its edges                                       #
# 3) check: 2d array to run goal test on 				  #
# Return:												  #
# 1) True: if given 2d array is the goal state            #
# 2) False: if given 2d array is not the goal state       #					
###########################################################
def goalTest(row, col, check):
	if (check[row][col] == 'G'):
		return True
	else: 
		return False


###########################################################	
# Heuristic #1:                                           #
# determines the number of cars blocking the exit         #
# (between red car and exit)                              #
# Paramters:                                              #
# 1) matrix: 2d array for which to calculate the heuristic#
# 2) col: the column number of where the exit is in array #
###########################################################
def h1(matrix, col):
	count = 0
	for row in matrix:
		if((row[col] != 'E' and row[col] != 'G')):
			count = count + 1
		for value in row:
			if value == 'G':
				return(count)


###########################################################	
# Heuristic #2:                                           #
# determines the number of cells between red car and exit #
# (between red car and exit)                              #
# Paramters:                                              #
# 1) matrix: state for which to calculate the heuristic   #
###########################################################
def h2(matrix):
	count = 0
	for row in matrix:
		count = count + 1
		for value in row:
			if value == 'G':
				#print(count)
				return(count)


###########################################################	
# Display method:                                         #
# prints out the given 2d matrix to the console			  #
# Paramters:                                              #
# 1) matrix: 2d array to print to console  				  #
###########################################################
def display(matrix):
	for row in matrix:
		for value in row:
			print(value, end = ' ')
		print("")


###########################################################	
# Action method:                                          #
# Returns a list of all possible successor states from the# 
# given state as in the 2d array passed to the method     #
# Paramters:                                              #
# 1) matrix: 2d array for which to generate successor     #
#            states                                       #
# Return:                                                 #
# list of list containing all possible successor states	  #
###########################################################
def action(matrix):
	successors = []
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			duplicate = copy.deepcopy(matrix)
			#if cell is empty no need to check
			if(matrix[i][j] == 'E'):
				continue

			#if cell has vertical car or Red car(assuming red car is always vertical)
			if(matrix[i][j] == 'V' or matrix[i][j] == 'v' or matrix[i][j] == 'G'):
				#cell below is empty
				try:
					if(matrix[i+1][j] == 'E' and i+1 < len(matrix)):
						if(i-2 >= 0 and i-2 < len(matrix)):
							#if truck
							if(matrix[i][j] == matrix[i-1][j] == matrix[i-2][j]):
								#move truck one cell forward
								duplicate[i-2][j] = 'E'
								duplicate[i+1][j] = duplicate[i][j]
								successors.append(duplicate)
								continue

						if(i-1 >= 0 and i-1 < len(matrix)-1):
							#if car
							if(matrix[i][j] == matrix[i-1][j]):
								#move car one cell forward
								duplicate[i-1][j] = 'E'
								duplicate[i+1][j] = duplicate[i][j]
								successors.append(duplicate)
								continue

				except Exception as e:
					pass
				

				#cell above is empty
				try:
					if(matrix[i-1][j] == 'E' and i-1 >= 0):
						if(i+2 >= 0 and i+2 < len(matrix)):
							#if truck
							if(matrix[i][j] == matrix[i+1][j] == matrix[i+2][j]):
								#move truck one cell forward
								duplicate[i+2][j] = 'E'
								duplicate[i-1][j] = duplicate[i][j]
								successors.append(duplicate)
								continue

						if(i+1 >= 0 and i+1 < len(matrix)):
							#if car
							if(matrix[i][j] == matrix[i+1][j]):
								#move car one cell forward
								duplicate[i+1][j] = 'E'
								duplicate[i-1][j] = duplicate[i][j]
								successors.append(duplicate)
								continue
				except Exception as e:
					pass

			if(matrix[i][j] == 'H' or matrix[i][j] == 'h'):
				#cell to the right is empty
				try:
					if(matrix[i][j+1] == 'E' and j+1 < len(matrix)):
						if(j-2 >= 0 and j-2 < len(matrix[0])):
							#if truck
							if(matrix[i][j] == matrix[i][j-1] == matrix[i][j-2]):
								#move truck one cell forward
								duplicate[i][j-2] = 'E'
								duplicate[i][j+1] = duplicate[i][j]
								successors.append(duplicate)
								continue

						if(j-1 >= 0 and j-1 < len(matrix)):
							#if car
							if(matrix[i][j] == matrix[i][j-1]):
								#move car one cell forward
								duplicate[i][j-1] = 'E'
								duplicate[i][j+1] = duplicate[i][j]
								successors.append(duplicate)
								continue
				except Exception as e:
					pass

				#cell to the left is empty
				try:
					if(matrix[i][j-1] == 'E' and j-1 >= 0):
						if(j+2 >= 0 and j+2 < len(matrix[0])):
							#if truck
							if(matrix[i][j] == matrix[i][j+1] == matrix[i][j+2]):
								#move truck one cell forward
								duplicate[i][j+2] = 'E'
								duplicate[i][j-1] = duplicate[i][j]
								successors.append(duplicate)
								continue

						if(j+1 >= 0 and j+1 < len(matrix)):
							#if car
							if(matrix[i][j] == matrix[i][j+1]):
								#move car one cell forward
								duplicate[i][j+1] = 'E'
								duplicate[i][j-1] = duplicate[i][j]
								successors.append(duplicate)
								continue
				except Exception as e:
					pass

	return(successors)


###########################################################	
# Get Path method:                                        #
# prints out and returns path taken to arrive at the given# 
# state	                                                  #
# Paramters:                                              #
# 1) matrix: state for which to print path  			  #
###########################################################
def getPath(matrix, frontier):
	returnList = []
	curr = matrix
	while(curr != None):
		returnList.append(curr[0])
		curr = curr[4]
	return returnList


###########################################################	
# A* method:	                                          #
# Runs A* search on the given 2d array to find the 		  #
# shortest sequence of moves allowing the red car to      #
# occupy the cell with the door on one of its edges.      #
# Once optimal path is found calls getPath to print and   #
# return the optimal path found. 						  #
# Paramters:                                              #
# 1) matrix: initial state to run A* search on 			  #
# 2) goalX: row number of the cell with the door on one   #
#           of its edges.		                          #
# 3) goalY: col number of the cell with the door on one   #
#			of its edges.								  #
# 4) frontier: an instance of the PriorityFrontier class  #
###########################################################
def aStar(matrix, goalX, goalY, frontier):

	#if initial state is goal state
	if (goalTest(goalX, goalY, matrix)):
		display(matrix)
		print("")
		return getPath(matrix, frontier)

	#comment out line of code according to the heuristic you wish to investigate

	#frontier.insert(matrix, 0, h1(matrix, goalY), None)
	frontier.insert(matrix, 0, h2(matrix), None)

	interior = []
	g = 0
	stateCounter = 0
	while(not(frontier.isEmpty())):
		stateCounter = stateCounter + 1
		current = frontier.getSmallest()
		interior.append(current[0])

		if (goalTest(goalX, goalY, current[0])):
			result = getPath(current, frontier)
			stepCount = 0
			i = len(result) - 1
			while i >= 0:
				print("State: ", stepCount)
				display(result[i])
				print("")
				stepCount = stepCount + 1
				i = i - 1
			# Comment out to not print number of states checked
			print("Number of States checked: ", stateCounter)
			return result


		#get successor states
		successors = action(current[0])
		
		for successor in successors:
			try:
				x = interior.index(successor)
			except:
				#each move has a cost of 1
				g = current[1] + 1
				if(not(frontier.checkFrontier(current[0]))):
					#comment out line of code according to the heuristic you wish to investigate
					
					#frontier.insert(successor, g, h1(successor, goalY), current)
					frontier.insert(successor, g, h2(successor), current) 

				interior.append(successor)
				pass


###########################################################	
# PriorityFrontier Class:	                              #
# Allows using a priority for storing 2d array states     #
# alongside it given g(n), h(n) and prioritizes them on   #
# there f(n) values. (f(n) = g(n) + h(n))			      #
###########################################################
class PriorityFrontier(object):

	#######################
	# Default Constructor #	                	              
	#######################
	def __init__(self): 
		self.queue = []


	###########################################################	
	# isEmpty Method:        	                              #
	# Returns true if the queue if empty else returns false   #
	###########################################################
	def isEmpty(self):
		if(len(self.queue) == []):
			return True
		else:
			return False

	###########################################################	
	# checkFrontier Method:        	                          #
	# Returns True if the given parameter 2d array is already #
	# present in the frontier else returns False              #   
	###########################################################
	def checkFrontier(self,matrix):
		for i in range(len(self.queue)):
			curr = self.queue[i]
			if(curr[0] == matrix):
				return True

		return False


	###########################################################	
	# insert Method:        	                              #
	# Adds a list consisting of a 2d array (state), its       #
	# g(n), h(n) and the parent state in a list based on its  #
	# f(n) (f(n) = g(n) + h(n)) value, to the list 			  #
	# (self.queue). As they are inserted based on ascending   #
	# order, it mimics a priority queue with the first element#
	# having the lowest f(n).                                 #
	###########################################################
	def insert (self, matrix, gn, hn, parent):
		fn = gn + hn 
		element = [matrix, gn, hn, fn, parent]

		i = 0
		if(len(self.queue)==0):
			self.queue.insert(0, element)
			return

		last = self.queue[len(self.queue)-1]

		if(fn > last[3]):
			self.queue.append(element)
			return

		while (i < len(self.queue)):
			var = self.queue[i]
			if(fn <= var[3]):
				self.queue.insert(i, element)
				break
			else:
				i = i + 1
		return


	###########################################################	
	# getSmallest Method:        	                          #
	# Returns and deletes the first element in the queue      #
	# which has the    										  #
	# lowest f(n) value.  									  #
	###########################################################
	def getSmallest(self):
		#when frontier is empty
		if(len(self.queue) <= 0):
			return -1
		#extract first (smallest fn) from queue
		x = self.queue[0]
		#delete first (smallest fn) from queue
		del self.queue[0]
		#return first (smallest fn) from queue
		return x


#create global frontier instance
frontier = PriorityFrontier()

aStar(input3, 0, 5, frontier)