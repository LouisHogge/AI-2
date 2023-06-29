import math
from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance


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


class PacmanAgent(Agent):


    def __init__(self, args):


        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.key_val = []
        self.key_depth = []
        self.depth_max = 9


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

        self.depth_max = 2*state.getNumFood() 
        if self.depth_max > 10 :
            self.depth_max = 10
        elif self.depth_max <5 :
            self.depth_max = 5
        minimax_move = self.minimax(state, True, 0, state.getNumFood())

        try:
            return minimax_move[1]

        except IndexError:
            return Directions.STOP


    def minimax (self, state, agent, depth, initial_numfood):


        """
        Given a pacman game state, the agent, the recurion depth and the number of food dots before running minimax returns a score and the legal move related.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        - 'agent': pacman (True) or ghost (False).
        - 'depth': the recursion depth.
        - 'initial_numfood': the number of food dots before running minimax.

        Return:
        -------
        - A score and the legal move related as defined in `game.Directions`.
        """

        if state.isWin() or state.isLose() :
            return [state.getScore(), "/"]
        if  initial_numfood > state.getNumFood():
            if self.depth_max > depth :
                self.depth_max = depth
            return [state.getScore() - depth, "/"]

        if depth >= self.depth_max and agent == True:
            return [state.getScore() - 1*self.min_move(state), "/"]
            
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
                
                val = self.minimax(next_state, False, depth+1, initial_numfood)

                val[1] = action
                if val[0] > max_val[0] :
                    max_val = val
            return max_val
            
        else:
            min_val = [math.inf, "/"]
            for next_state, action in state.generateGhostSuccessors(1):
                val = self.minimax(next_state, True, depth+1, initial_numfood)
                val[1] = action
                if val[0] < min_val[0] :
                    min_val = val
            return min_val


    def min_move(self, state) :


        """
        Given a pacman game state returns the distance between pacman and the nearest food dot except if the ghost is too close from pacman.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - The distance between pacman and the nearest food dot except if the ghost is too close from pacman.
        """
        
        pos_P = state.getPacmanPosition()
        pos_G = state.getGhostPosition(1)
        dist_GP = manhattanDistance(pos_G,pos_P)
        if dist_GP < 1 :
            return (state.getScore() - 500)
        else :
            food_location = state.getFood()
            dist_min = math.inf
            pos_d = ()
            dots_pos = []

            for x in range(food_location.width) :
                for y in range(food_location.height) :
                    if food_location[x][y] == True :
                        dist = manhattanDistance(pos_P, (x,y))
                        dots_pos.append((x,y))
                        if dist < dist_min :
                            dist_min = dist
                            pos_d = (x,y)

            return dist_min