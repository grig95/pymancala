from board_state import BoardState
import random

class RandomMoveAgent:
    def __init__(self):
        self.boardState=None

    def setBoardState(self, boardState):
        self.boardState=boardState

    def updateBoardState(self, moveIndex):
        self.boardState=self.boardState.getStateAfterMove(moveIndex)
    
    def getBestMove(self):
        possibleMoves = self.boardState.getNextStatesList()
        indices=[]
        for i in range(6):
            if possibleMoves[i] is not None:
                indices.append(i)
        return indices[random.randint(0, len(indices)-1)]