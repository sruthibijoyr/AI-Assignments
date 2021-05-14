import sys
from collections import deque
from time import process_time
import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import random
from collections import deque
import heapq 

class PathFinder():

    def __init__(self,initial,polygons, goal):
        self.initial = initial
        self.goal = goal
        self.polygons = polygons
        self.children = self.goal_tests = self.states = 0

    def actions(self, state):
        self.children += 1
        #points that you can move to from current point
        x = state[0]
        y = state[1]
        actions = []
        if self.checkPoint(x-1,y):
        	actions.append((x-1,y))  #left
        if self.checkPoint(x,y-1):
        	actions.append((x,y-1))  #up
        if self.checkPoint(x+1,y):
        	actions.append((x+1,y))	#right
        if self.checkPoint(x,y+1):
        	actions.append((x,y+1))	#bottom
        for action in actions:
        	yield action

    def checkPoint(self,x,y):
        p = Point(x,y)
        for poly in self.polygons:
            if p.within(poly):
                return False
        return True

    def result(self, state, action):
        self.states += 1
        #next state from action
        new_state = action
        return new_state

    def goal_test(self,state):
        self.goal_tests += 1
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

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def get_stats(self):
        return self.children, self.goal_tests,self.states


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)

def memoize(fn, slot=None, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn


def plotPolygons(polygons,res,x1,y1):
    for poly in polygons:
        plt.plot(*poly.exterior.xy,color = 'red')
    plt.plot()
    x = [x1]
    y = [y1]
    if not res:
        return
    for coord in res.solution():
        x.append(coord[0])
        y.append(coord[1])
    plt.plot(x,y,color = 'green')
    plt.show()


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
                    #print(child.solution())
                    return child
                frontier.append(child)
    return None

def best_first_graph_search(problem, f):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

best_first_greedy_search = best_first_graph_search

def astar_search(problem, h=None):
    h = memoize(h or problem.manhattanDist, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


#------------------------------------------------------------------------------------------------
def Left_index(points):
    '''
    Finding the left most point
    '''
    minn = 0
    for i in range(1, len(points)):
        if points[i].x < points[minn].x:
            minn = i
        elif points[i].x == points[minn].x:
            if points[i].y > points[minn].y:
                minn = i
    return minn


def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - \
        (q.x - p.x) * (r.y - q.y)

    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def convexHull(points, n):
    # There must be at least 3 points
    if n < 3:
        return

    # Find the leftmost point
    l = Left_index(points)

    hull = []
    p = l
    q = 0
    while True:

        hull.append(p)
        q = (p + 1) % n
        for i in range(n):
            if (orientation(points[p],
                            points[i], points[q]) == 2):
                q = i
        p = q
        if p == l:
            break
    return hull

def generatePolygons():
    polygons = dict()
    points = []
    for count in range(10):
        x = random.randrange(0, 11)  
        y = random.randrange(7, 20)
        points.append(Point(x, y))
    hull = convexHull(points, 10)
    polygons['p1'] = []
    for P in hull:
        polygons['p1'].append((points[P].x, points[P].y))

    points = []
    for count in range(10):
        x = random.randrange(11, 20)
        y = random.randrange(14, 20)
        points.append(Point(x, y))
    hull = convexHull(points, 10)
    polygons['p2'] = []
    for P in hull:
        polygons['p2'].append((points[P].x, points[P].y))

    points = []
    for count in range(10):
        x = random.randrange(4, 18)
        y = random.randrange(1, 6)
        points.append(Point(x, y))
    hull = convexHull(points, 10)
    polygons['p3'] = []
    for P in hull:
        polygons['p3'].append((points[P].x, points[P].y))

    points = []
    for count in range(10):
        x = random.randrange(20, 30)
        y = random.randrange(0, 9)
        points.append(Point(x, y))
    hull = convexHull(points, 10)
    polygons['p4'] = []
    for P in hull:
        polygons['p4'].append((points[P].x, points[P].y))

    points = []
    for count in range(10):
        x = random.randrange(22, 29)
        y = random.randrange(9, 20)
        points.append(Point(x, y))
    hull = convexHull(points, 10)
    polygons['p5'] = []
    for P in hull:
        polygons['p5'].append((points[P].x, points[P].y))

    points = []
    for count in range(10):
        x = random.randrange(13, 18)
        y = random.randrange(8, 12)
        points.append(Point(x, y))
    hull = convexHull(points, 10)
    polygons['p6'] = []
    for P in hull:
        polygons['p6'].append((points[P].x, points[P].y))

    return polygons
#-----------------------------------------------------------------------------------------------

def EmpAnalysis():
    count = 0
    bfs_nodes_expanded = 0
    bfs_goal_tests = 0
    bfs_nodes_generated = 0
    bfs_time_taken = 0
    bfs_completed = 0

    bfgs_nodes_expanded = 0
    bfgs_goal_tests = 0
    bfgs_nodes_generated = 0
    bfgs_time_taken = 0
    bfgs_completed = 0

    astar_nodes_expanded = 0
    astar_goal_tests = 0
    astar_nodes_generated = 0
    astar_time_taken = 0
    astar_completed = 0

    for i in range(100):

        polys = generatePolygons()
        coords = []
        for p in polys:
            coords.append(polys[p])
        polygons = [ Polygon(coord) for coord in coords ]
        for poly in polygons:
            plt.plot(*poly.exterior.xy,color = 'red')
        plt.plot()
        print("*******************Polygon COnfiguration*********************")
        plt.show()


        while True:
            f = 0
            x1 = random.randint(0,30)
            y1 = random.randint(0,20)
            p = Point(x1,y1)
            for poly in polygons:
                if p.within(poly):
                    f = 1
                    break
            if f==0:
                break

        while True:
            f = 0
            x2 = random.randint(0,30)
            y2 = random.randint(0,20)
            p = Point(x2,y2)
            for poly in polygons:
                if p.within(poly):
                    f = 1
                    break
            if f==0:
                break

            
        state = (x1,y1)
        goal = (x2,y2)

        print("Start state: ",state,"\tGoal state: ",goal)

        p = PathFinder(state,polygons,goal)

        print("*******************BFS******************")
        start = process_time()
        solution = breadth_first_graph_search(p)
        plotPolygons(polygons, solution,state[0],state[1])
        stop = process_time()
        x,y,z = p.get_stats()
        bfs_nodes_expanded+=x
        bfs_goal_tests+=y
        bfs_nodes_generated+=z
        bfs_time_taken+=(stop - start)
        if solution:
            bfs_completed += 1
        #print("completed bfs")

        print("*******************BFGS******************")
        start = process_time()
        solution = best_first_greedy_search(p,p.manhattanDist)
        plotPolygons(polygons, solution,state[0],state[1])
        stop = process_time()
        x,y,z = p.get_stats()
        bfgs_nodes_expanded+=x
        bfgs_goal_tests+=y
        bfgs_nodes_generated+=z
        bfgs_time_taken+=(stop - start)
        if solution:
            bfgs_completed += 1
        #print("completed bfgs")

        print("*******************A Star******************")
        start = process_time()
        solution = astar_search(p)
        plotPolygons(polygons, solution,state[0],state[1])
        stop = process_time()
        x,y,z = p.get_stats()
        astar_nodes_expanded+=x
        astar_goal_tests+=y
        astar_nodes_generated+=z
        astar_time_taken+=(stop - start)
        if solution:
            astar_completed += 1
        #print("completed astar")

        count+=1



    bfs_nodes_expanded/=count
    bfs_completed/=count
    bfs_nodes_generated/=count
    bfs_time_taken/=count

    bfgs_nodes_expanded/=count
    bfgs_completed/=count
    bfgs_nodes_generated/=count
    bfgs_time_taken/=count

    astar_nodes_expanded/=count
    astar_completed/=count
    astar_nodes_generated/=count
    astar_time_taken/=count


    print("\n\n******************\tBFS\t******************")
    print("Average time taken: ",bfs_time_taken)
    print("Average nodes generated: ",bfs_nodes_generated)
    print("Average nodes expanded: ",bfs_nodes_expanded)
    print("Precentage of completed instances: ",bfs_completed*100)

    print("\n\n******************\tBFGS\t******************")
    print("Average time taken: ",bfgs_time_taken)
    print("Average nodes generated: ",bfgs_nodes_generated)
    print("Average nodes expanded: ",bfgs_nodes_expanded)
    print("Precentage of completed instances: ",bfgs_completed*100)

    print("\n\n******************\tA STAR\t******************")
    print("Average time taken: ",astar_time_taken)
    print("Average nodes generated: ",astar_nodes_generated)
    print("Average nodes expanded: ",astar_nodes_expanded)
    print("Precentage of completed instances: ",astar_completed*100)


EmpAnalysis()

'''

******************      BFS     ******************
Average time taken:  0.24375
Average nodes generated:  3521.2
Average nodes expanded:  905.0
Precentage of completed instances:  100.0


******************      BFGS    ******************
Average time taken:  0.01875
Average nodes generated:  3615.8
Average nodes expanded:  932.4
Precentage of completed instances:  100.0


******************      A STAR  ******************
Average time taken:  0.040625
Average nodes generated:  3906.8
Average nodes expanded:  1012.0
Precentage of completed instances:  100.0
'''