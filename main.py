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

    moveEval, moves, moveBias, allEvals, bestState = algo.algo(gameObj, 3)
    try:
        gameObjCopy = copy.deepcopy(gameObj)
        gameObj.move(moves[0], place=True)
        for gameMove in moves:
            gameObjCopy.move(gameMove, place=True)

        accualEval = algo.evaluate(gameObjCopy.state, gameObjCopy)
        simEval = (moveEval / moveBias)

        # print(bestState)
        accuarcy = round(min(accualEval, simEval) / max(accualEval, simEval) * 100, 2)
        stateAccuarcy = round(algo.matrixSimilarity(gameObjCopy.state, bestState) / 36 * 100, 2)

        print(f"Predicted Eval/eval accuarcy: {accuarcy}% | State accuracy: {stateAccuarcy}%", end="\r")
    except IndexError:
        score, highVal = gameObj.endStats()
        print(
            f"\r\n{classes.blcolors.RED}FAILED DUE TO UNKNOWN CAUSE{classes.blcolors.CLEAR}" + 
            f": moveEval: {moveEval}, moves: {moves}\r\n{gameObj.state}\r\n" +
            f"{classes.blcolors.RED}GAME OVER{classes.blcolors.CLEAR} Score: {score}, highest: {highVal}"
        )

        gameObj.clear()
        pygame.event.clear()

pygame.quit()