import math
from pacman_module.game import Agent
from pacman_module.pacman import Directions


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
    
    return (state.getPacmanPosition(), state.getGhostPosition(1), state.getFood(), tuple(state.getCapsules()))


class PacmanAgent(Agent):


    def __init__(self, args):


        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """

        self.key_val = []
        self.key_depth = []
        self.depth_max = math.inf


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
            
        if depth >= self.depth_max :
            if agent:
                return [math.inf, "/"]
            else:
                return [-math.inf, "/"]

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

        if agent:
            max_val = [-math.inf, "/"]
            for next_state, action in state.generatePacmanSuccessors():

                val = self.minimax(next_state, False, depth+1)
                val[1] = action
                if val[0] > max_val[0] :
                    max_val = val
            return max_val
            
        else:
            min_val = [math.inf, "/"]
            for next_state, action in state.generateGhostSuccessors(1):
                val = self.minimax(next_state, True, depth+1)
                val[1] = action
                if val[0] < min_val[0] :
                    min_val = val
            return min_val  