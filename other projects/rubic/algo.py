import numpy as np
from state import next_state, solved_state
from location import next_location
from collections import OrderedDict
import util


def solve(init_state, init_location, method):
    """
    Solves the given Rubik's cube using the selected search algorithm.
 
    Args:
        init_state (numpy.array): Initial state of the Rubik's cube.
        init_location (numpy.array): Initial location of the little cubes.
        method (str): Name of the search algorithm.
 
    Returns:
        list: The sequence of actions needed to solve the Rubik's cube.
    """

    # instructions and hints:
    # 1. use 'solved_state()' to obtain the goal state.
    # 2. use 'next_state()' to obtain the next state when taking an action .
    # 3. use 'next_location()' to obtain the next location of the little cubes when taking an action.
    # 4. you can use 'Set', 'Dictionary', 'OrderedDict', and 'heapq' as efficient data structures.

    if method == 'Random':
        return list(np.random.randint(1, 12+1, 10))
    
    elif method == 'IDS-DFS':
        res = id_dfs1(init_state, 15)
        print("explored = ", res[1], " expand = ",res[2]," depth = ", res[3])
        return res[0]
    
    elif method == 'A*':
        res = a_star_search(init_location, init_state)
        print("explored = ", res[1], "  expanded = ", res[2])
        return res[0]

    elif method == 'BiBFS':
        res = biBFS(init_state)
        print("explored = ", res[1], "  expanded = ", res[2])
        return res[0]
    
    else:
        return []

def id_dfs1(init_state,limit):
    explored = 0
    expand = 0
    depth = -1
    for i in range(limit):
        print(i)
        depth += 1
        stack = util.Stack()
        stack.push((init_state,[], 0))
        stackRoute = util.Stack()
        stackRoute.push([])
        while not stack.isEmpty():
            explored += 1
            temp = stack.pop()
            temp = temp[0]
            if (temp == solved_state()).all():
                return stackRoute.pop(),depth,expand,explored
            routeTemp = stackRoute.pop()
            if len(routeTemp) >= i:
                continue
            for j in range(1,13):
                expand += 1
                neighbor = next_state(temp, j)
                stack.push((neighbor,routeTemp + [j], 0))
                stackRoute.push(routeTemp + [j])                          
            

def heuristic(location):
    sum = 0
    for i in range(2):
        for j in range(2):
            for k in range(2):
                k1 = (location[i][j][k] - 1) % 2
                j1 = int(((location[i][j][k] - 1)/2)) % 2
                i1 = int(((location[i][j][k] - 1)/4)) % 2
                sum += abs(i - i1) + abs(j - j1) + abs(k - k1)
    return sum/4.0

def a_star_search(start, sstate):
    frontier = util.PriorityQueue()
    frontier.push((start, heuristic(start), [], sstate), heuristic(start))
    cost_so_far = {}
    cost_so_far[repr(sstate.tolist())] = 0
    visited = set()
    explored = 0
    expanded = 0
    while not frontier.isEmpty():
        current = frontier.pop()
        expanded += 1
        visited.add(repr(current[3].tolist()))
        if (current[3] == solved_state()).all():
            return current[2], explored, expanded
        
        for i in range(1, 13):
            next = next_location(current[0], i)
            nstate = next_state(current[3], i)
            new_cost = cost_so_far[repr(current[3].tolist())] + 1
            if repr(nstate.tolist()) not in cost_so_far:
                explored += 1
                cost_so_far[repr(nstate.tolist())] = new_cost
                priority = new_cost + heuristic(next)
                frontier.push((next,priority, current[2] + [i], nstate), priority)
            elif new_cost < cost_so_far[repr(nstate.tolist())]:
                cost_so_far[repr(nstate.tolist())] = new_cost
                priority = new_cost + heuristic(next)
                frontier.push((next,priority, current[2] + [i], nstate), priority)

def biBFS(start):
    goal = solved_state()
    forwardVisited = set()
    backwardVisited = set()
    forwardAll = set()
    backwardAll = set()
    forwardAll.add(repr(start.tolist()))
    backwardAll.add(repr(goal.tolist()))
    forwardAllRoute = {}
    backwardAllRoute = {}
    forwardAllRoute[repr(start.tolist())] = []
    backwardAllRoute[repr(goal.tolist())] = []
    forward1 = util.Queue()
    backward1 = util.Queue()
    forward1.push((start, []))
    backward1.push((goal, []))
    forward2 = util.Queue()
    backward2 = util.Queue()
    expand = 0
    explore = 0 
    while True:
        while not forward1.isEmpty():
            explore += 1
            temp = forward1.pop()
            if not repr(temp[0].tolist()) in forwardVisited:
                forwardVisited.add(repr(temp[0].tolist()))
                for i in range(1,13):
                    expand += 1
                    next = next_state(temp[0], i)
                    if repr(next.tolist()) in backwardAll:
                        z = []
                        for k in backwardAllRoute[repr(next.tolist())]:
                            if k == 6:
                                z.append(12)
                            else:
                                z.append((k + 6 ) % 12)
                        return temp[1] + [i] + z, explore, expand
                    forward2.push((next, temp[1] + [i]))
                    forwardAll.add(repr(next.tolist()))
                    forwardAllRoute[repr(next.tolist())] = temp[1] + [i]
        while not backward1.isEmpty():
            explore += 1
            temp = backward1.pop()
            if not repr(temp[0].tolist()) in backwardVisited:
                backwardVisited.add(repr(temp[0].tolist()))
                for i in range(1,13):
                    expand += 1
                    next = next_state(temp[0], i)
                    if repr(next.tolist()) in forwardAll:
                        z = []
                        for k in temp[1]:
                            if k == 6:
                                z.append(12)
                            else:
                                z.append((k + 6 ) % 12 )
                        if i == 6:
                            i=12
                        else:
                            i = (i + 6 ) % 12 
                        return forwardAllRoute[repr(next.tolist())] + [i] + z, explore, expand
                    backward2.push((next, [i] + temp[1]))
                    backwardAll.add(repr(next.tolist()))
                    backwardAllRoute[repr(next.tolist())] = [i] + temp[1]
        while not forward2.isEmpty():
            forward1.push(forward2.pop())
        while not backward2.isEmpty():
            backward1.push(backward2.pop())