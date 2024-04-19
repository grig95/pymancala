from board_state import BoardState
from alphabeta import AlphaBetaEvaluationFunctions, AlphaBetaAgent
from randommove import RandomMoveAgent
import time

boardState=BoardState()

def botVsBot(agent1, agent2):
    agent1.isPlayerOne=True
    agent2.isPlayerOne=False

    start=time.time()

    agent1.setBoardState(boardState)
    agent2.setBoardState(boardState)

    while not boardState.isFinal():
        if boardState.isPlayerOnesTurn:
            chosenMove = agent1.getBestMove()
            agent1.updateBoardState(chosenMove)
            agent2.updateBoardState(chosenMove)
            print(f'Player1 chose move {chosenMove}\n')
            boardState=boardState.getStateAfterMove(chosenMove)
        else:
            chosenMove = agent2.getBestMove()
            agent1.updateBoardState(chosenMove)
            agent2.updateBoardState(chosenMove)
            print(f'Player2 chose move {chosenMove}\n')
            boardState=boardState.getStateAfterMove(chosenMove)

    end=time.time()

    print(boardState)
    print(f'Elapsed time: {end-start}')


def playerVsBot():
    isPlayerFirst = 'c'
    while isPlayerFirst not in ['y', 'n']:
        isPlayerFirst = input('Take the first move? (y/n) ')
        if isPlayerFirst not in ['y', 'n']:
            print('Invalid input')
    isPlayerFirst = isPlayerFirst=='y'
    if not isPlayerFirst:
        print('You are player 2. Your slots are 6-11. When choosing a move input 0 for your first slot (6), 1 for your second (7) and so on...')
    else:
        print('You are player 1. Your slots are 0-5.')

    botTypeIndex = 0
    while botTypeIndex not in ['1', '2']:
        botTypeIndex=input("Choose your opponent:\n1. Alpha-beta pruning\n2. Random move agent\n")
        if botTypeIndex not in ['1', '2']:
            print('Invalid input')
    
    if botTypeIndex == '1': #Alpha-beta
        evalFunctionIndex=0
        while evalFunctionIndex not in ['1', '2']:
            evalFunctionIndex=input("Choose the evaluation function for the alpha-beta algorithm:\n1. Naive mancala difference\n2. Mancala difference with (pseudo-)capture potential\n")
            if evalFunctionIndex not in ['1', '2']:
                print('Invalid input')
        
        if evalFunctionIndex == '1':
            evalFunction=AlphaBetaEvaluationFunctions.naiveMancalaDifference
        elif evalFunctionIndex == '2':
            evalFunction=AlphaBetaEvaluationFunctions.mancalaDifferencePlusCapture
        
        depth=False
        while type(depth) is not int:
            depth=input('Enter alpha-beta depth: ')
            try:
                depth=int(depth)
            except:
                print('Invalid input')
        
        AIAgent=AlphaBetaAgent(not isPlayerFirst, depth, evalFunction)
    elif botTypeIndex == '2': # Random move agent
        AIAgent=RandomMoveAgent()
    
    # Start game
    boardState=BoardState()
    AIAgent.setBoardState(boardState)
    while not boardState.isFinal():
        print(boardState)
        if isPlayerFirst==boardState.isPlayerOnesTurn: # Player's turn
            chosenMove=7
            while chosenMove not in range(6) or boardState.getNextStatesList()[chosenMove] is None:
                chosenMove=input('Choose your move (0-5): ')
                try:
                    chosenMove=int(chosenMove)
                    if chosenMove not in range(6) or boardState.getNextStatesList()[chosenMove] is None:
                        print('Invalid move!')
                except:
                    print('Invalid move symbol!')
            boardState=boardState.getStateAfterMove(chosenMove)
            AIAgent.updateBoardState(chosenMove)
        else: # AI's turn
            chosenMove=AIAgent.getBestMove()
            print(f'AI chose move {chosenMove}.')
            boardState=boardState.getStateAfterMove(chosenMove)
            AIAgent.updateBoardState(chosenMove)
    print(boardState) # Winner




if __name__ == '__main__':
    playerVsBot()