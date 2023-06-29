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
    
    return (state.getGhostDirection(1), state.getPacmanPosition(), state.getGhostPosition(1), state.getFood(), tuple(state.getCapsules()))


class PacmanAgent(Agent):


    def __init__(self, args):


        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """

        self.key_val = []
        self.key_depth = []


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
        depth_N = 8
        depth_S = 8
        depth_W = 8
        depth_E = 8

        cutOff_ans = self.cutOff(state)
        if cutOff_ans[0] == 1:
            depth_N = cutOff_ans[1]
        elif cutOff_ans[0] == 2:
            depth_S = cutOff_ans[1]
        elif cutOff_ans[0] == 3:
            depth_W = cutOff_ans[1]
        elif cutOff_ans[0] == 4:
            depth_E = cutOff_ans[1]
        elif cutOff_ans[0] == 5:
            depth_S = cutOff_ans[1]
            depth_W = cutOff_ans[2]
        elif cutOff_ans[0] == 6:
            depth_N = cutOff_ans[1]
            depth_W = cutOff_ans[2]
        elif cutOff_ans[0] == 7:
            depth_S = cutOff_ans[1]
            depth_E = cutOff_ans[2]
        elif cutOff_ans[0] == 8:
            depth_N = cutOff_ans[1]
            depth_E = cutOff_ans[2]

        minimax_move = self.minimax(state, True, 0, depth_N, depth_S, depth_W, depth_E)

        try:
            return minimax_move[1]

        except IndexError:
            return Directions.STOP
    

    def minimax (self, state, agent, depth, depth_N, depth_S, depth_W, depth_E):


        """
        Given a pacman game state, the agent, the recurion depth and the maximum recursion depth for each orientation returns a score and the legal move related.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        - 'agent': pacman (True) or ghost (False).
        - 'depth': the recursion depth.
        - 'depth_N': the maximum recursion depth for the North.
        - 'depth_S': the maximum recursion depth for the South.
        - 'depth_W': the maximum recursion depth for the West.
        - 'depth_E': the maximum recursion depth for the East.

        Return:
        -------
        - A score and the legal move related as defined in `game.Directions`.
        """

        if state.isWin() or state.isLose() :
            return [state.getScore(), "/"]

        if depth_N <= 0 or depth_S <= 0 or depth_W <= 0 or depth_E <= 0 and agent == True:
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

                if (action == "North"):
                    val = self.minimax(next_state, False, depth+1, depth_N-1, depth_S, depth_W, depth_E)
                if (action == "South"):
                    val = self.minimax(next_state, False, depth+1, depth_N, depth_S-1, depth_W, depth_E)
                if (action == "West"):
                    val = self.minimax(next_state, False, depth+1, depth_N, depth_S, depth_W-1, depth_E)
                if (action == "East"):
                    val = self.minimax(next_state, False, depth+1, depth_N, depth_S, depth_W, depth_E-1)
                
                val[1] = action
                if val[0] > max_val[0] :
                    max_val = val
            return max_val
            
        else:
            min_val = [math.inf, "/"]
            for next_state, action in state.generateGhostSuccessors(1):
        
                val = self.minimax(next_state, True, depth+1, depth_N-1, depth_S-1, depth_W-1, depth_E-1)
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
        if dist_GP < 2 :
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


    def cutOff(self, state):


        """
        Given a pacman game state returns the y-distance and the x-distance between pacman and the ghost.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - The y-distance and the x-distance between pacman and the ghost.
        """

        finder = set()
        (x, y) = state.getPacmanPosition()
        (m, n) = state.getGhostPosition(1)
        if x>=m and y>=n:
            finder.add(1)
        if x>=m and y<=n:
            finder.add(2)
        if x<=m and y>=n:
            finder.add(3)
        if x<=m and y<=n:
            finder.add(4)
        
        if 1 in finder and 2 in finder:
            depth_W = abs(x-m)
            return [3, depth_W, -1]
        elif 1 in finder and 3 in finder:
            depth_S = abs(y-n)
            return [2, depth_S, -1]
        elif 2 in finder and 4 in finder:
            depth_N = abs(n-y)
            return [1, depth_N, -1]
        elif 3 in finder and 4 in finder:
            depth_E = abs(m-x)
            return [4, depth_E, -1]
        elif 1 in finder:
            depth_S = abs(y-n)
            depth_W = abs(x-m)
            return [5, depth_S, depth_W]
        elif 2 in finder:
            depth_N = abs(n-y)
            depth_W = abs(x-m)
            return [6, depth_N, depth_W]
        elif 3 in finder:
            depth_S = abs(y-n)
            depth_E = abs(m-x)
            return [7, depth_S, depth_E]
        elif 4 in finder:
            depth_N = abs(n-y)
            depth_E = abs(m-x)
            return [8, depth_N, depth_E]