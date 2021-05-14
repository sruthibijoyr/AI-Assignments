import sys
from collections import deque
from copy import deepcopy
from search import Problem,Node
from time import process_time
import numpy as np
from shapely.geometry import Point, Polygon
import heapq

class PathFinder(Problem):

    def __init__(self,state,polygons, goal):
        super().__init__(state,polygons,goal)

    def actions(self, state):
        #points that you can move to from current point
        x = state[0]
        y = state[1]
        actions = []
        '''if self.checkPoint(x-1,y-1):
        	actions.append((x-1,y-1))	#top-left
        if self.checkPoint(x+1,y+1):
        	actions.append((x+1,y+1))'''	#bottom-right
        if self.checkPoint(x-1,y):
        	actions.append((x-1,y))  #left
        if self.checkPoint(x,y-1):
        	actions.append((x,y-1))  #up
        if self.checkPoint(x+1,y):
        	actions.append((x+1,y))	#right
        if self.checkPoint(x,y+1):
        	actions.append((x,y+1))	#bottom
        '''if self.checkPoint(x+1,y-1):
        	actions.append((x+1,y-1))	#top-right
        if self.checkPoint(x-1,y+1):
        	actions.append((x-1,y+1))	#bottom-left'''
        for action in actions:
        	yield action

    def checkPoint(self,x,y):
        p = Point(x,y)
        for poly in self.polygons:
            if p.within(poly):
                return False
        return True

    def result(self, state, action):
        #next state from action
        new_state = action
        return new_state

    def goal_test(self,state):
        if state == self.goal:
        	return True
        return False

    def manhattanDist(self,node):
        state = node.state
        x1 = self.goal[0]
        y1 = self.goal[1]

        x2 = state[0]
        y2 = state[1]

        manDist = abs(x1-x2) + abs(y1-y2)
        return manDist


    def Solution(self,state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                print(state[i][j],end = " ")
            print()

def breadth_first_graph_search(problem):
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = deque([node])
    explored = set()
    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    print(child.solution())
                    return child
                frontier.append(child)
    return None



def best_first_greedy_search(problem):
    node = Node(problem.initial)
    frontier = []
    explored = set()
    h = problem.manhattanDist(node)
    heapq.heappush(frontier, (h,node))
    while frontier:
        node = heapq.heappop(frontier)[1]
        if problem.goal_test(node.state):
            print(node.solution())
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                h = problem.manhattanDist(child)
                heapq.heappush(frontier, (h,child))
    return None

def astar_search(problem):
    node = Node(problem.initial)
    frontier = []
    explored = set()
    h = problem.manhattanDist(node)
    g = node.path_cost
    f = h + g
    heapq.heappush(frontier, (h,node))
    while frontier:
        node = heapq.heappop(frontier)[1]
        if problem.goal_test(node.state):
            print(node.solution())
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            h = problem.manhattanDist(child)
            g = node.path_cost+1
            f= g+h
            if child.state not in explored and child not in frontier:   
                child.path_cost = g
                heapq.heappush(frontier, (f,child))
            elif child in frontier and child.path_cost > g:
                new_child = child
                new_child.cost = g
                frontier.remove(child)
                heapq.heappush(frontier, (f,new_child))
    return None


state = (0,0)
polygons = [Polygon([(2,2),(2,4),(4,4),(4,2)])]
goal = (5,5)
problem = PathFinder(state,polygons,goal)
print("***** BFS *****")
res = breadth_first_graph_search(problem)
if res:
	print(res.state)
print("***** BFGS *****")
res = best_first_greedy_search(problem)
if res:
    print(res.state)
print("***** A Star *****")
res = astar_search(problem)
if res:
    print(res.state)

'''
OUTPUT:

***** BFS *****
[(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]
(5, 5)
***** BFGS *****
[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)]
(5, 5)
***** A Star *****
[(0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4), (4, 5), (5, 5)]
(5, 5)
'''