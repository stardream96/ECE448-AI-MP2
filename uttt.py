from time import sleep
from math import inf
from random import randint

import time ## need to delete
class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

    ##### helper functions by hf
    def allSpotsInBoard(self,currBoardIdx):
        # return all spots in a local board
        xy = self.globalIdx[currBoardIdx]
        x = xy[0]
        y = xy[1]
        result = []
        for i in range(0,3):
            for j in range(0,3):
                result.append((x+i, y+j))
        return result
    def emptySpotsInBoard(self, currBoardIdx):
        # return all empty spots in a local board
        xy = self.globalIdx[currBoardIdx]
        x = xy[0]
        y = xy[1]
        result = []
        for i in range(0,3):
            for j in range(0,3):
                if self.board[x+i][y+j] == '_':
                    result.append((x+i, y+j))
        return result
    def makeMove(self, location, isMax):
        if isMax == 1:
            print(location[0])
            print(location[1])
            self.board[location[0]][location[1]] = 'X'
        elif isMax == 0:
            self.board[location[0]][location[1]] = '_'
        elif isMax == -1:
            self.board[location[0]][location[1]] = 'O'
    #####
    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')
    def num_twos(self, player, opponent):
        """
        This is a helper function to count unblocked two-in-a-rows and prevented two-in-a-rows
        for the evaluation functions.
        110 MEANS PLAYER, PLAYER, OPPONENT!! (opponent blocks the two owned by player)
        :param player: either self.maxPlayer(X) or minPlayer(O)
        :param opponent: when opponent is '_', we are checking unblocked two-in-a-rows
                         or opponent is either 'X' or 'O'
        :return: number of unblocked two-in-a-rows owned by player
        """
        count = 0
        for start in self.globalIdx:
            # on rows (6 cases)
            if self.board[start[0]][start[1]] == player and self.board[start[0]][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == opponent:
                count += 1      #first row 110
            if self.board[start[0]][start[1]] == opponent and self.board[start[0]][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == player:
                count += 1      #first row 011
            if self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 2] == opponent:
                count += 1      #second row 110
            if self.board[start[0] + 1][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 2] == player:
                count += 1      #second row 011
            if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 2][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
                count += 1      #third row 110
            if self.board[start[0] + 2][start[1]] == opponent and self.board[start[0] + 2][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == player:
                count += 1      #third row 011
            # on cols (6 cases)
            if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 2][start[1]] == opponent:
                count += 1      #first col 110
            if self.board[start[0]][start[1]] == opponent and self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 2][start[1]] == player:
                count += 1      #first col 011
            if self.board[start[0]][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 1] == opponent:
                count += 1      #second col 110
            if self.board[start[0]][start[1] + 1] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 1] == player:
                count += 1      #second col 011
            if self.board[start[0]][start[1] + 2] == player and self.board[start[0] + 1][start[1] + 2] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
                count += 1      #third col 110
            if self.board[start[0]][start[1] + 2] == opponent and self.board[start[0] + 1][start[1] + 2] == player and self.board[start[0] + 2][start[1] + 2] == player:
                count += 1      #third col 011
            # on diagonals (4 cases)
            if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
                count += 1
            if self.board[start[0]][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == player:
                count += 1
            if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == opponent:
                count += 1
            if self.board[start[0] + 2][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == player:
                count += 1
        return count
    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score = 0
        if isMax:
            if self.checkWinner() == 1:
                return 10000
            #second rule:
            score += self.num_twos(self.maxPlayer, '_') * 500
            score += self.num_twos(self.minPlayer, self.maxPlayer) * 100
            if score != 0:
                return score
            #third rule: check corners
            for start in self.globalIdx:
                if self.board[start[0]][start[1]] == self.maxPlayer:
                    score += 30
                if self.board[start[0] + 2][start[1]] == self.maxPlayer:
                    score += 30
                if self.board[start[0]][start[1] + 2] == self.maxPlayer:
                    score += 30
                if self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
                    score += 30
        else:
            if self.checkWinner() == -1:
                return -10000
            #second rule:
            score -= self.num_twos(self.minPlayer, '_') * 100
            score -= self.num_twos(self.maxPlayer, self.minPlayer) * 500
            if score != 0:
                return score
            #third rule: check corners
            for start in self.globalIdx:
                if self.board[start[0]][start[1]] == self.minPlayer:
                    score -= 30
                if self.board[start[0] + 2][start[1]] == self.minPlayer:
                    score -= 30
                if self.board[start[0]][start[1] + 2] == self.minPlayer:
                    score -= 30
                if self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
                    score -= 30
        return score
    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        return score
    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for line in self.board:
            for slot in line:
                if slot == '_':
                    return True
        return False
    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        #check row wins
        for line in self.board:
            if (line[0] == line[1] == line[2] == self.maxPlayer) or (line[3] == line[4] == line[5] == self.maxPlayer) or (line[6] == line[7] == line[8] == self.maxPlayer):
                return 1
            if (line[0] == line[1] == line[2] == self.minPlayer) or (line[3] == line[4] == line[5] == self.minPlayer) or (line[6] == line[7] == line[8] == self.minPlayer):
                return -1
        #check column wins
        for start in self.globalIdx:
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] ] == self.board[start[0]+ 2 ][start[1]] == self.maxPlayer:
                return 1
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] ] == self.board[start[0]+ 2 ][start[1]] == self.minPlayer:
                return -1
            if self.board[start[0]][start[1] + 1] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 1] == self.maxPlayer:
                return 1
            if self.board[start[0]][start[1] + 1] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 1] == self.minPlayer:
                return -1
            if self.board[start[0]][start[1] + 2] == self.board[start[0] + 1][start[1] + 2] == self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
                return 1
            if self.board[start[0]][start[1] + 2] == self.board[start[0] + 1][start[1] + 2] == self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
                return -1
        #check diagonal wins:
        for start in self.globalIdx:
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
                return 1
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
                return -1
            if self.board[start[0] + 2][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0]][start[1] + 2] == self.maxPlayer:
                return 1
            if self.board[start[0] + 2][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0]][start[1] + 2] == self.minPlayer:
                return -1
        #no winner:
        return 0
    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        bestValue=0.0
        return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        bestValue=0.0
        if depth == 0:
            return self.evaluatePredifined(isMax)
        else :
            turn = 1
            if not isMax:
                turn = -1
            bestValueList = []
            bestMoveList  = []
            allSpots = self.allSpotsInBoard(currBoardIdx)
            for i, spot in enumerate(allSpots):
                if self.board[spot[0]][spot[1]] == '_':
                    self.makeMove(spot, turn)
                    result = self.minimax_recursive(depth - 1, i, not isMax)
                    bestValueList.append(result)
                    bestMoveList.append(spot)
                    self.makeMove(spot, 0)      # undo the makeMove
            if (isMax) :
                bestValue = max(bestValueList)
            else :
                bestValue = min(bestValueList)
            index = bestValueList.index(bestValue)
            bestMove = bestMoveList[index]
        return bestValue, bestMove
    ### recursive helper by hf
    def minimax_recursive(self, depth, currBoardIdx, isMax):
        bestValue=0.0
        if depth == 0:
            bestValue = self.evaluatePredifined(isMax)
            # self.printGameBoard()
            # print(bestValue)
            return bestValue
        else :
            turn = 1
            if not isMax:
                turn = -1
            bestValueList = []
            allSpots = self.allSpotsInBoard(currBoardIdx)
            for i, spot in enumerate(allSpots):
                if self.board[spot[0]][spot[1]] == '_':
                    self.makeMove(spot, turn)
                    result = self.minimax_recursive(depth - 1, i, not isMax)
                    bestValueList.append(result)
                    self.makeMove(spot, 0)      # undo the makeMove
            if (isMax) :
                bestValue = max(bestValueList)
            else :
                bestValue = min(bestValueList)
        return bestValue
    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE　
        print("playGamePredifinedAgent")
        turn = 1 # 1 for maxPlayer, -1 for minPlayer
        if (not maxFirst) :
            turn = -1
        currBoardIdx = self.startBoardIdx
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        while self.checkWinner() == 0:
            self.printGameBoard()
            if (turn) :
                if (isMinimaxOffensive):
                    best_value, best_move = self.minimax(self.maxDepth, currBoardIdx, True)
                else :
                    best_value, best_move = self.alphabeta(self.maxDepth,currBoardIdx,alpha,beta,True) ## not implemented yet

            else :
                if (isMinimaxDefensive):
                    best_value, best_move = self.minimax(self.maxDepth, currBoardIdx, True)
                else :
                    best_value, best_move = self.alphabeta(self.maxDepth,currBoardIdx,alpha,beta,True) ## not implemented yet
            print(best_move)
            nextBoardIdx = (best_move[0] - self.globalIdx[currBoardIdx][0])* 3 + best_move[1] - self.globalIdx[currBoardIdx][1]
            currBoardIdx = nextBoardIdx
            self.printGameBoard()
            self.makeMove(best_move, turn)
            bestMove.append(best_move)
            bestValue.append(best_value)
            gameBoards.append(self.board.copy())
            time.sleep(0.2)
            turn = -turn


        winner = self.checkWinner()
        expandedNodes = 0
        self.printGameBoard()
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
