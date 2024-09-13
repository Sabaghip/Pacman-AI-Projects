from Agents import Agent
import util
import random

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """
    def __init__(self, *args, **kwargs) -> None:
        self.index = 0 # your agent always has index 0

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        It takes a GameState and returns a tuple representing a position on the game board.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(self.index)

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (Game.py) and returns a number, where higher numbers are better.
        You can try and change this evaluation function if you want but it is not necessary.
        """
        nextGameState = currentGameState.generateSuccessor(self.index, action)
        return nextGameState.getScore(self.index) - currentGameState.getScore(self.index)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    Every player's score is the number of pieces they have placed on the board.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore(0)


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (Agents.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2', **kwargs):
        self.index = 0 # your agent always has index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent which extends MultiAgentSearchAgent and is supposed to be implementing a minimax tree with a certain depth.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**kwargs)

    def maxFunc(self, gamestate, agentIndex, d):
        if gamestate.isGameFinished():
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
        if gamestate.isGameFinished():
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

    def getAction(self, state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction

        But before getting your hands dirty, look at these functions:

        gameState.isGameFinished() -> bool
        gameState.getNumAgents() -> int
        gameState.generateSuccessor(agentIndex, action) -> GameState
        gameState.getLegalActions(agentIndex) -> list
        self.evaluationFunction(gameState) -> float
        """
        "*** YOUR CODE HERE ***"
        return self.maxFunc(state, 0, 0)[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning. It is very similar to the MinimaxAgent but you need to implement the alpha-beta pruning algorithm too.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**kwargs)

    def maxFunc(self, gamestate, agentIndex, d, a, b):
        if gamestate.isGameFinished():
            return ("STOP", self.evaluationFunction(gamestate))
        if gamestate.isGameFinished():
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
        if gamestate.isGameFinished():
            return ("STOP", self.evaluationFunction(gamestate))
        if gamestate.isGameFinished():
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

        You should keep track of alpha and beta in each node to be able to implement alpha-beta pruning.
        """
        "*** YOUR CODE HERE ***"
        return self.maxFunc(gameState, 0, 0, -100000, 100000)[0]
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent which has a max node for your agent but every other node is a chance node.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**kwargs)


    def maxFunc(self, gamestate, agentIndex, d):
        if gamestate.isGameFinished():
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
        if gamestate.isGameFinished():
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

        All opponents should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.maxFunc(gameState, 0, 0)[0]

def isStable(coinPosition, coins):
    flag = False
    for i in range(coinPosition[0]):
        if flag:
            break
        for j in range(8):
            if (i,j) not in coins:
                flag = True
                break
    else:
        for i in range(coinPosition[1]):
            if (coinPosition[0], i) not in coins:
                break
        else:
            return True
        for i in range(coinPosition[1],8):
            if (coinPosition[0], i) not in coins:
                break
            else:
                return True



    for i in range(coinPosition[0],8):
        if flag:
            break
        for j in range(8):
            if (i,j) not in coins:
                flag = True
                break
    else:
        for i in range(coinPosition[1]):
            if (coinPosition[0], i) not in coins:
                break
        else:
            return True
        for i in range(coinPosition[1],8):
            if (coinPosition[0], i) not in coins:
                break
            else:
                return True

    for i in range(coinPosition[1]):
        if flag:
            break
        for j in range(8):
            if (j,i) not in coins:
                flag = True
                break
    else:
        for i in range(coinPosition[0]):
            if (i, coinPosition[1]) not in coins:
                break
        else:
            return True
        for i in range(coinPosition[0],8):
            if (i, coinPosition[1]) not in coins:
                break
            else:
                return True

    for i in range(coinPosition[1], 8):
        if flag:
            break
        for j in range(8):
            if (j,i) not in coins:
                flag = True
                break
    else:
        for i in range(coinPosition[0]):
            if (i, coinPosition[1]) not in coins:
                break
        else:
            return True
        for i in range(coinPosition[0],8):
            if (i, coinPosition[1]) not in coins:
                break
            else:
                return True
    return False



def isUnstable(coinPosition, opponentCoins):
    for i in range(coinPosition[0]):
        if (i,coinPosition[1]) in opponentCoins:
            return True
        if (coinPosition[0] - i,coinPosition[1] - i) in opponentCoins:
            return True
        if (coinPosition[0] - i,coinPosition[1] + i) in opponentCoins:
            return True
        if (coinPosition[0] + i,coinPosition[1] - i) in opponentCoins:
            return True
        if (coinPosition[0] + i,coinPosition[1] + i) in opponentCoins:
            return True
    for i in range(coinPosition[0], 8):
        if (i,coinPosition[1]) in opponentCoins:
            return True
        if (coinPosition[0] - i,coinPosition[1] - i) in opponentCoins:
            return True
        if (coinPosition[0] - i,coinPosition[1] + i) in opponentCoins:
            return True
        if (coinPosition[0] + i,coinPosition[1] - i) in opponentCoins:
            return True
        if (coinPosition[0] + i,coinPosition[1] + i) in opponentCoins:
            return True

def betterEvaluationFunction(currentGameState):
    """
    Your extreme evaluation function.

    You are asked to read the following paper on othello heuristics and extend it for two to four player rollit game.
    Implementing a good stability heuristic has extra points.
    Any other brilliant ideas are also accepted. Just try and be original.

    The paper: Sannidhanam, Vaishnavi, and Muthukaruppan Annamalai. "An analysis of heuristics in othello." (2015).

    Here are also some functions you will need to use:
    
    gameState.getPieces(index) -> list
    gameState.getCorners() -> 4-tuple
    gameState.getScore() -> list
    gameState.getScore(index) -> int

    """
    
    "*** YOUR CODE HERE ***"

    # parity
    minParity = 0
    for i in range(1, currentGameState.getNumAgents()):
        minParity += currentGameState.getScore(i)
    if currentGameState.getScore(0) + minParity != 0:
        parityH = 100 * (currentGameState.getScore(0) - minParity) / (currentGameState.getScore(0) + minParity)
    else:
        parityH = 0

    # corners
    minCaughCorners = 0
    maxCaughCorners = 0
    corners = currentGameState.getCorners()
    for i in corners:
        if i==0:
            maxCaughCorners += 1
        elif i==-1:
            continue
        else:
            minCaughCorners += 1

    maxPotentialCorners = 0
    minPotentialCorners = 0
    maxUnlikelyCorners = 0
    minUnlikelyCorners = 0
    maxLegalActions = currentGameState.getLegalActions(0)
    if (0,7) in maxLegalActions:
        maxPotentialCorners += 1
    elif corners[1] != 0:
        maxUnlikelyCorners += 1
    if (0,0) in maxLegalActions:
        maxPotentialCorners += 1
    elif corners[0] != 0:
        maxUnlikelyCorners += 1
    if (7,7) in maxLegalActions:
        maxPotentialCorners += 1
    elif corners[3] != 0:
        maxUnlikelyCorners += 1
    if (7,0) in maxLegalActions:
        maxPotentialCorners += 1
    elif corners[2] != 0:
        maxUnlikelyCorners += 1

    for i in range(1, currentGameState.getNumAgents()):
        minLegalActions = currentGameState.getLegalActions(i)
        if (0,7) in minLegalActions:
            minPotentialCorners += 1
        elif corners[1] != i:
            minUnlikelyCorners += 1
        if (0,0) in minLegalActions:
            minPotentialCorners += 1
        elif corners[0] != i:
            minUnlikelyCorners += 1
        if (7,7) in minLegalActions:
            minPotentialCorners += 1
        elif corners[3] != i:
            minUnlikelyCorners += 1
        if (7,0) in minLegalActions:
            minPotentialCorners += 1
        elif corners[2] != i:
            minUnlikelyCorners += 1
    
    maxCornerValue = 4 * maxCaughCorners + maxPotentialCorners - maxUnlikelyCorners
    minCornerValue = 4 * minCaughCorners + minPotentialCorners - minUnlikelyCorners

    if maxCornerValue + minCornerValue != 0:
        cornerH = 100 * (maxCornerValue - minCornerValue) / (maxCornerValue + minCornerValue)
    else:
        cornerH = 0
    # mobility
    maxActualMobility = len(currentGameState.getLegalActions(0))
    minActualMobility = 0
    for i in range(1, currentGameState.getNumAgents()):
        minActualMobility += len(currentGameState.getLegalActions(i))

    if maxActualMobility + minActualMobility != 0:
        mobilityH = 100 * (maxActualMobility - minActualMobility) / (maxActualMobility + minActualMobility)
    else:
        mobilityH = 0
    # stability
    maxStableCoins = 0
    minStableCoins = 0
    maxUnStableCoins = 0
    minUnStableCoins = 0

    maxAllCoins = currentGameState.getPieces(0)
    minAllCoins = []
    for i in range(1, currentGameState.getNumAgents()):
        minAllCoins.extend(currentGameState.getPieces(i))
    
    for i in maxAllCoins:
        if isStable(i, maxAllCoins):
            maxStableCoins += 1
        elif isUnstable(i, minAllCoins):
            maxUnStableCoins += 1
    for i in minAllCoins:
        if isStable(i, minAllCoins):
            minStableCoins += 1
        elif isUnstable(i, maxAllCoins):
            minUnStableCoins += 1


    maxStability = maxStableCoins - maxUnStableCoins
    minStability = minStableCoins - minUnStableCoins
    if maxStability + minStability != 0:
        stabilityH = 100 * (maxStability - minStability) / (maxStability + minStability)
    else:
        stabilityH = 0

    return 2 * parityH + 4 * cornerH + 2 * mobilityH +  stabilityH
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction