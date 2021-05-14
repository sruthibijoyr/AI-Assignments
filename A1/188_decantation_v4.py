class DecantationProblem:
	''' Problem definition:
	Initial state = (8,0,0) {Capacity: 8 l, 5 l, 3 l}
	Actions = transfer contents of 8l -> 5l, 5l -> 3l, 3l -> 8l and vice versa
	Goal states = (4,x,x) or (x,4,x) or (x,x,4)
	'''
	def __init__(self):
		self.init_state = (8,0,0)
		self.goal = [(4,1,3), (4,3,1), (1,4,3), (3,4,1),
					 (4,4,0), (4,2,2), (2,4,2)]
		self.capacity = (8,5,3)

	def actions(self, state): 
		possible_actions = []
		for i in range(3):
			for j in range(3):
				if(i != j and state[i] > 0 and state[j] < self.capacity[j]):
					action = '%s_to_%s' % (i, j)
					possible_actions.append(action)
		return possible_actions

	def checkGoal(self, state):
		if state in self.goal:
			return True
		else:
			return False

class Node:
	''' Data structure to keep track of parent.
	State, parent, action(that was applied to parent) is stored
	'''
	def __init__(self, state, parent, action):
		self.state = state
		self.parent = parent # parent will be none for initial state
		self.action = action # action will also be none for initial state

	# When this function is called for a goal state, it prints solution
	# Otherwise it prints path from initial state to that state
	def displayPath(self):
		curr = self
		path = []
		while curr != None:
			path.append(curr)
			curr = curr.parent

		print("Sequence of states to reach goal: ",self.state,'\n')
		for i in range(len(path)-1, 0, -1):
			print(path[i].state,'\n    |\n    v')
			print('',path[i-1].action,'\n    |\n    v')
		print(path[i-1].state,end='\n\n')
		return

	# Function that returns children nodes for a given node
	def next_states(self, problem):
		children = []
		for action in problem.actions(self.state):
			from_jug = int(action[0])
			to_jug = int(action[-1])
			wt = min(problem.capacity[to_jug] - self.state[to_jug], self.state[from_jug])
			child = list(self.state)
			child[from_jug] -= wt
			child[to_jug]  += wt

			ch_node = Node(tuple(child), self, action)
			children.append(ch_node)
		return children

# Breadth-First Search used to find solution sequence
def BFS(problem):
	root = Node(problem.init_state, None, None)
	frontier = [] #Queue
	explored = dict()

	frontier.append(root)
	while(len(frontier)!=0):
		node = frontier.pop(0)
		explored[node.state] = 1

		for child in node.next_states(problem):
			if(child.state not in explored and child not in frontier):
				if(problem.checkGoal(child.state)):
					child.displayPath()
					return True # Returning after first goal state is reached
				frontier.append(child)
	return False
#Note: Only one goal state's solution sequence is printed
#To get other solutions, instead of returning after first goal state is encountered continue the loop.

dp = DecantationProblem()
print("Capacity of jugs (0,1,2) = (8l, 5l, 3l)",end='\n\n')
BFS(dp)