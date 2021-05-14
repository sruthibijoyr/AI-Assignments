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
					actions.append(str(self.maximum[i])+"to"+str(self.maximum[j]))
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
		node = self
		while( node != None):
			path.append(node)
			node = node.parent

		path = path[::-1]
		print(path)