import pygame
import numpy as np
import random
import math
from module.Network import NeuralNetwork


def getAngle(a, b, c):
    try:
        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        return np.degrees(angle)
    except:
        return 0

class BodySegment(object):
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.lastDir = ''
        self.dir = ''
    def move(self, dir, snakeBoard):
        self.dir = self.lastDir
        self.lastDir = dir
        self.erase(snakeBoard)
        if dir == 'up':
            self.pos[1] -= 1
        elif dir == 'down':
            self.pos[1] += 1
        elif dir == 'left':
            self.pos[0] -= 1
        elif dir == 'right':
            self.pos[0] += 1
        self.display(snakeBoard)

    def display(self, snakeBoard):
        #pygame.draw.rect(dis,self.color,[self.pos[0]*(lineWidth+squareSize) + lineWidth,
        #                                 self.pos[1]*(lineWidth+squareSize) + lineWidth + startBoardHeight,squareSize,squareSize])
        snakeBoard[self.pos[0]][self.pos[1]] = 1

    def erase(self, snakeBoard):
        #pygame.draw.rect(dis, black, [self.pos[0] * (lineWidth + squareSize) + lineWidth,
        #                                   self.pos[1] * (lineWidth + squareSize) + lineWidth + startBoardHeight, squareSize, squareSize])
        snakeBoard[self.pos[0]][self.pos[1]] = 0

class Snake(object):
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        body = BodySegment(color,pos)
        self.body = []
        self.body.append(body)
        self.age = 0
        self.stomach = 500
        self.isAlive = True
        self.headDir = 'up'
    def display(self, snakeBoard):
        for segment in self.body:
            segment.display(snakeBoard)
    def move(self, snakeBoard):
        self.stomach -= 1
        if self.stomach == 0:
            self.isAlive = False
            return
        self.age += 1
        if self.headDir == 'left' and (snakeBoard[self.body[0].pos[0] - 1][self.body[0].pos[1]] == 1 or self.body[0].pos[0] == 0):
            self.isAlive = False
        elif self.headDir == 'right' and (snakeBoard[self.body[0].pos[0] + 1][self.body[0].pos[1]] == 1 or self.body[0].pos[0] == numCol - 1):
            self.isAlive = False
        elif self.headDir == 'up' and (snakeBoard[self.body[0].pos[0]][self.body[0].pos[1] - 1] == 1 or self.body[0].pos[1] == 0):
            self.isAlive = False
        elif self.headDir == 'down' and (snakeBoard[self.body[0].pos[0]][self.body[0].pos[1] + 1] == 1 or self.body[0].pos[1] == numRow - 1):
            self.isAlive = False
        self.body[0].move(self.headDir,snakeBoard)
        for i in range(1,len(self.body)):
            self.body[i].move(self.body[i-1].dir,snakeBoard)
        for i in range(1,len(self.body)):
            self.body[i].lastDir = self.body[i-1].dir

    def growth(self, snakeBoard):
        tailDir = self.body[len(self.body)-1].lastDir
        newPos = [self.body[len(self.body)-1].pos[0],self.body[len(self.body)-1].pos[1]]
        if tailDir == 'up':
            newPos[1] += 1
        elif tailDir == 'down':
            newPos[1] -= 1
        elif tailDir == 'left':
            newPos[0] += 1
        elif tailDir == 'right':
            newPos[0] -= 1
        newSegment = BodySegment(self.color,newPos)
        newSegment.display(snakeBoard)
        self.body.append(newSegment)
    def death(self):
        pass

class Controller(object):
    def __init__(self):
        self.applePos = []
        self.applePos.append(0)
        self.applePos.append(0)
        self.snakeBoard = np.zeros((numCol + 1, numRow + 1))
        self.snake = self.initSnake()
        self.isShowed = False
        self.isToggled = False
        self.snakeVision = ''
        self.score = 0
    def generateApple(self):
        x = random.randint(0, numCol - 1)
        y = random.randint(0, numRow - 1)
        while self.snakeBoard[x][y] == 1:
            x = random.randint(0, numCol - 1)
            y = random.randint(0, numRow - 1)
        self.applePos[0] = x
        self.applePos[1] = y
        self.snakeBoard[x][y] = -1
    def isEatApple(self):
        snakeHead = self.snake.body[0].pos
        if snakeHead[0] == self.applePos[0] and snakeHead[1] == self.applePos[1]:
            return True
        return False
    def snakeEatApple(self):
        self.snake.stomach = 500
        self.snake.growth(self.snakeBoard)
        self.generateApple()
    def initSnake(self):
        self.snake = Snake(cyan, [10, 10])
        self.snake.display(self.snakeBoard)
        return self.snake
    def start(self, network = None):
        self.snakeBoard = np.zeros((numCol + 1, numRow + 1))
        self.snake = self.initSnake()
        self.generateApple()
        clock = pygame.time.Clock()
        isRun = True
        if network is None:
            network = NeuralNetwork()
        while isRun:
            if self.update(network) == False:
                isRun = False
            if self.isShowed == True:
                if self.isToggled == False:
                    pygame.init()
                    dis = pygame.display.set_mode((windowWidth, windowHeight))
                    self.drawBoard(dis)
                    self.drawDisplay(dis)
                    self.isToggled = True
                self.render(dis, network)
                clock.tick(20)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.snake.isAlive = False
        #print('You Died!')
        #print('Length: ' + str(len(self.snake.body)) + ' Age: ' + str(self.snake.age) + ' Stomach: ' + str(self.snake.stomach))
        self.score = self.fitness()
        return self.fitness()
    def fitness(self):
        return len(self.snake.body)*501 + self.snake.age
    def update(self, network):
        if self.snake.isAlive == False:
            return False
        for i in range(-math.ceil(numColVision / 2), math.ceil(numColVision / 2)):
            for j in range(-math.ceil(numRowVision / 2), math.ceil(numRowVision / 2)):
                x = self.snake.body[0].pos[0] + i
                y = self.snake.body[0].pos[1] + j
                if x < 0 or x >= numCol or y < 0 or y >= numRow:
                    vision[math.floor(numColVision / 2) + i][math.floor(numRowVision / 2) + j] = 1
                else:
                    vision[math.floor(numColVision / 2) + i][math.floor(numRowVision / 2) + j] = self.snakeBoard[x][y]
        appleVision = self.getAppleDirection()
        self.snakeVision = np.concatenate((np.delete(vision.reshape(1, vision.size), 24, axis=1), appleVision), axis=1)
        movement = network.filterOutput(network.forward(self.snakeVision))
        for i in range(movement.size):
            if int(movement[i]) == 1 and i == 0:
                self.snake.headDir = 'up'
                break
            elif int(movement[i]) == 1 and i == 1:
                self.snake.headDir = 'down'
                break
            elif int(movement[i]) == 1 and i == 2:
                self.snake.headDir = 'left'
                break
            else:
                self.snake.headDir = 'right'
        self.snake.move(self.snakeBoard)
        if self.isEatApple():
            self.snakeEatApple()

    def drawBoard(self, dis):
        for i in range(numRow+1):
            pygame.draw.line(dis, gray, (0, i*squareSize + i*lineWidth + startBoardHeight), (boardWidth, i*squareSize + i*lineWidth + startBoardHeight), lineWidth)
        for i in range(numCol+1):
            pygame.draw.line(dis, gray, (i * squareSize + i*lineWidth, startBoardHeight), (i * squareSize + i*lineWidth, startBoardHeight + boardHeight), lineWidth)
        pygame.display.update()

    def drawDisplay(self, dis):
        for i in range(numRowVision + 1):
            pygame.draw.line(dis, gray, (boardWidth + marginBoardWidth, i*squareSize + i*lineWidth + marginBoardHeight), (boardWidth + marginBoardWidth + numColVision*(squareSize + lineWidth), i*squareSize + i*lineWidth + marginBoardHeight), lineWidth)
        for i in range(numColVision+1):
            pygame.draw.line(dis, gray, (i * squareSize + i*lineWidth + boardWidth + marginBoardWidth, marginBoardHeight), (i * squareSize + i*lineWidth + boardWidth + marginBoardWidth, marginBoardHeight + numRowVision*(squareSize + lineWidth)), lineWidth)
        for i in range(4):
            pygame.draw.line(dis, gray, (boardWidth + marginVisionWidth, i * squareSize + i * lineWidth + marginBoardHeight + marginVisionHeight + numRowVision*(squareSize + lineWidth)),
                             (boardWidth + marginVisionWidth + 3 * (squareSize + lineWidth),
                              i * squareSize + i * lineWidth + marginBoardHeight + marginVisionHeight + numRowVision*(squareSize + lineWidth)), lineWidth)
        for i in range(4):
            pygame.draw.line(dis, gray, (i * squareSize + i * lineWidth + boardWidth + marginVisionWidth, marginBoardHeight + marginVisionHeight + numRowVision*(squareSize + lineWidth)),
                             (i * squareSize + i * lineWidth + boardWidth + marginVisionWidth,
                              marginBoardHeight + marginVisionHeight + numRowVision*(squareSize + lineWidth) + 3 * (squareSize + lineWidth)), lineWidth)


    def displayVision(self, dis):
        x = boardWidth + marginBoardWidth
        y = marginBoardHeight
        for i in range(len(vision)):
            for j in range(len(vision[i])):
                if vision[i][j] == 1:
                    pygame.draw.rect(dis, white, [x + i * (squareSize + lineWidth) + lineWidth,
                                                  y + j*(squareSize+lineWidth) + lineWidth, squareSize, squareSize])
                elif vision[i][j] == -1:
                    pygame.draw.rect(dis, red, [x + i * (squareSize + lineWidth) + lineWidth,
                                                  y + j * (squareSize + lineWidth) + lineWidth, squareSize, squareSize])
                else:
                    pygame.draw.rect(dis, black, [x + i * (squareSize + lineWidth) + lineWidth,
                                                  y + j * (squareSize + lineWidth) + lineWidth, squareSize, squareSize])

    def getAppleDirection(self):
        posHead = self.snake.body[0].pos
        upVector = np.array([posHead[0], 0])
        headVector = np.array([posHead[0], posHead[1]])
        appleVector = np.array([self.applePos[0], self.applePos[1]])
        angle = getAngle(upVector, headVector, appleVector)
        applePosition = 0
        if angle >= 157.5:
            applePosition = 4
        elif angle >= 112.5:
            if posHead[0] < self.applePos[0]:
                applePosition = 3
            else:
                applePosition = 5

        elif angle >= 67.5:
            if posHead[0] < self.applePos[0]:
                applePosition = 2
            else:
                applePosition = 6

        elif angle >= 22.5:
            if posHead[0] < self.applePos[0]:
                applePosition = 1
            else:
                applePosition = 7

        else:
            applePosition = 0

        vectorizePosition = np.zeros((1, 8))
        vectorizePosition[0][applePosition] = 1

        return vectorizePosition

    def displayAppleDirection(self, appleVision, dis):
        x = boardWidth + marginVisionWidth
        y = marginBoardHeight + marginVisionHeight + numRowVision * (squareSize + lineWidth) + lineWidth
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(dis, black, [x + i * (squareSize + lineWidth) + lineWidth,
                                              y + j * (squareSize + lineWidth), squareSize, squareSize])
        index = np.where(appleVision == 1)[1][0]
        if index == 0:
            pygame.draw.rect(dis, red, [x + 1 * (squareSize + lineWidth) + lineWidth,
                                        y + 0 * (squareSize + lineWidth), squareSize, squareSize])
        elif index == 1:
            pygame.draw.rect(dis, red, [x + 2 * (squareSize + lineWidth) + lineWidth,
                                        y + 0 * (squareSize + lineWidth), squareSize, squareSize])
        elif index == 2:
            pygame.draw.rect(dis, red, [x + 2 * (squareSize + lineWidth) + lineWidth,
                                        y + 1 * (squareSize + lineWidth), squareSize, squareSize])
        elif index == 3:
            pygame.draw.rect(dis, red, [x + 2 * (squareSize + lineWidth) + lineWidth,
                                        y + 2 * (squareSize + lineWidth), squareSize, squareSize])
        elif index == 4:
            pygame.draw.rect(dis, red, [x + 1 * (squareSize + lineWidth) + lineWidth,
                                        y + 2 * (squareSize + lineWidth), squareSize, squareSize])
        elif index == 5:
            pygame.draw.rect(dis, red, [x + 0 * (squareSize + lineWidth) + lineWidth,
                                        y + 2 * (squareSize + lineWidth), squareSize, squareSize])
        elif index == 6:
            pygame.draw.rect(dis, red, [x + 0 * (squareSize + lineWidth) + lineWidth,
                                        y + 1 * (squareSize + lineWidth), squareSize, squareSize])
        elif index == 7:
            pygame.draw.rect(dis, red, [x + 0 * (squareSize + lineWidth) + lineWidth,
                                        y + 0 * (squareSize + lineWidth), squareSize, squareSize])

    def render(self, dis, network):
        network.render(dis, self.snakeVision, [800, 325])
        self.displayAppleDirection(self.getAppleDirection(),dis)
        self.displayVision(dis)
        for i in range(numCol):
            for j in range(numRow):
                if self.snakeBoard[i][j] == 0:
                    color = black
                elif self.snakeBoard[i][j] == 1:
                    color = cyan
                else:
                    color = red
                pygame.draw.rect(dis, color, [i * (lineWidth + squareSize) + lineWidth,
                                      j * (lineWidth + squareSize) + lineWidth + startBoardHeight, squareSize, squareSize])
        pygame.display.update()

red = (255,0,0)
cyan = (0,255,255)
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
gray = (200,200,200)

squareSize = 25
lineWidth = 2
numRow = 20
numCol = 20
numRowVision = 7
numColVision = 7
vision = np.zeros((numColVision,numRowVision))
startBoardHeight = 50
marginBoardHeight = 100
marginBoardWidth = 30
marginVisionHeight = 100
marginVisionWidth = 84
boardHeight = lineWidth*numRow + squareSize*numRow
windowHeight = 650
boardWidth = lineWidth*numCol + squareSize*numCol
windowWidth = 1300
