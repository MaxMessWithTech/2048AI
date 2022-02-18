import copy
import numpy as np

class algoSave:
    def __init__(self, eval, moves, bias, numb):
        self.eval = eval
        self.moves = moves
        self.bias = bias
        self.numb = numb
    
    def __repr__(self) -> list:
        return self.moves

def searchAlgoSaveList(saveSim, eval, moves, bias):
    for save in saveSim:
        if save.moves == moves:
            save.eval += eval
            save.numb += 1
            save.bias += bias
            return saveSim
    saveSim.append(algoSave(eval, moves, bias, 1))
    return saveSim

def algo(gameObj, maxDepth, moves=[], depth=1, placeBias=1, curMax=0, allEvals=[], ENABLE_2_4_ADDING = False):
    if depth == maxDepth:
        eval = evaluate(gameObj.state, gameObj) * placeBias
        allEvals = allEvals+[eval]
        return eval, moves, placeBias, allEvals, gameObj.state
    
    allEvals = allEvals+[evaluate(gameObj.state, gameObj) * placeBias]
    
    # CurMax needs to be on the first level of anylysis
    # print(f"curMax: {curMax}")
    if evaluate(gameObj.state, gameObj) * placeBias < curMax:
        #print(f"Giving up at curMax: {curMax}")
        return evaluate(gameObj.state, gameObj) * placeBias, moves, placeBias, allEvals, gameObj.state
    
    highestEval = 0
    highestBias = 0
    bestMoveSeq = []
    bestState = None

    validMoves = gameObj.find_valid_moves()

    if len(validMoves) == 0:
        return evaluate(gameObj.state, gameObj) * placeBias, moves, placeBias, allEvals, gameObj.state

    for move in validMoves:
        copyiedGameObj = copy.deepcopy(gameObj)
        copyiedGameObj.move(move)
        copyMoves = copy.deepcopy(moves)
        copyMoves.append(move)

        # NEXT - ADD all of the sims together when simulating 2's and 4's

        saveSim = list()

        for y in range(4):
            for x in range(4):
                if copyiedGameObj.state[y][x] == 0:
                    copyiedGameObj2 = copy.deepcopy(copyiedGameObj)
                    copyiedGameObj2.placeNumb(2, x, y)
                    moveSimEval, movesSimList, movePlaceBias, simAllEvals, simState = algo(
                        copyiedGameObj2, maxDepth, 
                        moves=copyMoves, depth=depth + 1, placeBias=placeBias*9, 
                        curMax=curMax, 
                        allEvals=copy.copy(allEvals), 
                        ENABLE_2_4_ADDING=ENABLE_2_4_ADDING
                    )
                    # SOMEHOW INCREASE curMax by highest boi
                    if ENABLE_2_4_ADDING:
                        searchAlgoSaveList(saveSim, moveSimEval, movesSimList, movePlaceBias)
                    elif  moveSimEval > highestEval:
                        highestEval = moveSimEval
                        bestMoveSeq = movesSimList
                        highestBias = movePlaceBias
                        bestState = simState
                        curMax = simAllEvals[depth-1]
                    
                    copyiedGameObj4 = copy.deepcopy(copyiedGameObj)
                    copyiedGameObj4.placeNumb(4, x, y)
                    moveSimEval, movesSimList, movePlaceBias, simAllEvals, simState = algo(
                        copyiedGameObj4, maxDepth, 
                        moves=copyMoves, depth=depth + 1, placeBias=placeBias*1, 
                        curMax=curMax, 
                        allEvals=copy.copy(allEvals), 
                        ENABLE_2_4_ADDING=ENABLE_2_4_ADDING
                    )
                    if ENABLE_2_4_ADDING:
                        searchAlgoSaveList(saveSim, moveSimEval, movesSimList, movePlaceBias)
                    elif  moveSimEval > highestEval:
                        highestEval = moveSimEval
                        bestMoveSeq = movesSimList
                        highestBias = movePlaceBias
                        bestState = simState
                        curMax = simAllEvals[depth-1]

        # Do thing with thing
        if ENABLE_2_4_ADDING:
            for save in saveSim:
                if (save.eval / save.numb) > highestEval:
                    highestEval = save.eval / save.numb
                    bestMoveSeq = save.moves
                    highestBias = save.bias

    return highestEval, bestMoveSeq, highestBias, allEvals, bestState


def asyncAlgo(gameObj, maxDepth, callback):
    moveEval, moves, moveBias, allEvals = algo(gameObj, maxDepth)
    # print("Async Algo done")
    callback(moveEval, moves, moveBias, allEvals)
    

def evaluate(state, gameObj):
    bias_matrix = [
        [0, 1, 2, 8],
        [1, 2, 2, 8],
        [2, 2, 12, 16],
        [8, 8, 16, 64]
    ]

    matrix, rating = mmult(bias_matrix, state)

    # rating = rating * len(gameObj.find_valid_moves())

    return rating
    


def mmult(matrix1, matrix2):
    res = [[0 for x in range(4)] for y in range(4)] 
    resInt = 0
    
    # explicit for loops
    """
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
    
                # resulted matrix
                res[i][j] += matrix1[i][k] * matrix2[k][j]
                resInt += matrix1[i][k] * matrix2[k][j]
    """
    # """
    for y in range(4):
        for x in range(4):
            res[y][x] = matrix1[y][x] * matrix2[y][x]
            resInt += res[y][x]
    # """
    return res, resInt
    

def matrixSimilarity(matrix1, matrix2):
    same = 0
    for y in range(4):
        for x in range(4):
            if matrix1[y][x] == matrix2[y][x]:
                same += 1
    return same


"""
1) Apply rating engine
"""