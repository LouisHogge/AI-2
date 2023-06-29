import math
from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue, manhattanDistance


def key(state):


    """
    Returns a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """
    
    return (state.getPacmanPosition(), state.getGhostPosition(1), state.getGhostDirection(1), state.getFood(), tuple(state.getCapsules()))


def step_cost(prev_state, next_state):


    """
    Given a pacman game state, and the next one return the cost generate by steps between two position.

    Arguments:
    ----------
    - `prev_state` and 'next_state' : the current game state and the next one. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - The cost generate by steps between two position.
    """

    if prev_state.getNumFood() > next_state.getNumFood():
        return 1-5 # 1pt lose for the move but 5 pts win fot the food eaten
    else:
        return 1 # 1 pt lose for the move


def heuristic(state): 


    """
    Given a pacman game state, calculate the distance between pacman and the closest food dot.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

    Return:
    -------
    - The distance between pacman and the closest food dot.
    """

    food_grid = state.getFood()
    pacman_pos = state.getPacmanPosition()
    distances = []

    for x in range(food_grid.width):
        for y in range(food_grid.height):
            if food_grid[x][y]:
                distances.append(manhattanDistance(pacman_pos, (x, y)))

    if not distances:
        return 0
    else:
        return min(distances)


class PacmanAgent(Agent):


    def __init__(self, args):


        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """

        self.closed = set()
        self.key_val = []
        self.key_depth = []
        self.depth_max = 5


    def get_action(self, state):


        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        self.closed.clear()
        self.key_val.clear()
        self.key_depth.clear()

        minimax_move = self.minimax(state, True, 0)

        try:
            return minimax_move[1]

        except IndexError:
            return Directions.STOP

    
    def minimax (self, state, agent, depth):


        """
        Given a pacman game state, the agent and the recurion depth returns a score and the legal move related.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        - 'agent': pacman (True) or ghost (False).
        - 'depth': the recursion depth.

        Return:
        -------
        - A score and the legal move related as defined in `game.Directions`.
        """

        if state.isWin() or state.isLose() :
            return [state.getScore(), "/"]
            
        if depth >= self.depth_max and agent == True:
            return [state.getScore() - heuristic(state), "/"]
            

        current_key = key(state)
        if current_key in self.key_val:
            index = self.key_val.index(current_key)
            in_depth = self.key_depth[index]
            if in_depth > depth :
                self.key_depth[index] = depth
            else :
                if agent:
                    return [math.inf, "/"]
                else:
                    return [-math.inf, "/"]
        else:
            self.key_val.append(current_key)
            self.key_depth.append(depth)

        if agent:                           #only keep the successor that A-star define as the best
            (path,cost) = self.astar(state)
            move = path.pop(0)
            for next_state, action in state.generatePacmanSuccessors():
                if action == move :                    
                    val = self.minimax(next_state, False, depth+1)
                    val[1] = action
            return val
            
        else:
            min_val = [math.inf, "/"]
            for next_state, action in state.generateGhostSuccessors(1):
                val = self.minimax(next_state, True, depth+1)
                val[1] = action
                if val[0] < min_val[0] :
                    min_val = val
            return min_val


    def astar(self, state): 


        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions` and the costs attached to each legal move.
        """
    
        path = []
        fringe = PriorityQueue()
        fringe.push((state, path, 0.), 0.)
        closed = set() 

        while True:
            if fringe.isEmpty():
                return [] 

            _, (current, path, cost) = fringe.pop() 

            current_key = key(current)

            if current.isWin(): 
                return (path, cost) 

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    next_cost = cost + step_cost(current, next_state)
                    fringe.push((next_state, path + [action], next_cost), next_cost + heuristic(next_state)) 