from pickle import TRUE
import pygame
import classes
import algo
import threading
import time

RUN_ALGO_TIMES = 10
CUR_RUN = 1
ALGO_RESULTS = list()
TEST_AI_STATE = True

class AlgoResult:
    def __init__(self, endState, endScore, endHigh):
        self.endState = endState
        self.endScore = endScore
        self.endHigh = endHigh

pygame.init()

screen = pygame.display.set_mode([300, 300])

gridObj = classes.gameGrid()
gameObj = classes.game()

gameObj.placeRandomNumb(True)
gameObj.placeRandomNumb(True)

print("\r\n\r\n")

running = True
while running:
    if CUR_RUN == RUN_ALGO_TIMES:
        if not TEST_AI_STATE:
            TEST_AI_STATE = True
            CUR_RUN = 1
        else:
            running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0)) # Clears screen
    gridObj.update(gameObj.state)

    if len(gameObj.find_valid_moves()) == 0:
        score, highVal = gameObj.endStats()
        print(f"{CUR_RUN}) {classes.blcolors.RED}GAME OVER{classes.blcolors.CLEAR} Score: {score}, highest: {highVal}")

        ALGO_RESULTS.append(AlgoResult(gameObj.state, score, highVal))

        gameObj.clear()
        pygame.event.clear()
        CUR_RUN += 1

    score, highVal = gameObj.endStats()
    print(f"{classes.blcolors.GREEN}RUNING{classes.blcolors.CLEAR} Score: {score}, highest: {highVal}", end="\r")

    moveEval, moves = algo.algo(gameObj, 3, ENABLE_2_4_ADDING=TEST_AI_STATE)
    try:
        gameObj.move(moves[0], place=True)
    
    except IndexError:
        score, highVal = gameObj.endStats()
        print(
            f"{classes.blcolors.RED}FAILED DUE TO UNKNOWN CAUSE{classes.blcolors.CLEAR}" + 
            f": moveEval: {moveEval}, moves: {moves}\r\n{gameObj.state}\r\n" +
            f"{CUR_RUN}) {classes.blcolors.RED}GAME OVER{classes.blcolors.CLEAR} Score: {score}, highest: {highVal}"
        )
        ALGO_RESULTS.append(AlgoResult(gameObj.state, score, highVal))

        gameObj.clear()
        pygame.event.clear()
        CUR_RUN += 1

    # x = threading.Thread(target=algo.asyncAlgo, args=(gameObj, 3, gameObj.move), daemon=True)
    # x.start()

pygame.quit()