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
import sys
import copy


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

    def goalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """
        util.raiseNotDefined()

    def getResult(self, state, action):
        """
        Given a state and an action, returns resulting state.
        """
        util.raiseNotDefined()

    def getCost(self, state, action):
        """
        Given a state and an action, returns step cost, which is the incremental cost 
        of moving to that successor.
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
    return [s, s, w, s, w, w, s, w]


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"

    max_depth = 0

    actualState = problem.getStartState()

    while True:
        path = util.Queue()
        visitedStates = util.Queue()
        close_nodes = util.Stack()

        found = iterative_recursive_deepening(actualState, max_depth, problem, path, visitedStates, close_nodes)

        if found:
            return path.list

        max_depth += 1


def iterative_recursive_deepening(actual_state, max_depth, problem, path, visitedStates, close_nodes):

    visitedStates.push(actual_state)

    if problem.goalTest(actual_state):
        return True
    elif max_depth > 0:
        actions = util.Queue()

        for action in problem.getActions(actual_state):
            child = problem.getResult(actual_state, action)
            actions.push(action)
            close_nodes.push(child)

        for action in actions.list:
            child = close_nodes.pop()
            if child not in visitedStates.list and child not in close_nodes.list:
                found = iterative_recursive_deepening(child, max_depth - 1, problem, path, visitedStates, close_nodes)
                if found:
                    path.push(action)
                    return True
    return False


def aStarSearch(problem, heuristic=nullHeuristic):
    actual_state = problem.getStartState()
    possible_actions = util.PriorityQueue()

    actual_state_cost = heuristic(actual_state, problem)

    path = []
    visited_nodes = util.Queue()
    visited_nodes.push(actual_state)

    path = recursive_a_star_search(problem, actual_state, possible_actions, actual_state_cost, heuristic, path, visited_nodes)

    return path


def recursive_a_star_search(problem, actual_state, possible_actions, actual_state_cost, heuristic, path, visited_nodes):

    while True:
        if problem.goalTest(actual_state):
            return path

        actions = problem.getActions(actual_state)

        for action in actions:
            new_path = copy.copy(path)
            new_path.append(action)
            resulting_state = problem.getResult(actual_state, action)
            action_cost = calculate_cost(actual_state, action, resulting_state, problem, actual_state_cost - heuristic(actual_state, problem), heuristic)
            possible_actions.push((resulting_state, action_cost, new_path), action_cost)

        new_node_found = False
        while not new_node_found:

            if possible_actions.isEmpty():
                return False

            (actual_state, actual_state_cost, path) = possible_actions.pop()

            if actual_state not in visited_nodes.list:
                visited_nodes.push(actual_state)
                new_node_found = True

        #path = recursive_a_star_search(problem, actual_state, possible_actions, actual_state_cost, heuristic, path, visited_nodes)

    # if path:
    #     return path



def calculate_cost(actual_state, action, resulting_state, problem, cost_so_far, heuristic):

    cost = problem.getCost(actual_state, action)

    if cost:
        return heuristic(resulting_state, problem) + cost + cost_so_far
    else:
        return heuristic(resulting_state, problem) + cost_so_far


# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
