#8 queens

class Problem:

	def __init__(self,initial):
		self.init = initial

	def actions(self,curr_state):
		actions = []
		for i in range(8):
			actions.append("move_queen_"+str(i))
		return actions	

	def value(self,state):
		attacks = 0
		for i in range(8):
			for j in range(i+1,8):
				r1 = i
				r2 = j
				c1 = state[i]
				c2 = state[j]

				if c1 == c2:
					attacks+=1
				if r1-c1 == r2-c2:
					attacks+=1
				if r1+c1 == r2+c2:
					attacks+=1
		return attacks

class Node:

	def __init__(self,state):
		self.state = state

	def expand(self,problem):
		children = []
		for action in problem.actions(self.state):
			queen_to_move = int(action[-1])
			for i in range(8):
				child_state = list(self.state)
				if child_state[queen_to_move] != i:
					child_state[queen_to_move] = i
					children.append(Node(tuple(child_state)))
		return children


def hillClimbing(problem):

	node = Node(problem.init)

	while True:
		children = node.expand(problem)
		if len(children) == 0:
			break
		min_child = min(children, key = lambda node: problem.value(node.state))
		if problem.value(min_child.state) >= problem.value(node.state):
			if problem.value(node.state)!=0:
				return False
			break
		node = min_child
	return node.state

def printBoard(res,initial):
	if res == False:
		print("\nSolution not found for statring configuration ",initial,". Local minima achieved.")
	else:
		print("\nSafe configuration found for starting configuration ",initial,". Solution: ",res)
		config = []
		for i in res:
			temp = []
			for j in range(8):
				if j==i:
					temp.append("Q")
				else:
					temp.append(" ")
			config.append(temp)

		for temp in config:
			print(temp)

initial = (1, 6, 6, 6, 6 ,1, 4, 2)
problem1 = Problem(initial)
res = hillClimbing(problem1)
printBoard(res,initial)

initial = (0,0,0,0,0,0,0,0)
problem2 = Problem(initial)
res = hillClimbing(problem2)
printBoard(res,initial)

'''

OUTPUT:

sruthi@LAPTOP-6GBRQ20R:/mnt/d/College/SEM 5/AI/Lab/A3$ python3 8queens.py

Safe configuration found for starting configuration  (1, 6, 6, 6, 6, 1, 4, 2) . Solution:  (5, 3, 6, 0, 7, 1, 4, 2)
[' ', ' ', ' ', ' ', ' ', 'Q', ' ', ' ']
[' ', ' ', ' ', 'Q', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', 'Q', ' ']
['Q', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Q']
[' ', 'Q', ' ', ' ', ' ', ' ', ' ', ' ']
[' ', ' ', ' ', ' ', 'Q', ' ', ' ', ' ']
[' ', ' ', 'Q', ' ', ' ', ' ', ' ', ' ']

Solution not found for statring configuration  (0, 0, 0, 0, 0, 0, 0, 0) . Local minima achieved.

'''

