#tic tac toe using mini max algo
import math 
class TicTacToe:

	def __init__(self):
		self.initial = ((0,0,0),(0,0,0),(0,0,0))

	def player(self,state):
		x_count = 0
		o_count = 0
		for row in state:
			for move in row:
				if move == 'X':
					x_count+=1
				elif move == 'O':
					o_count+=1
		if x_count <= o_count:
			return 'X'
		else:
			return 'O'

	def actions(self,state):
		action = []
		for i in range(3):
			for j in range(3):
				if state[i][j] == 0:
					index = (i,j)
					action.append(index)
		return action

	def result(self,state,action):
		p = self.player(state)
		i = action[0]
		j = action[1]
		new_state = [list(row) for row in state]
		new_state[i][j] = p
		new_state = tuple(map(tuple, new_state))
		return new_state

	def terminal_test(self,state):
		p = self.player(state)
		p = 'X' if p == 'O' else 'O'
		for row in state:
			if row.count(p) == 3:
				return True
		for i in range(3):
			if state[i][i]!=p:
				break
		else:
			return True

		for i in range(3):
			if state[i][3-i-1] != p:
				break
		else:
			return True

		for i in range(3):
			for j in range(3):
				if state[j][i] != p:
					break
			else:
				return True

		empty = 0
		for row in state:
			empty += row.count(0)
		if empty == 0:
			return None

		return False

	def utility(self,state):
		p = self.player(state)
		p = 'X' if p == 'O' else 'O'

		term = self.terminal_test(state)

		if term == None:
			return 0
		if p == 'O':
			return -1
		else:
			return 1

class Node:
	def __init__(self,state, parent):
		self.state = state
		self.parent = parent
		self.utility = 0

	def next_states(self,problem):
		children = []
		#print(self.state)
		for action in problem.actions(self.state):
			#print(action,problem.result(self.state,action))
			child = Node(problem.result(self.state,action), self)
			children.append(child)
		return children


def alphaBetaSearch(node, problem):
	v = max_value(node, problem, -math.inf, math.inf)
	return v

def max_value(node, problem, alpha, beta):
	val = problem.terminal_test(node.state)
	if val != False:
		return problem.utility(node.state)

	v = -math.inf
	children = node.next_states(problem)
	for child in children:
		v = max(v, min_value(child, problem, alpha, beta))
		if v >= beta:
			return v
		alpha = max(alpha, v)
	return v

def min_value(node, problem, alpha, beta):
	val = problem.terminal_test(node.state)
	if val != False:
		return problem.utility(node.state)

	v = math.inf
	children = node.next_states(problem)
	for child in children:
		v = min(v, max_value(child, problem, alpha, beta))
		if v <= alpha:
			return v
		beta = min(beta, v)
	return v

def minmax_decision(node, problem):
	if problem.terminal_test(node.state) != False:
		return problem.utility(node.state)
	values = []
	for child in node.next_states(problem):
		values.append(minmax_decision(child, problem))
	if problem.player(node.state) == 'X':
		node.utility = max(values)
		return max(values)
	else:
		node.utility = min(values)
		return min(values)



p = TicTacToe()

node = Node(p.initial, None)
print("Mini-max decision result:")
print(minmax_decision(node,p))
print("Alpha-beta pruning result:")
print(alphaBetaSearch(node,p))

'''
Mini-max decision result:
0
Alpha-beta pruning result:
0
'''