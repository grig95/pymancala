from board_state import BoardState

# Functions used in alpha-beta evaluation
# They take a BoardState and a boolean isPlayerOne value and return a state evaluation relative to the player, i.e. positive for a good position and negative otherwise
class AlphaBetaEvaluationFunctions:
    def __init__(self):
        pass
    
    # Simply subtracts the opposing player's mancala score from the current one's
    @staticmethod
    def naiveMancalaDifference(boardState : BoardState, isPlayerOne=True):
        if isPlayerOne:
            return boardState.mancala1-boardState.mancala2
        else:
            return boardState.mancala2-boardState.mancala1
    
    # Does the mancala difference and adds the difference between capture potentials
    @staticmethod
    def mancalaDifferencePlusCapture(boardState : BoardState, isPlayerOne=True):
        score = boardState.mancala1-boardState.mancala2
        for i in range(6):
            if boardState.slots[i]==0:
                score+=0.5*boardState.slots[11-i]
        for i in range(6, 12):
            if boardState.slots[i]==0:
                score-=0.5*boardState.slots[11-i]
        if isPlayerOne:
            return score
        else:
            return -score

# Contains the logic for the alpha-beta search
class AlphaBetaNode:
    def __init__(self, boardState : BoardState, parentNode = None):
        self.boardState=boardState
        self.parentNode=parentNode
        self.provisionalValue=None # nodes that have no value may have a provisionalValue, but nodes with a value MUST have a provisionalValue equal to it
        self.value=None
        self.children=None
    
    # Propagates the Provisional Backed up Value upwards up to the first ancestor node belonging to the other player, 
    # from the perspective of the player indicated by isPlayerOne
    def propagatePBV(self, isPlayerOne):
        if self.parentNode is not None:
            if self.parentNode.provisionalValue is None:
                self.parentNode.provisionalValue=self.provisionalValue
            elif self.parentNode.boardState.isPlayerOnesTurn == isPlayerOne: # the parent node belongs to the current player, maximize it
                self.parentNode.provisionalValue=max(self.parentNode.provisionalValue, self.provisionalValue)
            else: # the parent node belongs to the opposing player, minimize it
                self.parentNode.provisionalValue=min(self.parentNode.provisionalValue, self.provisionalValue)


    # Check the ancestors for provisional values that lead to pruning
    def checkForPruning(self, childPBV, isPlayerOne):
        if childPBV is None:
            return False

        if self.boardState.isPlayerOnesTurn != isPlayerOne: #the ancestor node is of a different type from the (Nxgrand)child
            if isPlayerOne: # the child is a current player node
                if self.provisionalValue is not None and self.provisionalValue<childPBV:
                    return True
            else: # the child is an other player node
                if self.provisionalValue is not None and self.provisionalValue>childPBV:
                    return True
        
        if self.parentNode is not None:
            return self.parentNode.checkForPruning(childPBV, isPlayerOne)
        else:
            return False
    

    def setValueAndPropagate(self, value, isPlayerOne):
        self.value=value
        self.provisionalValue=self.value
        self.propagatePBV(isPlayerOne)


    # Runs the alpha-beta pruning algorithm with a set depth, using the given evaluation function and from the perspective of the player specified through isPlayerOne
    def runAlphaBeta(self, depth, evalFunction, isPlayerOne):
        # reset value and provisionalValue
        self.value=None
        self.provisionalValue=None

        if depth==0 or self.boardState.isFinal(): # reached the end of the search, evaluate position and propagate values
            self.setValueAndPropagate(evalFunction(self.boardState, isPlayerOne), isPlayerOne)
            return
        
        # Create children list if it does not exist
        if self.children is None:
            self.children=[]
            for state in self.boardState.getNextStatesList():
                if state is None:
                    self.children.append(None)
                else:
                    self.children.append(AlphaBetaNode(state, self))
        
        # Recurse through children
        for child in self.children:
            if child is not None:
                child.runAlphaBeta(depth-1, evalFunction, isPlayerOne)
                # Check ancestors' provisional values for pruning:
                if self.checkForPruning(self.provisionalValue, isPlayerOne):
                    break

        # There should be now a provisionalValue set (because the node was either pruned out based on it or all of its children were evaluated)]
        self.setValueAndPropagate(self.provisionalValue, isPlayerOne)



class AlphaBetaAgent:
    def __init__(self, isPlayerOne, depth, evalFunction):
        self.root = None
        self.isPlayerOne=isPlayerOne
        self.depth=depth
        self.evalFunction=evalFunction

    def setBoardState(self, boardState : BoardState):
        self.root = AlphaBetaNode(boardState)
    
    # Returns a number between 0 and 5 corresponding to its chosen move
    def getBestMove(self):
        self.root.runAlphaBeta(self.depth, self.evalFunction, self.isPlayerOne)
        #self.debug_print_root_value()
        #self.debug_print_next_move_values()
        for moveIndex, child in enumerate(self.root.children):
            if child is not None:
                if self.root.value == child.value:
                    return moveIndex
    
    # Takes a moveIndex and updates the root accordingly. Used to 'notify' the agent of the next move so it can re-use already created objects in the next calculation
    # Using this speeds up the game-length search by roughly 70%!
    def updateBoardState(self, moveIndex):
        if self.root is None:
            raise Exception("AlphaBetaAgent.updateBoardState() was called, but the object has no root member set.")
        
        if self.root.children is not None:
            if self.root.children[moveIndex] is None:
                raise Exception("AlphaBetaAgent.updateBoardState() was called with a moveIndex indicating an invalid move.")
            self.root=self.root.children[moveIndex]
        else:
            newState=self.root.boardState.getStateAfterMove(moveIndex)
            if newState is None:
                raise Exception("AlphaBetaAgent.updateBoardState() was called with a moveIndex indicating an invalid move.")
            self.root=AlphaBetaNode(newState)

    def debug_print_root_value(self):
        print(self.root.value)

    def debug_print_next_move_values(self):
        l = []
        for child in self.root.children:
            if child is None:
                l.append(None)
            else:
                l.append(child.value)
        print(l)
