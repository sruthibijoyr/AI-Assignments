class Problem:
  def __init__(self, initial):
    self. initial = initial
    self.goal = ((0,1,2,),(3,4,5),(6,7,8))
  
  def goalTest(self, state):
    if state == self.goal:
      return True
    return False

  def findEmpty(self,state):
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i][j] == 0:
          return i,j
  
  def getActions(self, state):
    actions = []
    row, col = self.findEmpty(state)
    if row != 0:
      action = "("+str(row-1)+","+str(col)+")"
      actions.append(action)
    if row != 2:
      action = "("+str(row+1)+","+str(col)+")"
      actions.append(action)
    if col != 0:
      action = "("+str(row)+","+str(col-1)+")"
      actions.append(action)
    if col != 2:
      action = "("+str(row)+","+str(col+1)+")"
      actions.append(action)

    return actions

  
class Node:
  def __init__(self, state, parent,action):
    self.state = state
    self.parent = parent
    self.action = action

  def nextStates(self, problem):
    next = []
    er, ec = problem.findEmpty(self.state)
    for action in problem.getActions(self.state):
      r = int(action[1])
      c = int(action[-2])
      new_state = list(map(list, self.state))

      new_state[er][ec] = new_state[r][c]
      new_state[r][c] = 0
      next.append(tuple(map(tuple, new_state)))
    return next

  def printSolution(self):
    node = self
    states = []
    actions = []
    while(node):
      states.append(node.state)
      actions.append(node.action)
      node = node.next
    states = states[::-1]
    actions = actions[::-1]
    for i in range(len(states)):
      for row in states[i]:
        print(row)
      print(" ")
      print(actions[i]) 
      print("\n\n")

def depthFirstSearch(problem):
  node = Node(problem.initial, None, None)
  frontier = [node]
  explored = {}
  while(len(frontier) != 0):
    node = frontier.pop()
    explored[node.state] = 1
    actions = problem.getActions(node.state)
    states = node.nextStates(problem)
    for i in range(len(actions)):
      child = Node(states[i],node, actions[i])
      if problem.goalTest(node.state):
        node.printSolution()
        return True
      if child not in frontier and child.state not in explored:
        frontier.append(child)
  return False





p = Problem(((7,2,4),(5,0,6),(8,3,1)))

res = depthFirstSearch(p)
if res == False:
  print("No solution!")  

  