class puzzleProblem:
	def __init__(self):
		self.initial = ((7, 2, 4),
					 (5, 0, 6),
					 (8, 3, 1))

		self.goal = ((0, 1, 2),
					 (3, 4, 5),
					 (6, 7, 8))

	def checkGoal(self, state):
		if state == self.goal:
			return True
		return False

	def actions(self, state):
		possible_actions = []
		# Finding index of 0 first
		for i in range(3):
			for j in range(3):
				if state[i][j] == 0:
					ind = (i,j)
					break
		# Elements to the left, right, above and below zero can occupy that index
		if(ind[0] > 0): # Element above empty position exists
			action = '(%s, %s)_to_(%s, %s)' % (ind[0]-1, ind[1], ind[0], ind[1])
			possible_actions.append(action)
		if(ind[0] < 2): # Element below empty position exists
			action = '(%s, %s)_to_(%s, %s)' % (ind[0]+1, ind[1], ind[0], ind[1])
			possible_actions.append(action)
		if(ind[1] > 0): # Element to the left of empty position exists
			action = '(%s, %s)_to_(%s, %s)' % (ind[0], ind[1]-1, ind[0], ind[1])
			possible_actions.append(action)
		if(ind[1] < 2): # Element to the right of empty position exists
			action = '(%s, %s)_to_(%s, %s)' % (ind[0], ind[1]+1, ind[0], ind[1])
			possible_actions.append(action)
		return possible_actions

class Node:
	def __init__(self, state, parent, action):
		self.state = state
		self.parent = parent
		self.action = action

	# After performing an action, the next state will basically be swap of
	# the empty space and number
	def next_states(self, problem):
		children = []
		for action in problem.actions(self.state):
			child = [[] for i in range(3)]
			for i in range(3):
				for j in range(3):
					child[i].append(self.state[i][j])
			# Swapping empty space and number indicated by action
			from_space = (int(action[1]), int(action[4]))
			to_space = (int(action[-5]), int(action[-2]))

			val1 = child[from_space[0]][from_space[1]]
			val2 = child[to_space[0]][to_space[1]]

			child[from_space[0]][from_space[1]] = val2
			child[to_space[0]][to_space[1]] = val1

			ch_node = Node(tuple(map(tuple, child)), self, action)
			children.append(ch_node)
		return children

	def displayPath(self):
		curr = self
		path = []
		while curr != None:
			path.append(curr)
			curr = curr.parent

		print("Sequence of states to reach goal: ")
		for i in range(len(path)-1, -1, -1):
			for j in range(3):
				for k in range(3):
					if(path[i].state[j][k] == 0):
						print(" ",end=' ')
						continue
					print(path[i].state[j][k], end = ' ')
				print()
			print()
		return


def DFS(problem):
	root = Node(problem.initial, None, None)
	frontier = [] #Queue
	explored = dict()

	frontier.append(root)
	while(len(frontier)!=0):
		node = frontier.pop()
		explored[node.state] = 1
		for child in node.next_states(problem):
			if(child.state not in explored and child not in frontier):
				if(problem.checkGoal(child.state)):
					child.displayPath()
					return True # Returning after first goal state is reached
				frontier.append(child)
	return False

''' Testing
print(p.actions(p.initial))

# Testing v2
parent = Node(p.initial, None, None)
for chnode in parent.next_states(p):
	print(chnode.state)'''

# Testing v3
p = puzzleProblem()
DFS(p)