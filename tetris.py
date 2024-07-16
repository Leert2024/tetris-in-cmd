from time import sleep
from os import system
from sys import exit
from setup import *
from colorama import Fore,just_fix_windows_console
just_fix_windows_console()
from random import randint,random
from keyboard import on_press

#以下是所有可能生成的结构
'''
█ ██ ██     ██     █   █         █
█ ██   ██ ██     ███ ███ ███
█
█
'''

board = []
blocks = []
centre = (0,0)
score = 0

#call()在键盘事件发生时被调用
def call(x):
    global centre, out
    if x.event_type == 'down' and x.name == 'r':
        r_rotate()
    elif x.event_type == 'down' and x.name == 'l':
        l_rotate()

    #按down直接下落到底部
    elif x.event_type == 'down' and x.name == 'down':
        for i in range(HEIGHT):
            if try_fall() == True:
                break

    #按left左移所有可控方块
    elif x.event_type == 'down' and x.name == 'left':
        prev_pos = []
        for i in blocks:
            prev_pos.append(i.position)
        for i in blocks:
            if i.position[1] <= 0 or (board[i.position[0]][i.position[1]-1] != 0 and ((i.position[0],i.position[1]-1) not in prev_pos)):
                return 
        for i in blocks:

            #如果在界外，则方块仅更新位置，而不进行面板对应位置的重绘
            if i.position[0] < 0:
                break
            board[i.position[0]][i.position[1]] = 0
            
        for i in blocks:
            i.position = (i.position[0],i.position[1]-1)
            i.draw()
        centre = (centre[0], centre[1]-1)

    #按right右移所有可控方块
    elif x.event_type == 'down' and x.name == 'right':
        prev_pos = []
        for i in blocks:
            prev_pos.append(i.position)
        for i in blocks:
            if i.position[1] >= LENGTH - 1 or (board[i.position[0]][i.position[1]+1] != 0 and ((i.position[0],i.position[1]+1) not in prev_pos)):
                return 
        for i in blocks:
            if i.position[0] < 0:
                break
            board[i.position[0]][i.position[1]] = 0
        for i in blocks:
            i.position = (i.position[0],i.position[1]+1)
            i.draw()
        centre = (centre[0], centre[1]+1)
    elif x.event_type == 'down' and x.name == 'p':
        out = 2
    elif x.event_type == 'down' and x.name == 's':
        out = 3
    else:
        return 
        
on_press(call)

#初始化游戏面板
def init_board():
    for i in range(HEIGHT):
        layer = []
        for j in range(LENGTH):
            layer.append(0)
        board.append(layer)

class Block():
    def __init__(self, icon_num, pos):
        self.icon = icon_num
        self.position = pos
        self.draw()
        blocks.append(self)
    def draw(self):
        if self.position[0] >= 0:#若越界则跳过“重绘”
            board[self.position[0]][self.position[1]] = self.icon
        
def l_rotate():
    prev_pos = []
    for i in blocks:
        prev_pos.append(i.position)
    temp = []
    for i in blocks:
        Y = int(centre[0]-i.position[1]+centre[1])
        X = int(centre[1]+i.position[0]-centre[0])
        if X < 0 or X > LENGTH-1 or Y > HEIGHT-1 or (board[Y][X] != 0 and ((Y,X) not in prev_pos)):
            return
        temp.append(Y)
        temp.append(X)
    for i in range(4):
        if blocks[i].position[0] >= 0:
            board[blocks[i].position[0]][blocks[i].position[1]] = 0
        blocks[i].position = (temp[i*2], temp[i*2+1])
    for i in blocks:
        i.draw()
        
def r_rotate():
    prev_pos = []
    for i in blocks:
        prev_pos.append(i.position)
    temp = []
    for i in blocks:
        Y = int(centre[0]+i.position[1]-centre[1])
        X = int(centre[1]-i.position[0]+centre[0])
        if X < 0 or X > LENGTH-1 or Y > HEIGHT-1 or (board[Y][X] != 0 and ((Y,X) not in prev_pos)):
            return
        temp.append(Y)
        temp.append(X)
    for i in range(4):
        if blocks[i].position[0] >= 0:
            board[blocks[i].position[0]][blocks[i].position[1]] = 0
        blocks[i].position = (temp[i*2], temp[i*2+1])
    for i in blocks:
        i.draw()
#尝试使所有可控方块下落，能下落返回False，不能下落返回True
def try_fall():
    global centre
    prev_pos = []
    for i in blocks:
        prev_pos.append(i.position)
    for i in blocks:
        if i.position[0] >= HEIGHT - 1 or (i.position[0] >= 0 and board[i.position[0]+1][i.position[1]] != 0 and ((i.position[0]+1, i.position[1]) not in prev_pos)):
            return True
    for i in blocks:
        if i.position[0] < 0:
            break
        board[i.position[0]][i.position[1]] = 0
    for i in blocks:
        i.position = (i.position[0]+1,i.position[1])
        i.draw()
    centre = (centre[0]+1, centre[1])
    return False

#仅在try_fall()返回True时被调用，进行得分与层的消除
def try_score():
    global score
    add = 1
    for i in range(HEIGHT):
        if_score = True
        for j in range(LENGTH):
            if board[i][j] == 0:
                if_score = False
                break
        if if_score:
            score += LENGTH * add
            add += 1
            for k in range(i,-1,-1):
                if k != 0:
                    for l in range(LENGTH):
                        board[k][l] = board[k-1][l]
                else:
                    for l in range(LENGTH):
                        board[k][l] = 0
#生成随机结构
def structure():
    global block_type, centre
    block_type = randint(1,7)
    
    if block_type == 1:#1型
        X = randint(1,LENGTH - 3)
        for i in range(4):
            block = Block(1, (-1, X-1+i))
        centre = (-1.5, X+0.5)
        
    elif block_type == 2:#O型
        X = randint(0,LENGTH - 2)
        for i in range(2):
            block = Block(2, (-1-i, X))
            block = Block(2, (-1-i, X+1))
        centre = (-1.5, X+0.5)
        
    elif block_type == 3:#Z型
        X = randint(0,LENGTH - 3)
        for i in range(2):
            block = Block(3, (-1-i, X-i+1))
            block = Block(3, (-1-i, X-i+2))
        centre = (-2, X+1)
        
    elif block_type == 4:#S型
        X = randint(0,LENGTH - 3)
        for i in range(2):
            block = Block(4, (-1-i, X+i))
            block = Block(4, (-1-i, X+i+1))
        centre = (-2, X+1)
            
    elif block_type == 5:#T型
        X = randint(0,LENGTH - 3)
        for i in range(3):
            block = Block(5, (-1, X+i))
        block = Block(5, (-2, X+1))
        centre = (-1, X+1)
        
    elif block_type == 6:#J型
        X = randint(0,LENGTH - 3)
        for i in range(3):
            block = Block(6, (-1, X+i))
        block = Block(6, (-2, X))
        centre = (-1, X+1)
        
    elif block_type == 7:#L型
        X = randint(0,LENGTH - 3)
        for i in range(3):
            block = Block(7, (-1, X+i))
        block = Block(7, (-2, X+2))
        centre = (-1, X+1)
    

#用户界面输出
def print_board():
    system('cls')
    
    layer = '┌'
    for i in range(LENGTH):
        layer += '─'
    layer += '┐'
    print(layer)
        
    for i in range(HEIGHT):
        layer = '│'
        for j in range(LENGTH):
            layer += ICONS[board[i][j]]
        layer += '│'
        print(layer)

    layer = '└'
    for i in range(LENGTH):
        layer += '─'
    layer += '┘'
    print(layer)
def if_over():
    for i in blocks:
        if i.position[0] < 0:
            return True
#每隔SLEEP秒被调用一次
def update():
    global positions, blocks, out
    if try_fall():
        if if_over():
            out = 1
        try_score()
        blocks = []
        structure()
    print_board()
    print('score = ' +str(score))
    print('''Press ↓ for instant fall.
→ for right.\t← for left.
p for pause.\ts for exit.
r for clockwise rotation.\tl for anticlockwise rotation.''')

if __name__ == '__main__':
    out = 0
    init_board()
    structure()
    while out != 1:
        if out == 2:
            print('Game paused. Press enter to continue.')
            input()
            out = 0
        elif out == 3:
            exit()
        sleep(SLEEP)
        update()
    print('Game over!')
    input()
