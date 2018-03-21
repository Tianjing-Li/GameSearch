import operator
from copy import deepcopy

# Search Tree for board states, contains a list of search nodes
class searchTree:

	def __init__(self, initial):
		self.head = self.searchNode(state=initial)

	def createSearchNode(self, state, parent, operator, cost, depth):
		newNode = self.searchNode(state, parent, operator, cost, depth)
		return newNode

	class searchNode:
		def __init__(self, state=None, parent=None, operator=0, cost=0, depth=0):
			self.state = state 
			self.parent = parent
			self.operator = operator
			self.cost = cost
			self.depth = depth

# Board States, containing board state and board information for manipulation
class boardState:
	def __init__(self, board=[[1, 4, 2],[5, 3, 0]]):
		self.board = board
		self.zeroLocation = self.getZeroLocation()
		self.operators = self.getOperators()
		self.sortedOperators = self.sortOperators()

	def getZeroLocation(self):
		board = self.board
		i = j = 0

		# find where 0 is located (the empty slot)
		for row_num, row in enumerate(board):
			for col_num, num in enumerate(row):
				if num == 0:
					i = row_num
					j = col_num
					break

		return (i, j)

	# finds states that can be reached from current one
	# operators:
	# 1 : up
	# 2 : down
	# 3 : left
	# 4 : right
	def getOperators(self):
		(i, j) = self.zeroLocation
		operators = []

		if i == 0:
			operators.append(1)
		else:
			operators.append(2)
		if j == 0:
			operators.append(3)
		elif j == 1:
			operators.append(3)
			operators.append(4)
		elif j == 2:
			operators.append(4)

		return operators

	# sorts operators based on piece number (ascending order)
	def sortOperators(self):
		mapping = {}
		board = self.board
		ops = self.operators
		(i, j) = self.zeroLocation

		for op in ops:
			if op == 1:
				mapping[op] = board[i+1][j]
			elif op == 2:
				mapping[op] = board[i-1][j]
			elif op == 3:
				mapping[op] = board[i][j+1]
			elif op == 4:
				mapping[op] = board[i][j-1]

		# sort mapping by value, then append keys to new list
		sorted_mapping = sorted(mapping.items(), key=operator.itemgetter(1), reverse = False)
		sorted_operators = [pair[0] for pair in sorted_mapping]
		return sorted_operators

# -----------------------------------------------------------------------------------------------
									  #Main Functions 
# -----------------------------------------------------------------------------------------------

# given a valid operator from 1-4
# perform move and return new state
def moveState(state, operator):
	if operator < 1 or operator > 4 or operator not in state.operators:
		print "Invalid operator, returning board unchanged"
		return state

	board = deepcopy(state.board) # current board location
	(i, j) = state.zeroLocation # current location of 0 (empty)

	if operator == 1: # move piece up
		board[i][j], board[i+1][j] = board[i+1][j], 0
	elif operator == 2: # move piece down
		board[i][j], board[i-1][j] = board[i-1][j], 0
	elif operator == 3: # move piece left
		board[i][j], board[i][j+1] = board[i][j+1], 0
	elif operator == 4: # move piece right
		board[i][j], board[i][j-1] = board[i][j-1], 0

	new = boardState(board)
	return new

def isSameState(state1, state2):
	board1 = state1.board 
	board2 = state2.board 

	for i in range(len(board1)):
		for j in range(len(board1[0])):
			if board1[i][j] != board2[i][j]:
				return False 

	return True

def isSeenState(states_seen, state):
	for to_compare in states_seen:
		if isSameState(to_compare, state):
			return True 

	return False

def printState(state):
	board = state.board 

	for i in range(len(board)):
		print board[i]

def printPath(end_node):
	current_node = end_node
	state_list = []

	while current_node is not None:
		state = current_node.state 
		state_list.append(state) # add current state to stack
		current_node = current_node.parent

	index = 0 
	while state_list:
		print "STATE " + str(index) + ":"
		index = index + 1

		current_state = state_list.pop()
		printState(current_state)


def BFS(initial, goal):
	seen = []
	st = searchTree(initial) # initialize search tree with initial board state as head
	queue = [st.head]		 # add head to queue start
	count = 0

	while queue:
		current_node = queue.pop(0) # remove from end of queue (left pop)
		current_state = current_node.state 

		if isSameState(current_state, goal): # check if we've reached goal
			print "Goal Reached: BFS"
			return current_node

		#print current_state.board

		seen.append(current_state) # list of board states already seen
		sorted_operators = current_state.sortedOperators # get list of possible operators

		for op in sorted_operators: # operators sorted from smallest tile number
			new_state = moveState(current_state, op)

			if not isSeenState(seen, new_state): # if we have yet to see the state
				# create new search tree node with new board state, which is a child of the current node
				new_node = st.createSearchNode(state=new_state, parent=current_node, 
					operator=op, cost=current_node.cost+1, depth=current_node.depth+1)
				queue.append(new_node)

	print "End of Queue reached"

# Use priority queues to run BFS but taking into account lower cost paths
def uniformCost(initial, goal):
	seen = []
	st = searchTree(initial)	# initialize search tree with initial board state as head
	priority_queue = [st.head]  			# add head to queue start

	while priority_queue:
		current_node = priority_queue.pop(0) # remove highest priority (lowest cost)
		current_state = current_node.state

		if isSameState(current_state, goal):
			print "Goal Reached: Uniform Cost"
			return current_node 

		seen.append(current_state)
		sorted_operators = current_state.sortedOperators

		for op in sorted_operators: # operators sorted from smallest tile number
			new_state = moveState(current_state, op)

			if not isSeenState(seen, new_state): # if we have yet to see the state
				# create new search tree node with new board state, which is a child of the current node
				new_node = st.createSearchNode(state=new_state, parent=current_node, 
					operator=op, cost=current_node.cost+1, depth=current_node.depth+1)
				priority_queue.append(new_node)

		# sort priority_queue by priority for next iteration
		priority_queue.sort(key=operator.attrgetter("cost"))
	
def DFS(initial, goal):
	seen = []
	st = searchTree(initial)
	stack = [st.head]

	while stack:
		current_node = stack.pop()
		current_state = current_node.state

		if isSameState(current_state, goal):
			print "Goal Reached: DFS"
			return current_node

		seen.append(current_state)
		sorted_operators = current_state.sortedOperators 

		for op in sorted_operators[::-1]: # iterate through list BACKWARDS (so smallest tile at top)
			new_state = moveState(current_state, op)

			if not isSeenState(seen, new_state):
				# create new search tree node with new board state, which is a child of the current node
				new_node = st.createSearchNode(state=new_state, parent=current_node, 
					operator=op, cost=current_node.cost+1, depth=current_node.depth+1)
				stack.append(new_node)

	print "End of stack reached"

def iterativeDeepening(initial, goal):
	st = searchTree(initial)
	current_max_depth = 0
	step_size = 1

	while True:
		stack = [st.head]
		seen = []
		while stack:
			current_node = stack.pop()

			if current_node.depth > current_max_depth:
				continue

			current_state = current_node.state

			if isSameState(current_state, goal):
				print "Goal Reached: Iterative Deepening"
				return current_node

			seen.append(current_state)
			sorted_operators = current_state.sortedOperators 

			for op in sorted_operators[::-1]: # iterate through list BACKWARDS (so smallest tile at top)
				new_state = moveState(current_state, op)

				if not isSeenState(seen, new_state):
					# create new search tree node with new board state, which is a child of the current node
					new_node = st.createSearchNode(state=new_state, parent=current_node, 
						operator=op, cost=current_node.cost+1, depth=current_node.depth+1)
					stack.append(new_node)

		current_max_depth = current_max_depth + step_size
		print "End of stack reached: max_depth = " + str(current_max_depth)


def main():
	init = boardState()
	goal = boardState([[0,1,2],[5,4,3]])
	
	#end_node = BFS(init, goal)

	#end_node = DFS(init, goal)

	end_node = iterativeDeepening(init, goal)

	printPath(end_node)



	#printPath(end_node)

	#print goal_node.parent.state.board
	#print st.head.state.operators



if __name__ == "__main__":
	main()


