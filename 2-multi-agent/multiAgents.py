# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #print(legalMoves[chosenIndex])
        #print(scores)
        #print(legalMoves)


        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print(f"{successorGameState}\n{newPos}\n{newFood}\n{newGhostStates}\n{newScaredTimes}")

        
        q = util.Queue()
        q.push(newPos)
        visited = [newPos]
        res =(-1, -1)
        while not q.isEmpty():
            x = q.pop()
            try:
                if newFood[x[0] + 1][x[1]]:
                    res = x 
                    break
                elif (x[0] + 1, x[1]) not in visited:
                    q.push((x[0] + 1, x[1]))
                    visited.append((x[0] + 1, x[1]))
            except :
                pass
            try:
                if newFood[x[0] - 1][x[1]]:
                    res = x 
                    break
                elif (x[0] - 1, x[1]) not in visited:
                    q.push((x[0] - 1, x[1]))
                    visited.append((x[0] - 1, x[1]))
            except:
                pass
            try:
                if newFood[x[0]][x[1] + 1]:
                    res = x 
                    break
                elif (x[0], x[1] + 1) not in visited:
                    q.push((x[0], x[1] + 1))
                    visited.append((x[0], x[1] + 1))
            except:
                pass
            try:
                if newFood[x[0]][x[1] - 1]:
                    res = x 
                    break
                elif (x[0] + 1, x[1] - 1) not in visited:
                    q.push((x[0], x[1] - 1))
                    visited.append((x[0], x[1] - 1))
            except :
                pass

        distanceToNearestFood = abs(newPos[0] - res[0]) + abs(newPos[1] - res[1])
        ghostsDistances = []
        for i in range(len(newGhostStates)):
            ghost = newGhostStates[i]
            ghostPosition = ghost.getPosition()
            ghostDistance = abs(newPos[0] - ghostPosition[0]) + abs(newPos[1] - ghostPosition[1])
            if newScaredTimes[i] <= ghostDistance:
                ghostsDistances.append(ghostDistance)
        distanceToNearestGhost = 0
        if len(ghostsDistances) > 0:
            distanceToNearestGhost = min(ghostsDistances)
        else:
            distanceToNearestGhost = 1000
        if distanceToNearestGhost > 5:
            distanceToNearestGhost = 1000
        
        actionPoint = 100
        if action == "STOP":
            actionPoint = 0
        

        "*** YOUR CODE HERE ***"
        return actionPoint + newFood.count(item=False) * distanceToNearestGhost  - newFood.count(item=True) * (distanceToNearestFood)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def maxFunc(self, gamestate, agentIndex, d):
        if gamestate.isWin():
            return ("STOP", self.evaluationFunction(gamestate))
        scores = []
        actions = gamestate.getLegalActions(agentIndex)
        for action in actions:
            scores.append(self.minFunc(gamestate.generateSuccessor(agentIndex, action), 1, d + 1))
        choices = [x for x in range(len(scores)) if scores[x]==max(scores)]
        try:
            chosenIndex = random.choice(choices)
            return (actions[chosenIndex], scores[chosenIndex])
        except:
            return("STOP", self.evaluationFunction(gamestate))
        


    
    def minFunc(self, gamestate, agentIndex, d):
        if gamestate.isLose():
            return self.evaluationFunction(gamestate)
        if agentIndex == gamestate.getNumAgents():
            if d == self.depth:
                return self.evaluationFunction(gamestate)
            else:
                return self.maxFunc(gamestate, 0, d)[1]
        scores = []
        actions = gamestate.getLegalActions(agentIndex)
        for action in actions:
            scores.append(self.minFunc(gamestate.generateSuccessor(agentIndex, action), agentIndex + 1, d))
        try:
            return min(scores)
        except:
            return self.evaluationFunction(gamestate)
        


    """def func(self, gameState, action):
        stateAfterPacmanPlay = gameState.generateSuccessor(0, action)
        statesAfterGhostsPlay = [stateAfterPacmanPlay]
        statesFirstIndex = 0
        if stateAfterPacmanPlay.isWin():
            return 100000
        lastGhostScores = []
        for ghostIndex in range(1, stateAfterPacmanPlay.getNumAgents()):
            lastGhostScores = []
            ghosActionsScore = []

            for _ in self.depth - 1:
                for p in range(statesFirstIndex, len(statesAfterGhostsPlay)):
                    ghostActions = statesAfterGhostsPlay[p].getLegalActions(ghostIndex)
                    for ghostActionIndex in range(len(ghostActions)):
                        statesAfterGhostsPlay.append(statesAfterGhostsPlay.generateSuccessor(ghostIndex, ghostActions[ghostActionIndex]))
                        statesFirstIndex +=1
            try:
                stateAfterPacmanPlay = stateAfterPacmanPlay.generateSuccessor(ghostIndex, ghostAction)
                lastGhostScores.append(min(ghosActionsScore))
            except:
                if len(lastGhostScores)>0:
                    lastGhostScores.append(lastGhostScores[-1])
                else:
                    lastGhostScores.append(self.evaluationFunction(gameState.generateSuccessor(0, action)))
        score = max(lastGhostScores)
        return score"""


    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        x=self.maxFunc(gameState, 0, 0)[0]
        return x
        
        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def maxFunc(self, gamestate, agentIndex, d, a, b):
        if gamestate.isWin():
            return ("STOP", self.evaluationFunction(gamestate))
        if gamestate.isLose():
            return ("STOP", self.evaluationFunction(gamestate))
        actions = gamestate.getLegalActions(agentIndex)
        v = -100000
        resAction = None
        for action in actions:
            successor = gamestate.generateSuccessor(agentIndex, action)
            v = max(v, self.minFunc(successor, 1, d + 1, a, b)[1])
            if v > b:
                return (resAction, v)
            temp = max(a, v)
            if temp != a:
                resAction = action
            a = temp
        return (resAction, v)
        

    
    def minFunc(self, gamestate, agentIndex, d, a, b):
        if gamestate.isLose():
            return ("STOP", self.evaluationFunction(gamestate))
        if gamestate.isWin():
            return ("STOP", self.evaluationFunction(gamestate))
        if agentIndex == gamestate.getNumAgents():
            if d == self.depth:
                return ("STOP", self.evaluationFunction(gamestate))
            else:
                return self.maxFunc(gamestate, 0, d, a, b)
        actions = gamestate.getLegalActions(agentIndex)
        v = 100000
        resAction = None
        for action in actions:
            successor = gamestate.generateSuccessor(agentIndex, action)
            v = min(v, self.minFunc(successor, agentIndex + 1, d, a, b)[1])
            if v < a:
                return (resAction, v)
            temp = min(b, v)
            if temp != b:
                resAction = action
            b = temp
        return (resAction, v)
            

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        x=self.maxFunc(gameState, 0, 0, -100000, 100000)[0]
        return x
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def maxFunc(self, gamestate, agentIndex, d):
        if gamestate.isWin():
            return ("STOP", self.evaluationFunction(gamestate))
        scores = []
        actions = gamestate.getLegalActions(agentIndex)
        for action in actions:
            scores.append(self.minFunc(gamestate.generateSuccessor(agentIndex, action), 1, d + 1))
        choices = [x for x in range(len(scores)) if scores[x]==max(scores)]
        try:
            chosenIndex = random.choice(choices)
            return (actions[chosenIndex], scores[chosenIndex])
        except:
            return("STOP", self.evaluationFunction(gamestate))
        


    
    def minFunc(self, gamestate, agentIndex, d):
        if gamestate.isLose():
            return self.evaluationFunction(gamestate)
        if agentIndex == gamestate.getNumAgents():
            if d == self.depth:
                return self.evaluationFunction(gamestate)
            else:
                return self.maxFunc(gamestate, 0, d)[1]
        scores = []
        actions = gamestate.getLegalActions(agentIndex)
        for action in actions:
            scores.append(self.minFunc(gamestate.generateSuccessor(agentIndex, action), agentIndex + 1, d))
        try:
            return sum(scores)/len(scores)
        except:
            return self.evaluationFunction(gamestate)

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        x=self.maxFunc(gameState, 0, 0)[0]
        return x
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    Don't forget to use pacmanPosition, foods, scaredTimers, ghostPositions!
    DESCRIPTION: <write something here so we know what you did>
    """

    pacmanPosition = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimers = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()


    q = util.Queue()
    q.push(pacmanPosition)
    visited = [pacmanPosition]
    res =(-1, -1)
    while not q.isEmpty():
        x = q.pop()
        try:
            if foods[x[0] + 1][x[1]]:
                res = x 
                break
            elif (x[0] + 1, x[1]) not in visited:
                q.push((x[0] + 1, x[1]))
                visited.append((x[0] + 1, x[1]))
        except :
            pass
        try:
            if foods[x[0] - 1][x[1]]:
                res = x 
                break
            elif (x[0] - 1, x[1]) not in visited:
                q.push((x[0] - 1, x[1]))
                visited.append((x[0] - 1, x[1]))
        except:
            pass
        try:
            if foods[x[0]][x[1] + 1]:
                res = x 
                break
            elif (x[0], x[1] + 1) not in visited:
                q.push((x[0], x[1] + 1))
                visited.append((x[0], x[1] + 1))
        except:
            pass
        try:
            if foods[x[0]][x[1] - 1]:
                res = x 
                break
            elif (x[0] + 1, x[1] - 1) not in visited:
                q.push((x[0], x[1] - 1))
                visited.append((x[0], x[1] - 1))
        except :
            pass

    distanceToNearestFood = abs(pacmanPosition[0] - res[0]) + abs(pacmanPosition[1] - res[1])


    temp = (x[0], x[1])
    q = util.Queue()
    q.push(x)
    visited = [x]
    res =(-1, -1)
    while not q.isEmpty():
        x = q.pop()
        try:
            if foods[x[0] + 1][x[1]]:
                res = x 
                break
            elif (x[0] + 1, x[1]) not in visited:
                q.push((x[0] + 1, x[1]))
                visited.append((x[0] + 1, x[1]))
        except :
            pass
        try:
            if foods[x[0] - 1][x[1]]:
                res = x 
                break
            elif (x[0] - 1, x[1]) not in visited:
                q.push((x[0] - 1, x[1]))
                visited.append((x[0] - 1, x[1]))
        except:
            pass
        try:
            if foods[x[0]][x[1] + 1]:
                res = x 
                break
            elif (x[0], x[1] + 1) not in visited:
                q.push((x[0], x[1] + 1))
                visited.append((x[0], x[1] + 1))
        except:
            pass
        try:
            if foods[x[0]][x[1] - 1]:
                res = x 
                break
            elif (x[0] + 1, x[1] - 1) not in visited:
                q.push((x[0], x[1] - 1))
                visited.append((x[0], x[1] - 1))
        except :
            pass

    distanceFromNearestFoodToNextFood = abs(temp[0] - res[0]) + abs(temp[1] - res[1])


    ghostsDistances = []
    p = 0
    for i in range(len(ghostPositions)):
        ghost = ghostStates[i]
        ghostPosition = ghost.getPosition()
        ghostDistance = abs(pacmanPosition[0] - ghostPosition[0]) + abs(pacmanPosition[1] - ghostPosition[1])
        if scaredTimers[i] <= ghostDistance:
            ghostsDistances.append(ghostDistance)
        else:
            p += 20 * ghostDistance

    distanceToNearestGhost = 0
    numberOfOs = 0
    #distanceTonearestCapsul = 0
    if len(ghostsDistances) > 0:
        distanceToNearestGhost = min(ghostsDistances)
    else:
        distanceToNearestGhost = 1000
    if distanceToNearestGhost > 5:
        distanceToNearestGhost = 1000
    else:
        numberOfOs = len(currentGameState.getCapsules())
        
    actionPoint = 100
    "*** YOUR CODE HERE ***"
    return foods.count(item=False) * distanceToNearestGhost  - foods.count(item=True) * (numberOfOs + 1) * (distanceToNearestFood + distanceFromNearestFoodToNextFood) - p


# Abbreviation
better = betterEvaluationFunction
