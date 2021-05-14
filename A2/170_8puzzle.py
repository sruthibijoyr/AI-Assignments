
import heapq

class Problem:
	def __init__(self):
		self.init = ((7,2,4),(5,0,6),(8,3,1))
		self.goal_state = ((0,1,2),(3,4,5),(6,7,8))

	def isGoal(self,curr_state):
		if curr_state ==self.goal_state:
			return True
		else:
			return False

	def findActions(self, curr_state):
		actions = []
		flag=0
		for i in range(3):
			for j in range(3):
				if curr_state[i][j] == 0:
					flag=1
					break
			if flag==1:
				break
		if i!=0:
			actions.append("move("+str(i-1)+","+str(j)+")")
		if i!=2:
			actions.append("move("+str(i+1)+","+str(j)+")")
		if j!=0:
			actions.append("move("+str(i)+","+str(j-1)+")")
		if j!=2:
			actions.append("move("+str(i)+","+str(j+1)+")")
		return actions


class Node:
	def __init__(self,state,parent,action,cost):
		self.state = state
		self.parent = parent
		self.action = action
		self.cost = cost

	def __lt__(self,node):
		return self.state < node.state
        
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
			if actions[i]!=None:
				print("\n\nAction: "+actions[i])
			print("State:")
			for state in path[i]:
				print(state)

	def next_states(self,problem):
		successors = []
		#print(self.state)
		flag=0
		for i in range(3):
			for j in range(3):
				if self.state[i][j] == 0:
					flag=1
					break
			if flag==1:
				break
		empty_i,empty_j = i,j
		for action in problem.findActions(self.state):
			i = int(action[5])
			j = int(action[7])
			sState = []
			for t in self.state:
				sState.append(list(t))
			sState[empty_i][empty_j] ,sState[i][j] = sState[i][j],sState[empty_i][empty_j]
			snode = Node(tuple(map(tuple,sState)),self,action,None)
			successors.append(snode)
		return successors

def manhattanDist(node):
	state = node.state
	manDist = 0
	for x1 in range(3):
		for y1 in range(3):
			x2 = state[x1][y1]//3
			y2 = state[x1][y1]%3
			manDist += abs(x1-x2) + abs(y1-y2)
	return manDist


#Uninformed search strategy
def DFS(problem):
	root = Node(problem.init, None, None,None)
	frontier = [] 
	explored = {}
	frontier.append(root)
	while len(frontier)!=0:
		node = frontier.pop()
		explored[node.state] = 1
		for successor in node.next_states(problem):
			if successor.state not in explored and successor not in frontier:
				if problem.isGoal(successor.state) == True:
					print("Sequence of States and Actions to Goal State:\n")
					successor.tracePath()
					return True
				frontier.append(successor)
	return False



#Greedy BFS
def GBFS(problem):
	root = Node(problem.init,None,None,None)
	frontier = [] #priority queue
	explored = {}
	h = manhattanDist(root)
	heapq.heappush(frontier, (h,root))
	while len(frontier)!=0:
		node = heapq.heappop(frontier)[1]
		explored[node.state] = 1
		if problem.isGoal(node.state) == True:
			print("Sequence of States and Actions to Goal State:\n")
			node.tracePath()
			return True
		for successor in node.next_states(problem):
			if successor.state not in explored and successor not in frontier:
				h = manhattanDist(successor)
				heapq.heappush(frontier, (h,successor))
	return False


def AStar(problem):
	root = Node(problem.init,None,None,0)
	frontier = [] #priority queue
	explored = {}
	h = manhattanDist(root)
	g = root.cost
	f = h + g
	heapq.heappush(frontier, (f,root))
	while len(frontier)!=0:
		node = heapq.heappop(frontier)[1]
		explored[node.state] = 1
		if problem.isGoal(node.state) == True:
			print("Sequence of States and Actions to Goal State:\n")
			node.tracePath()
			return True
		for successor in node.next_states(problem):
			h = manhattanDist(successor)
			g = node.cost + 1
			f = g+h
			if successor.state not in explored and successor not in frontier:	
				successor.cost = g
				heapq.heappush(frontier, (f,successor))
			elif successor in frontier and successor.cost > g:
				new_successor = successor
				new_successor.cost = g
				frontier.remove(successor)
				heapq.heappush(frontier, (f,new_successor))

	return False



problem = Problem()

print("\n\n\t\t\t\t\tDepth First Search\n")
res = DFS(problem)
if res == False:
	print("No solution found!")

print("\n\n\t\t\t\t\tGreedy Best First Search\n")
res = GBFS(problem)
if res == False:
	print("No solution found!")

print("\n\n\t\t\t\t\tA* Search\n")
res = AStar(problem)
if res == False:
	print("No solution found!")