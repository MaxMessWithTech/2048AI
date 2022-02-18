from socket import timeout
import pygame
import classes
import algo
import threading
import time
import copy

pygame.init()

screen = pygame.display.set_mode([300, 300])

gridObj = classes.gameGrid()
gameObj = classes.game()

gameObj.placeRandomNumb(True)
gameObj.placeRandomNumb(True)


algoReady = False
algoStarted = False
algoMoveEval = 0
algoMoves = list()
algoMoveBias = 0
algoAllEvals = list()
def setAlgoReady(moveEval, moves, moveBias, allEvals):
    global algoStarted, algoMoveEval, algoMoves, algoMoveBias, algoAllEvals, algoReady
    algoMoveEval = moveEval
    algoMoves = moves
    algoMoveBias = moveBias
    algoAllEvals = allEvals
    algoReady = True


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if gameObj.move("l"):
                    gameObj.placeRandomNumb()
            elif event.key == pygame.K_RIGHT:
                if gameObj.move("r"):
                    gameObj.placeRandomNumb()
            elif event.key == pygame.K_UP:
                if gameObj.move("u"):
                    gameObj.placeRandomNumb()
            elif event.key == pygame.K_DOWN:
                if gameObj.move("d"):
                    gameObj.placeRandomNumb()

    screen.fill((0, 0, 0)) # Clears screen
    gridObj.update(gameObj.state)

    if len(gameObj.find_valid_moves()) == 0:
        score, highVal = gameObj.endStats()
        print(f"\r\n{classes.blcolors.RED}GAME OVER{classes.blcolors.CLEAR} Score: {score}, highest: {highVal}")
        print(gameObj.state)
        time.sleep(2)
        gameObj.clear()
        pygame.event.clear()
    
    # print(f"Algo State: Started: {algoStarted}, Finished {algoReady}", end="\r\n")
    if not algoStarted:
        algoStarted = True
        x = threading.Thread(target=algo.asyncAlgo, args=(gameObj, 3, setAlgoReady), daemon=True)
        x.start()
        algoReady = False
    elif algoReady:
        moveEval = algoMoveEval
        moves = algoMoves
        moveBias = algoMoveBias
        allEvals = algoAllEvals
        try:
            gameObjCopy = copy.deepcopy(gameObj)
            gameObj.move(moves[0], place=True)
            for gameMove in moves:
                gameObjCopy.move(gameMove, place=True)

            accualEval = algo.evaluate(gameObjCopy.state, gameObjCopy)
            simEval = (moveEval / moveBias)

            
            accuarcy = round(min(accualEval, simEval) / max(accualEval, simEval) * 100, 2)
            # stateAccuarcy = round(algo.matrixSimilarity(gameObj.state, ) / 36 * 100, 2)

            print(f"Predicted Eval/eval accuarcy: {accuarcy}% ", end="\r")
        except IndexError:
            score, highVal = gameObj.endStats()
            print(
                f"\r\n{classes.blcolors.RED}FAILED DUE TO UNKNOWN CAUSE{classes.blcolors.CLEAR}" + 
                f": moveEval: {moveEval}, moves: {moves}\r\n{gameObj.state}\r\n" +
                f"{classes.blcolors.RED}GAME OVER{classes.blcolors.CLEAR} Score: {score}, highest: {highVal}"
            )

            gameObj.clear()
            pygame.event.clear()
        algoStarted = False
    
    """
    moveEval, moves, moveBias, allEvals = algo.algo(gameObj, 3)
    try:
        gameObjCopy = copy.deepcopy(gameObj)
        gameObj.move(moves[0], place=True)
        for gameMove in moves:
            gameObjCopy.move(gameMove, place=True)

        accualEval = algo.evaluate(gameObjCopy.state, gameObjCopy)
        simEval = (moveEval / moveBias)

        
        accuarcy = round(min(accualEval, simEval) / max(accualEval, simEval) * 100, 2)
        # stateAccuarcy = round(algo.matrixSimilarity(gameObj.state, ) / 36 * 100, 2)

        print(f"Predicted Eval/eval accuarcy: {accuarcy}% ", end="\r")
    except IndexError:
        score, highVal = gameObj.endStats()
        print(
            f"\r\n{classes.blcolors.RED}FAILED DUE TO UNKNOWN CAUSE{classes.blcolors.CLEAR}" + 
            f": moveEval: {moveEval}, moves: {moves}\r\n{gameObj.state}\r\n" +
            f"{classes.blcolors.RED}GAME OVER{classes.blcolors.CLEAR} Score: {score}, highest: {highVal}"
        )

        gameObj.clear()
        pygame.event.clear()
    """

pygame.quit()