class BoardState:
    # The board is arranged and interpreted as such: slots 0-5 (player1's slots), mancala 1, slots 6-11 (player2's slots), mancala 2, ... (loopback) 
    def __init__(self,
                 isPlayerOnesTurn=True, 
                 slots=[4 for i in range(12)], 
                 mancala1=0,
                 mancala2=0):
        
        if len(slots)!=12:
            raise Exception("Invalid amount of slots in BoardState constructor!")
        self.isPlayerOnesTurn=isPlayerOnesTurn
        self.slots=slots.copy()
        self.mancala1=mancala1
        self.mancala2=mancala2
    

    # Equality check
    def __eq__(self, other):
        return (self.isPlayerOnesTurn==other.isPlayerOnesTurn and 
                self.slots==other.slots and
                self.mancala1==other.mancala1 and
                self.mancala2==other.mancala2)
    

    # Used to print the state to console
    def __str__(self):
        if self.isFinal(): # if the game is over
            string = f'Player 1: {self.mancala1}\nPlayer 2: {self.mancala2}\n'
            if self.mancala1>self.mancala2:
                string+='Player 1 wins!\n'
            elif self.mancala1<self.mancala2:
                string+='Player 2 wins!\n'
            else:
                string+='Draw!\n'
            return string           

        if self.isPlayerOnesTurn:
            string='Player 1 to move!\n\n'
        else:
            string='Player 2 to move!\n\n'
        for i in range(6):
            string += f'Slot {i}: {self.slots[i]}\n'
        string += f'Mancala 1: {self.mancala1}\n'
        for i in range(6, 12):
            string += f'Slot {i}: {self.slots[i]}\n'
        string += f'Mancala 2: {self.mancala2}\n'
        return string
    

    # Returns a new BoardState, corresponding to the state after a move, or None if the move is invalid
    # Takes an integer (x) from between 0 and 5, and interprets it as the player to move picking their x-th slot
    def getStateAfterMove(self, moveIndex):
        if moveIndex not in [x for x in range(6)]:
            raise ValueError(f"Invalid argument: BoardState.getStateAfterMove(moveIndex) expects an integer between 0 and 5, but instead got {moveIndex}.")
        
        if self.isPlayerOnesTurn:
            trueSlot=moveIndex
        else:
            trueSlot=moveIndex+6
        
        # Check for invalid move, i.e. the game is already over or slot with 0 pebbles chosen and return None if so
        if self.slots[trueSlot]==0:
            return None

        # Update pebble count for each slot and the right mancala:
        newState=BoardState(self.isPlayerOnesTurn, self.slots, self.mancala1, self.mancala2)
        pebblesUp=self.slots[trueSlot]
        newState.slots[trueSlot]=0
        for i in range(12):
            newState.slots[i]+=pebblesUp//13
        if self.isPlayerOnesTurn:
            newState.mancala1+=pebblesUp//13
        else:
            newState.mancala2+=pebblesUp//13
        if self.isPlayerOnesTurn: #if the first player made the move
            for r in range(1, pebblesUp%13+1):
                if moveIndex+r<6:
                    newState.slots[moveIndex+r]+=1
                elif moveIndex+r==6:
                    newState.mancala1+=1
                else:
                    newState.slots[(moveIndex+r-1)%12]+=1
        else: #if the second player made the move
            for r in range(1, pebblesUp%13+1):
                if moveIndex+r<6:
                    newState.slots[trueSlot+r]+=1
                elif moveIndex+r==6:
                    newState.mancala2+=1
                else:
                    newState.slots[(trueSlot+r-1)%12]+=1
        
        # Capture opposing pebbles if the last pebble was placed in an empty slot belonging to the current player
        lastPebbleSlot = -1
        if moveIndex+pebblesUp<6 and newState.slots[trueSlot+pebblesUp]==1: # last pebble placed in an empty slot succeeding the initial one in current player's field
            lastPebbleSlot = trueSlot+pebblesUp
        elif pebblesUp>12-moveIndex and pebblesUp<=13 and newState.slots[(trueSlot+pebblesUp-1)%12]==1:  # last pebble placed in either the initial slot (which was empty) 
                                                                                                        # or in an empty one preceding it in the current player's field
            lastPebbleSlot = (trueSlot+pebblesUp-1)%12
        # If there is a capture to be made
        if lastPebbleSlot!=-1:
            if self.isPlayerOnesTurn:
                newState.mancala1+=newState.slots[lastPebbleSlot]+newState.slots[11-lastPebbleSlot]
                newState.slots[lastPebbleSlot]=0
                newState.slots[11-lastPebbleSlot]=0
            else:
                newState.mancala2+=newState.slots[lastPebbleSlot]+newState.slots[11-lastPebbleSlot]
                newState.slots[lastPebbleSlot]=0
                newState.slots[11-lastPebbleSlot]=0
        
        # Change the player to move, unless the last pebble was placed in the current player's mancala
        if not moveIndex+pebblesUp%13==6: #last pebble in mancala
            newState.isPlayerOnesTurn = not self.isPlayerOnesTurn
        
        #Check if the game is over, i.e. if all slots on one side of the field are empty
        if newState.slots[:6]==[0 for i in range(6)]: #Player1's slots are empty, move player2's pebbles in their mancala
            for i in range(6, 12):
                newState.mancala2+=newState.slots[i]
                newState.slots[i]=0
        elif newState.slots[6:12]==[0 for i in range(6)]: #Do the same for Player2
            for i in range(6):
                newState.mancala1+=newState.slots[i]
                newState.slots[i]=0
        
        return newState
    

    # Returns a list of possible next states, indexed by their corresponding move indices
    # (None values are possible for invalid move indexes)
    def getNextStatesList(self):
        l=[]
        for i in range(6):
            l.append(self.getStateAfterMove(i))
        return l
    

    # Checks if a state is final, i.e. if the game is over
    def isFinal(self):
        return self.slots==[0 for x in range(12)]