import pygame
import math
import copy
import sys
import time

def player(board):
    count = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != 0:
                count += 1
    if count%2 == 0:
        return "X"
    else: 
        return "O"


def actions(board):
    possible_actions = []
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 0:
                possible_actions.append([y,x])
    return possible_actions

def result(board, action):
    player_move = player(board)
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player_move
    return new_board


def winner(board):
    if board[0][0] != 0 and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif  board[0][2] != 0 and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    for x in range(len(board)):
        if board[x][0] != 0 and board[x][0] == board[x][1] and board[x][1] == board[x][2]:
            return board[x][0]
        elif board[0][x] != 0 and board[0][x] == board[1][x] and board[1][x] == board[2][x]:
            return board[0][x]
    return None



def terminal(board):
    if winner(board):
        return True
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]  == 0:
                return False
    return True


def utility(board):
    win = winner(board)
    if win == "X":
        return 1
    elif win == "O":
        return -1
    else:
        return 0


def minimax(board):
    if player(board) == "X":
        v = -math.inf
        for action in actions(board):
            k = min_value(result(board, action))
            if k == 1:
                bestmove = action
                break
            if k>v:
                v=k
                bestmove = action
    else:
        v = math.inf
        for action in actions(board):
            k = max_value(result(board, action ))
            if k == -1:
                bestmove = action
                break
            if k<v:
                v=k
                bestmove = action
    return bestmove

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v,min_value(result(board, action )))
        if v == 1:
            return v
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v,max_value(result(board, action )))
        if v == -1:
            return v
    return v


pygame.init()
color = (0,0, 0)
screen = pygame.display.set_mode((700,500)) #300, 300 - 600, 400
screen.fill(color)
pygame.display.set_caption('Tic Tac Toe')

Game = [[0,0,0],
        [0,0,0],
        [0,0,0]]

def drawGrid():
    blockSize = 100 #Set the size of the grid block
    for x in range(4):
        pygame.draw.line(screen,(255,255,255),(x*blockSize+200, 50), (x*blockSize +200, 350), 5)
        pygame.draw.line(screen,(255,255,255),(200, 50+x*blockSize), (500 , 50+x*blockSize), 5)

def DrawX(x,y):
    blockSize = 100
    pygame.draw.line(screen,(255,255,255),(x*blockSize+235,y*blockSize+75), (x*blockSize+265, y*blockSize+125), 5)
    pygame.draw.line(screen,(255,255,255),(x*blockSize+265,y*blockSize+75), (x*blockSize+235 , y*blockSize+125), 5)
def DrawO(x,y):
    blockSize = 100
    pygame.draw.circle(screen,(255,255,255),(x*blockSize+250,y*blockSize+100),25)
    pygame.draw.circle(screen,(0,0,0),(x*blockSize+250,y*blockSize+100),20)
def drawButton(text):
    pygame.draw.rect(screen,(255,255,255),(220,370,260,85))
    pygame.draw.rect(screen,(0,0,0),(225,375,250,75))
    font = pygame.font.Font('freesansbold.ttf',40)
    message = font.render(text,True,(255,255,255))
    screen.blit(message,(242,395))

def AIscore():
    font = pygame.font.Font('freesansbold.ttf',32)
    score = font.render('AI Score: ' + str(AI),True,(255,255,255))
    screen.blit(score,(500,10))
def Playerscore():
    font = pygame.font.Font('freesansbold.ttf',32)
    score = font.render('Player Score: ' + str(playercount),True,(255,255,255))
    screen.blit(score,(10,10))


running = True
start = True
playagain = False
yourturn = True
gamenumber = 0
playercount = 0
AI = 0
Game = [[0,0,0],
        [0,0,0],
        [0,0,0]]

while running:
    drawGrid()
    AIscore()
    Playerscore()
    if gamenumber % 2 == 0:
        human = "X"
    else:
        human ="O" 

    if terminal(Game):
        drawButton("Game Over")
        pygame.display.update()
        time.sleep(1)
        if utility(Game) == 1:
            if human == "X":
                playercount += 1
            else:
                AI +=1
        if utility(Game) == -1:
            if human == "X":
                AI += 1
            else:
                playercount +=1
        Game = [[0,0,0],
        [0,0,0],
        [0,0,0]]
        gamenumber += 1
        playagain = True
        screen.fill([0,0,0])

    if start:
        drawButton("Play Game")
    elif playagain:
        drawButton("Play Again")
    else:
        if player(Game) == human:
             drawButton(" Your Turn")
        else:
            drawButton("AI Thinking")
    
    if not start and not playagain:       
        if player(Game) != human:
            time.sleep(0.5)
            bestmove = minimax(Game)
            if human == "X":
                DrawO(bestmove[1],bestmove[0])
            else:
                DrawX(bestmove[1],bestmove[0])
            Game = result(Game,bestmove)
            yourturn = True
            pygame.event.clear(eventtype=pygame.MOUSEBUTTONDOWN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start or playagain:
                x,y = event.pos
                if (x>225 and x<475) and (y>375 and y<450):
                    start = False
                    if playagain and human == "O":
                        drawButton("AI Thinking")
                        yourturn = False
                    playagain = False
            elif yourturn:
                x,y = event.pos
                if (x>200 and x<500) and (y>50 and y<350):
                    blockSize = 100
                    x = ((x-200 )// blockSize) 
                    y = ((y-50)// blockSize)
                    if player(Game) == human and not Game[y][x]: 
                        Game[y][x] = human
                        if human == "X":
                            DrawX(x,y)
                        else:
                            DrawO(x,y)
                        drawButton("AI Thinking")
                        yourturn = False

    pygame.display.update()