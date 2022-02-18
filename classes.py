import imp
from random import randint
import re
from turtle import width
import pygame
import copy
import time


class blcolors:
    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    CLEAR = "\u001b[0m"

class game:
    def __init__(self, state=None):
        self.state = [[0 for x in range(4)] for y in range(4)]
        if state != None and type(state) == list:
            if len(state) == 4:
                self.state = state
    
    def placeNumb(self, numb, x, y):
        # print(f"{blcolors.CYAN}PLACING {numb} at ({x}, {y}){blcolors.CLEAR}")
        self.state[y][x] = numb

    def placeRandomNumb(self, first=False):
        if len(self.find_valid_moves()) == 0 and not first:
            print(f"{blcolors.RED}GAME OVER{blcolors.CLEAR}")
            print(self.state)
            time.sleep(2)
            self.clear()
            return False
        
        x = randint(0, 3)
        y = randint(0, 3)
        if self.state[y][x] == 0:
            rand = randint(0, 9)
            if rand == 9:
                self.placeNumb(4, x, y)
            else:
                self.placeNumb(2, x, y)
            # print(f"{blcolors.RED}{self.state[0]}\r\n{self.state[1]}\r\n{self.state[2]}\r\n{self.state[3]}{blcolors.CLEAR}\r\n")
        else:
            self.placeRandomNumb()
        return True
    
    def find_availible_sqrs(self, state=None):
        if state is None:
            state = self.state
        
        for row in state:
            if 0 in row:
                return True
        return False

    def find_valid_moves(self):
        validMoves = list()
        for move in ["d", "u", "r", "l"]:
            if self.move(move, False):
                validMoves.append(move)
        return validMoves

    def clear(self):
        self.state = [[0 for x in range(4)] for y in range(4)]
        self.placeRandomNumb(True)
        self.placeRandomNumb(True)

    def endStats(self):
        totalScore = 0
        highestScore = 0
        for y in self.state:
            for x in y:
                totalScore += x
                if x > highestScore:
                    highestScore = x
        return totalScore, highestScore


    def move(self, dir, save=True, place=False):
        state = copy.deepcopy(self.state)
        if dir == "d":
            newState = self.move_down(state)
        elif dir == "u":
            newState = self.move_up(state)
        elif dir == "r":
            newState = self.move_right(state)
        elif dir == "l":
            newState = self.move_left(state)
        else:
            return False
        if str(self.state) != str(newState):
            if save:
                self.state = newState
            if place:
                self.placeRandomNumb()
            return True
        # print(f"{blcolors.RED}INVALID MOVE{blcolors.CLEAR}")
        return False
    
    def move_down(self, state):
        alreadyCombined = list()
        for x in range(4): # Go through cols
            for y in range(2, -1, -1): # Go through cols from bottom to top
                if state[y][x] != 0:
                    for moveIndex in range(y + 1, 4, 1):
                        if state[moveIndex][x] == 0:
                            state[moveIndex][x] = state[moveIndex - 1][x]
                            state[moveIndex - 1][x] = 0
                            if (x, moveIndex - 1) in alreadyCombined:
                                alreadyCombined[alreadyCombined.index((x, moveIndex - 1))] = (x, moveIndex)
                        elif state[moveIndex][x] == state[moveIndex - 1][x]:
                            if (x, moveIndex) not in alreadyCombined and (x, moveIndex - 1) not in alreadyCombined:
                                state[moveIndex][x] = state[moveIndex - 1][x] * 2
                                state[moveIndex - 1][x] = 0
                                alreadyCombined.append((x, moveIndex))
        return state
    
    def move_up(self, state):
        alreadyCombined = list()
        for x in range(4): # Go through cols
            for y in range(1, 4, 1): # Go through cols from top to bottom
                if state[y][x] != 0:
                    for moveIndex in range(y - 1, -1, -1): # Goes up
                        if state[moveIndex][x] == 0:
                            state[moveIndex][x] = state[moveIndex + 1][x]
                            state[moveIndex + 1][x] = 0
                            if (x, moveIndex + 1) in alreadyCombined:
                                alreadyCombined[alreadyCombined.index((x, moveIndex + 1))] = (x, moveIndex)
                        elif state[moveIndex][x] == state[moveIndex + 1][x]:
                            if (x, moveIndex) not in alreadyCombined and (x, moveIndex + 1) not in alreadyCombined:
                                state[moveIndex][x] = state[moveIndex + 1][x] * 2
                                state[moveIndex + 1][x] = 0
                                alreadyCombined.append((x, moveIndex))
        return state
    
    def move_right(self, state):
        alreadyCombined = list()
        for y in range(4): # Go through rows
            for x in range(2, -1, -1): # Go through rows from right to left
                if state[y][x] != 0:
                    for moveIndex in range(x + 1, 4, 1): # Goes right
                        if state[y][moveIndex] == 0:
                            state[y][moveIndex] = state[y][moveIndex - 1]
                            state[y][moveIndex - 1] = 0
                            if (moveIndex - 1, y) in alreadyCombined:
                                alreadyCombined[alreadyCombined.index((moveIndex - 1, y))] = (moveIndex, y)
                        elif state[y][moveIndex] == state[y][moveIndex - 1]:
                            if (moveIndex, y) not in alreadyCombined and (moveIndex - 1, y) not in alreadyCombined:
                                state[y][moveIndex] = state[y][moveIndex - 1] * 2
                                state[y][moveIndex - 1] = 0
                                alreadyCombined.append((moveIndex, y))
        return state
    
    def move_left(self, state):
        alreadyCombined = list()
        for y in range(4): # Go through rows
            for x in range(1, 4, 1): # Go through rows from left to right
                if state[y][x] != 0:
                    for moveIndex in range(x - 1, -1, -1): # Goes left
                        if state[y][moveIndex] == 0:
                            state[y][moveIndex] = state[y][moveIndex + 1]
                            state[y][moveIndex + 1] = 0
                            if (moveIndex + 1, y) in alreadyCombined:
                                alreadyCombined[alreadyCombined.index((moveIndex + 1, y))] = (moveIndex, y)
                        elif state[y][moveIndex] == state[y][moveIndex + 1]:
                            if (moveIndex, y) not in alreadyCombined and (moveIndex + 1, y) not in alreadyCombined:
                                state[y][moveIndex] = state[y][moveIndex + 1] * 2
                                state[y][moveIndex + 1] = 0
                                alreadyCombined.append((moveIndex, y))
        return state



class gameGrid:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.font = pygame.font.SysFont('Comic Sans MS', 24)

    def update(self, state):
        self.make_grid(state)

    def make_grid(self, state):
        # Verticals
        padding = 10
        distance = (self.area.width - (padding * 2)) / 4
        for lineIndex in range(5):
            pygame.draw.line(
                self.screen, 
                pygame.color.Color(255,255,255), 
                (distance * lineIndex + padding, padding), 
                (distance * lineIndex + padding, self.area.height - padding),
                width = 5,
            )
            
        for lineIndex in range(5):
            pygame.draw.line(
                self.screen, 
                pygame.color.Color(255,255,255), 
                (padding, distance * lineIndex + padding), 
                (self.area.height - padding, distance * lineIndex + padding),
                width = 5,
            )
        for y in range(4):
            for x in range(4):
                textsurface = self.font.render(str(state[y][x]), False, (255,255,255))
                centerTitle = textsurface.get_rect(
                    center=(distance * (x+1) + padding - distance / 2, distance * (y+1) + padding - distance / 2)
                )
                self.screen.blit(textsurface, centerTitle)
        pygame.display.flip()

