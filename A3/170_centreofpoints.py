#center for a set of problem

class Problem:

	def __init__(self):
		self.init = (5,4)
		self.points = [(1,7),(2,3),(4,2),(7,1),(9,4)]

	def findActions(self,curr_state):
		actions = ['move_left','move_right','move_up','move_down']
		return actions

	def manDistance(self,state):
		md = 0
		for point in self.points:
			md += abs(state[0]-point[0]) + abs(state[1]-point[1])
		return md
		

class Node:

	def __init__(self,state):
		self.state = state

	def next_states(self,problem):
		successors = []
		for action in problem.findActions(self.state):
			if action == 'move_left':
				point = (self.state[0] - 1, self.state[1])
			elif action == 'move_right':
				point = (self.state[0] + 1, self.state[1])
			elif action == 'move_up':
				point = (self.state[0], self.state[1] + 1)
			elif action == 'move_down':
				point = (self.state[0], self.state[1] - 1)
			successors.append(Node(point))
		return successors

def hillClimbing(problem):
	node = Node(problem.init)
	while(True):
		print(node.state)
		successors = node.next_states(problem)
		if len(successors) == 0:
			break
		least_successor = min(successors, key = lambda node: problem.manDistance(node.state))
		if problem.manDistance(least_successor.state) >= problem.manDistance(node.state):
			break
		node = least_successor
	return node.state

problem = Problem()
res = hillClimbing(problem)
print("\nCentre of points ",problem.points," :",res)

'''
OUTPUT:

(5, 4)
(4, 4)
(4, 3)

Centre of points  [(1, 7), (2, 3), (4, 2), (7, 1), (9, 4)]  : (4, 3)
'''