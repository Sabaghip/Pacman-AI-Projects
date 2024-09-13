# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    visited = []
    stack = util.Stack()
    stack.push((problem.getStartState(),"nn", 0))
    stackRoute = util.Stack()
    stackRoute.push([])


    while not stack.isEmpty():
        temp = stack.pop()
        temp = temp[0]
        visited.append(temp)
        
        if problem.isGoalState(temp):
            return stackRoute.pop()
        routeTemp = stackRoute.pop()
        for neighbor in problem.getSuccessors(temp):
            if neighbor[0] not in visited:
                stack.push(neighbor)
                stackRoute.push(routeTemp + [neighbor[1]])
    return []
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    visited = [problem.getStartState()]
    q = util.Queue()
    q.push((problem.getStartState(),"nn", 0))
    qForRouts = util.Queue()
    qForRouts.push([])

    while not q.isEmpty():
        temp = q.pop()
        temp = temp[0]
        
        if problem.isGoalState(temp):
            res = qForRouts.pop()
            return res
        routeTemp = qForRouts.pop()
        for neighbor in problem.getSuccessors(temp):
            if neighbor[0] not in visited:
                visited.append(neighbor[0])
                q.push(neighbor)
                action = neighbor[1]
                qForRouts.push(routeTemp + [action])
        
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    visited = []
    q = util.PriorityQueue()
    fring = [(problem.getStartState(), 0, [])]
    q.push(problem.getStartState(), 0)

    while not q.isEmpty():
        temp = q.pop()
        visited.append(temp)
        temp1 = [x for x in fring if x[0] == temp][0]
        cost = temp1[1]
        tempRout = temp1[2]

        if problem.isGoalState(temp):
            return tempRout
        fring = [x for x in fring if x[0] != temp]
        for neighbor in problem.getSuccessors(temp):
            if neighbor[0] not in visited:
                q.update(neighbor[0], neighbor[2] + cost)
                action = neighbor[1]
                for i in fring:
                    if i[0] == neighbor[0]:
                        if i[1] > neighbor[2] + cost:
                            fring.remove(i)
                            fring.append((neighbor[0], neighbor[2] + cost, tempRout + [action]))
                        break
                else:
                    fring.append((neighbor[0], neighbor[2] + cost, tempRout + [action]))
                
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    visited = []
    q = util.PriorityQueue()
    fring = [(problem.getStartState(), 0, [])]
    q.push(problem.getStartState(), 0)
    while not q.isEmpty():
        temp = q.pop()
        visited.append(temp)
        temp1 = [x for x in fring if x[0] == temp][0]
        cost = temp1[1]
        tempRout = temp1[2]
        
        if problem.isGoalState(temp):
            return tempRout
        fring = [x for x in fring if x[0] != temp]
        for neighbor in problem.getSuccessors(temp):
            if neighbor[0] not in visited:
                h = heuristic(neighbor[0], problem)
                q.update(neighbor[0], neighbor[2] + cost + h)
                action = neighbor[1]
                for i in fring:
                    if i[0] == neighbor[0]:
                        if i[1] > neighbor[2] + cost:
                            fring.remove(i)
                            fring.append((neighbor[0], neighbor[2] + cost, tempRout + [action]))
                        break
                else:
                    fring.append((neighbor[0], neighbor[2] + cost, tempRout + [action]))
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
