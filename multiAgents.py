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
import sys

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

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

        "*** YOUR CODE HERE ***"
        if successorGameState.isWin():
            #prefere ganhar a fazer qualquer outra coisa como pegar a capsula que assuta os fantasmas
            return float("inf")
        ghost_position = currentGameState.getGhostPosition(1)
        ghost_distance = util.manhattanDistance(ghost_position, newPos)
        score = ghost_distance + successorGameState.getScore()
        food_list = newFood.asList()
        closest_food = float ("inf")
        #favorece a comida mais proxima
        for foodpos in food_list:
            food_distance = util.manhattanDistance(foodpos, newPos)
            if (food_distance < closest_food):
                 closest_food = food_distance
        #da preferencia para estados que melhorem a pontuacao
        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 120
        #prefere nao ficar parado
        if action == Directions.STOP:
            score -= 3
        score -= 3 * closest_food
        capsuleplaces = currentGameState.getCapsules()
        if successorGameState.getPacmanPosition() in capsuleplaces:
            score += 140
        return score


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
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

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
      Your minimax agent (question 7)
    """

    def getAction(self, actualGameState):
        a = self.doMax(actualGameState, 0)
        return a[1]

    def doMax(self, actualGameState, depth):
        if depth == self.depth:
            return (self.evaluationFunction(actualGameState), None)

        possibleActions = actualGameState.getLegalActions(0)
        bestScore = -sys.maxint
        bestAction = None

        if len(possibleActions) == 0:
            return (self.evaluationFunction(actualGameState), None)

        for action in possibleActions:
            nextState = actualGameState.generateSuccessor(0, action)
            nextScore = self.doMin(nextState, 1, depth)[0]

            if (nextScore > bestScore):
                bestScore, bestAction = nextScore, action

        return (bestScore, bestAction)

    def doMin(self, actualGameState, index, depth):
        possibleActions = actualGameState.getLegalActions(index)
        bestScore = sys.maxint
        bestAction = None

        if len(possibleActions) == 0:
            return (self.evaluationFunction(actualGameState), None)

        for action in possibleActions:
            nextState = actualGameState.generateSuccessor(index, action)
            a = actualGameState.getNumAgents()

            if (index == actualGameState.getNumAgents() - 1):
                nextScore = self.doMax(nextState, depth + 1)[0]
            else:
                nextScore = self.doMin(nextState, index + 1, depth)[0]

            if (nextScore < bestScore):
                bestScore, bestAction = nextScore, action

        return (bestScore, bestAction)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

