#decantation problem

class Problem:

	def __init__(self):
		self.init = (8,0,0)
		self.maximum = (8,5,3)
		self.goal_states = [(4,3,1),(4,1,3),(4,4,0),(4,2,2),(3,4,1),(2,4,2),(1,4,3)]

	def isGoal(self,current_state):
		if current_state in self.goal_states:
			return True
		else:
			return False

	def findAction(self, current_state):
		actions = []
		for i in range(3):
			for j in range(3):
				if i!=j and current_state[i]>0 and current_state[j]<self.maximum[j]:
					actions.append(str(i)+"to"+str(j))
		return actions
'''
problem = Problem()
print(problem.findAction((8,0,0)))'''

class Node:

	def __init__(self,state,parent,action):
		self.state = state
		self.parent = parent
		self.action = action

	def tracePath(self):
		path = []
		actions = []
		node = self
		while( node != None):
			path.append(node.state)
			actions.append(node.action)
			node = node.parent

		path = path[::-1]
		actions = actions[::-1]
		for i in range(len(path)):
			print("State: ",path[i],"\tAction: ",actions[i])


	def next_states(self,problem):
		successors = []
		for action in problem.findAction(self.state):
			source = int(action[0])
			dest = int(action[-1])
			sState = []
			for i in range(3):
				if i==source:
					sState.append(self.state[i]-(problem.maximum[dest] - self.state[dest]))
					if sState[i]<0:
						sState[i]=0
				elif i==dest:
					sState.append(self.state[i]+self.state[source])
					if sState[i]>problem.maximum[i]:
						sState[i] = problem.maximum[i]
				else:
					sState.append(self.state[i])

			snode = Node(tuple(sState),self,action)
			successors.append(snode)
		return successors


def BFS(problem):
	root = Node(problem.init,None,None)
	frontier = []
	explored = {}

	frontier.append(root)

	while len(frontier)!=0:
		print("\n\nContents of queue: ")
		for n in frontier:
			print(n.state,end="  ")
		node = frontier.pop(0)
		explored[node.state]=1
		for successor in node.next_states(problem):
			if successor.state not in explored and successor not in frontier:
				if problem.isGoal(successor.state) == True:
					print("\n\nSequence of States and Actions to Goal State: ")
					successor.tracePath()
					print("\n\nStates explored by algorithm: ",end=" ")
					for s in explored:
						print(s,end=" ")
					print("\n\nNumber of states explored by algorithm: ",len(explored))
					return True
				frontier.append(successor)
	return False

problem = Problem()
res = BFS(problem)
if res == False:
	print("No solution found!")


'''
OUTPUT:

Contents of queue:
(8, 0, 0)

Contents of queue:
(3, 5, 0)  (5, 0, 3)

Contents of queue:
(5, 0, 3)  (0, 5, 3)  (3, 2, 3)

Contents of queue:
(0, 5, 3)  (3, 2, 3)  (0, 5, 3)  (5, 3, 0)

Contents of queue:
(3, 2, 3)  (0, 5, 3)  (5, 3, 0)

Contents of queue:
(0, 5, 3)  (5, 3, 0)  (6, 2, 0)

Contents of queue:
(5, 3, 0)  (6, 2, 0)

Contents of queue:
(6, 2, 0)  (2, 3, 3)

Contents of queue:
(2, 3, 3)  (6, 0, 2)

Contents of queue:
(6, 0, 2)  (2, 5, 1)

Contents of queue:
(2, 5, 1)  (1, 5, 2)

Contents of queue:
(1, 5, 2)  (7, 0, 1)

Sequence of States and Actions to Goal State:
State:  (8, 0, 0)       Action:  None
State:  (3, 5, 0)       Action:  0to1
State:  (3, 2, 3)       Action:  1to2
State:  (6, 2, 0)       Action:  2to0
State:  (6, 0, 2)       Action:  1to2
State:  (1, 5, 2)       Action:  0to1
State:  (1, 4, 3)       Action:  1to2


States explored by algorithm:  (8, 0, 0) (3, 5, 0) (5, 0, 3) (0, 5, 3) (3, 2, 3) (5, 3, 0) (6, 2, 0) (2, 3, 3) (6, 0, 2) (2, 5, 1) (1, 5, 2)

Number of states explored by algorithm:  11
'''