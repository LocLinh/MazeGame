from logging import root
from sys import flags
import textwrap
from tkinter import *
import tkinter
import PySimpleGUI as sg
import numpy as np
import math
from PIL import Image, ImageTk

from numpy.core.fromnumeric import size
import mazeGenerator as Maze
# constant
AppFont = 'Any 16'
sg.theme('DarkGrey5')
_VARS = {'cellCount': 31, 'gridSize': 620, 'canvas': False, 'window': False,
         'playerPos': [20, 20], 'cellMAP': False}
cellSize = _VARS['gridSize']/_VARS['cellCount']
exitPos = [_VARS['cellCount']-2, _VARS['cellCount']-2]
Grade = {'Cau1': 0, 'Cau2': 0, 'Cau3': 0}
Ans = {'Cau1': 'không chọn', 'Cau2': 'không chọn', 'Cau3': 'không chọn'}
goal = 0
visitedCells = {}
bus_stations = [ (10, 15), (21, 7), (5, 21), (24, 19)]
# light purple 0, light blue 1, light green 2, tomato 3, pink 4, yellow 5, skin 6, light grey 7
visited_colors = ['#9D84B7', '#B2F9FC', '#77D970', '#ff6347', 'pink', '#FEE440', '#ECAC5D', '#D5D5D5']
current_visited_color = 0
root = tkinter.Tk()
root.withdraw()
bus_u = PhotoImage(file="images/bus_up.png")
bus_d = PhotoImage(file="images/bus_down.png")
bus_l = PhotoImage(file="images/bus_left.png")
bus_r = PhotoImage(file="images/bus_right.png")
university_1 = PhotoImage(file="images/University_1.png")
university_2 = PhotoImage(file="images/University_2.png")
university_3 = PhotoImage(file="images/University_3.png")
university_4 = PhotoImage(file="images/University_4.png")
finish_line = PhotoImage(file="images/finish_flag.png")
# feature functions
def makeMaze(dimX, dimY):
    """makes a maze by reading maze.txt.

    Maze.txt can be modified manually or using mazeGenarate() in mazeGenerator.py
    """
    # # Add blank cells fro entrance,exit and around them:
    starterMap = Maze.readMaze()
    return starterMap

_VARS['cellMAP'] = makeMaze(_VARS['cellCount'], _VARS['cellCount'])

# METHODS:

def drawGrid():
    cells = _VARS['cellCount']
    _VARS['canvas'].TKCanvas.create_rectangle(
        1, 1, _VARS['gridSize'], _VARS['gridSize'], outline='BLACK', width=1)
    for x in range(cells):
        _VARS['canvas'].TKCanvas.create_line(
            ((cellSize * x), 0), ((cellSize * x), _VARS['gridSize']),
            fill='BLACK', width=1)
        _VARS['canvas'].TKCanvas.create_line(
            (0, (cellSize * x)), (_VARS['gridSize'], (cellSize * x)),
            fill='BLACK', width=1)


def draw_Object(x, y, img):
    # draw bus, player, finsih line
    _VARS['canvas'].TKCanvas.create_image(x+10, y+11, image=img)


def draw_player_direction(x, y, direction='Left:37'):
    # draw 4 direction of player
    if checkEvents(direction) == 'Up':
        _VARS['canvas'].TKCanvas.create_image(x+10, y+11, image=bus_u)
    elif  checkEvents(direction) == 'Down':
        _VARS['canvas'].TKCanvas.create_image(x+10, y+11, image=bus_d)
    elif  checkEvents(direction) == 'Left':
        _VARS['canvas'].TKCanvas.create_image(x+10, y+11, image=bus_l)
    elif  checkEvents(direction) == 'Right':
        _VARS['canvas'].TKCanvas.create_image(x+10, y+11, image=bus_r)
    else:
        _VARS['canvas'].TKCanvas.create_image(x+10, y+11, image=bus_l)



def drawCell(x, y, color='GREY'):
    _VARS['canvas'].TKCanvas.create_rectangle(
        x, y, x + cellSize, y + cellSize,
        outline='BLACK', fill=color, width=1)


def placeCells():
    for row in range(_VARS['cellMAP'].shape[0]):
        for column in range(_VARS['cellMAP'].shape[1]):
            if(_VARS['cellMAP'][column][row] == 1):
                drawCell((cellSize*row), (cellSize*column))


def checkEvents(event):
    move = ''
    if len(event) == 1:
        if ord(event) == 63232:  # UP
            move = 'Up'
        elif ord(event) == 63233:  # DOWN
            move = 'Down'
        elif ord(event) == 63234:  # LEFT
            move = 'Left'
        elif ord(event) == 63235:  # RIGHT
            move = 'Right'
    # Filter key press Windows :
    else:
        if event.startswith('Up'):
            move = 'Up'
        elif event.startswith('Down'):
            move = 'Down'
        elif event.startswith('Left'):
            move = 'Left'
        elif event.startswith('Right'):
            move = 'Right'
    return move


# INIT :
huongdan = sg.Image(source='images/huongdan.png')
interact_col = [
    [huongdan],
    [sg.pin(sg.Text('Tìm đường đến đích nào!!', key='content_0', font=AppFont, pad=(0, (50, 20)), visible=True))],
    [sg.pin(sg.Text('Bạn đang ở cơ sở TP. Thủ Đức\n\nBạn sẽ chọn chuyến xe nào để đi\n     đến cơ sở Nguyễn Kiệm?', key='content_1', font=AppFont, pad=(0, (50, 20)), visible=False))],
    [sg.pin(sg.Text('Bạn đang ở cơ sở Nguyễn Kiệm\n\nBạn sẽ chọn chuyến xe nào để đi\n     đến cơ sở 2C Phổ Quang?', key='content_2', font=AppFont, pad=(0, (50, 20)), visible=False))],
    [sg.pin(sg.Text('Bạn đang ở cơ sở 2C Phổ Quang\n\nBạn sẽ chọn chuyến xe nào để đi\n             đến cơ sở Q7?', key='content_3', font=AppFont, pad=(0, (50, 20)), visible=False))],
    [sg.pin(sg.Text('Bạn đang ở cơ sở Quận 7\n\n Sắp tới đích rồi!!', key='content_4', font=AppFont, pad=(0, (50, 20)), visible=False))],
    [sg.pin(sg.Text('Chúc mừng bạn đạt %s điểm!!\nĐáp án câu 1 là A, bạn %s\nĐáp án câu 2 là A, bạn %s\nĐáp án câu 3 là A, bạn %s' % (goal, Ans['Cau1'], Ans['Cau2'], Ans['Cau3']), key='content_5', font=AppFont, pad=(0, (50, 20)), visible=False))],
    [
        sg.pin(sg.Button(button_text='A. Xe 55', key='button_1_A', button_color='red', pad=((20, 20), 0), visible=False)),
        sg.pin(sg.Button(button_text='B. Xe 99' , key='button_1_B', button_color= ('black', 'pink'), pad=(20, 0), visible=False)), 
        sg.pin(sg.Button(button_text='C. Xe 150', key='button_1_C', button_color='green', pad=((20, 0), 0), visible=False))
    ],
    [
        sg.pin(sg.Button(button_text='A. Xe 07', key = 'button_2_A', button_color=('black', 'yellow'), pad=((22, 20), 0), visible=False)),
        sg.pin(sg.Button(button_text='B. Xe 55' , key='button_2_B', button_color= 'red', pad=(20, 0), visible=False)), 
        sg.pin(sg.Button(button_text='C. Xe 150', key='button_2_C', button_color='green', pad=((20, 0), 0), visible=False))
    ],
    [sg.pin(sg.Button(button_text='A. Xe 152 rồi chuyển qua xe 34', key='button_3_A', button_color='tomato', visible=False))],
    [sg.pin(sg.Button(button_text='B. Xe 104 rồi chuyển qua xe 34' , key='button_3_B', button_color='black', visible=False))],
    [sg.pin(sg.Button(button_text='C. Xe 34 rồi chuyển qua xe 20', key='button_3_C',button_color='green', visible=False))],
]

main_game_col = [
    [sg.Canvas(size=(_VARS['gridSize'], _VARS['gridSize']), background_color='white', key='canvas')],
    [sg.Exit(font=AppFont, pad=((10, 0), (0, 0))), 
        sg.Text('', key='-exit-', font=AppFont, size=(15, 1)), 
        sg.Button('Restart', font=AppFont)]
]
layout = [
    [sg.Column(main_game_col),
    sg.Column(interact_col, key='content', vertical_alignment='t', size=(330, 500))]
]

_VARS['window'] = sg.Window('Maze Game', layout, resizable=False, finalize=True,
                            return_keyboard_events=True, location=(200, 0))
_VARS['canvas'] = _VARS['window']['canvas']

def Draw():
    # draw bus stations, goal, player and walls 
    # draw everythings
    drawGrid()
    drawCell(exitPos[0]*cellSize, exitPos[1]*cellSize, 'Black')
    for item in visitedCells:
        color_idx = visitedCells[(item[0], item[1])]
        drawCell(item[0]*cellSize, item[1]*cellSize, visited_colors[color_idx])
    # draw 4 busstation
    draw_Object(bus_stations[0][0]*cellSize, bus_stations[0][1]*cellSize, university_1)
    draw_Object(bus_stations[1][0]*cellSize, bus_stations[1][1]*cellSize, university_2)
    draw_Object(bus_stations[2][0]*cellSize, bus_stations[2][1]*cellSize, university_3)
    draw_Object(bus_stations[3][0]*cellSize, bus_stations[3][1]*cellSize, university_4)
    # draw goal
    draw_Object(580, 580, finish_line)
    placeCells()

## update question if player is on a bus station
def content_available(n:int = 0, enable=True):
    if n == 0 or n == 4 or n == 5:
        _VARS['window'][f'content_{n}'].Update(visible=enable)
    else:
        _VARS['window'][f'content_{n}'].Update(visible=enable)
        _VARS['window'][f'button_{n}_A'].Update(visible=enable)
        _VARS['window'][f'button_{n}_B'].Update(visible=enable)
        _VARS['window'][f'button_{n}_C'].Update(visible=enable)

def Update_content(n = 0):
    content = [0, 1, 2, 3, 4, 5]
    for i in content:
        if i == n:
            content_available(i, True)
        else:
            content_available(i, False)


## check answer return of the questions above
def check_answer(content = 1, answer = ''):
    if not answer:
        return False
    # print(content, answer)
    if content == 1:
        if event == 'button_1_A':
            Grade['Cau1'] = 1
            Ans['Cau1'] = 'chọn đúng'
            return 3
        elif event == 'button_1_B':
            Grade['Cau1'] = 0
            Ans['Cau1'] = 'chọn B'
            return 4
        elif event == 'button_1_C':
            Grade['Cau1'] = 0
            Ans['Cau1'] = 'chọn C'
            return 2
    elif content == 2:
        if event == 'button_2_A':
            Grade['Cau2'] = 1
            Ans['Cau2'] = 'chọn đúng'
            return 5
        elif event == 'button_2_B':
            Grade['Cau2'] = 0
            Ans['Cau2'] = 'chọn B'
            return 3
        elif event == 'button_2_C':
            Grade['Cau2'] = 0
            Ans['Cau2'] = 'chọn C'
            return 2
    elif content == 3:
        if event == 'button_3_A':
            Grade['Cau3'] = 1
            Ans['Cau3'] = 'chọn đúng'
            return 6
        elif event == 'button_3_B':
            Grade['Cau3'] = 0
            Ans['Cau3'] = 'chọn B'
            return 7
        elif event == 'button_3_C':
            Grade['Cau3'] = 0
            Ans['Cau3'] = 'chọn C'
            return 2
    return False

# alow answer question flag
Q_1 = True
Q_2 = True
Q_3 = True

Draw()
draw_Object(_VARS['playerPos'][0], _VARS['playerPos'][1], bus_l)

while True:             # Event Loop
    event, values = _VARS['window'].read()
    if event in (None, 'Exit'):
        break

    if event == 'Restart':
        _VARS['playerPos'] = [20, 20]
        visitedCells = {}
        goal = 0
        Grade = {'Cau1': 0, 'Cau2': 0, 'Cau3': 0}
        current_visited_color = 0
        Q_1 = True
        Q_2 = True
        Q_3 = True
    
    # print(event)
    xPos = int(math.ceil(_VARS['playerPos'][0]/cellSize))
    yPos = int(math.ceil(_VARS['playerPos'][1]/cellSize))

    '''
        Check event move
    '''
    # check if player is answer any question
    # if true then dont alow player to move
    move_alow = Q_1 and Q_2 and Q_3

    if checkEvents(event) == 'Up':
        if int(_VARS['playerPos'][1] - cellSize) >= 0:
            if _VARS['cellMAP'][yPos-1][xPos] != 1 and move_alow:
                _VARS['playerPos'][1] = _VARS['playerPos'][1] - cellSize
    elif checkEvents(event) == 'Down':
        if int(_VARS['playerPos'][1] + cellSize) < _VARS['gridSize']-1:
            if _VARS['cellMAP'][yPos+1][xPos] != 1 and move_alow:
                _VARS['playerPos'][1] = _VARS['playerPos'][1] + cellSize
    elif checkEvents(event) == 'Left':
        if int(_VARS['playerPos'][0] - cellSize) >= 0:
            if _VARS['cellMAP'][yPos][xPos-1] != 1 and move_alow:
                _VARS['playerPos'][0] = _VARS['playerPos'][0] - cellSize
    elif checkEvents(event) == 'Right':
        if int(_VARS['playerPos'][0] + cellSize) < _VARS['gridSize']-1:
            if _VARS['cellMAP'][yPos][xPos+1] != 1 and move_alow:
                _VARS['playerPos'][0] = _VARS['playerPos'][0] + cellSize

    # save visited cells
    visitedCells[(xPos, yPos)] = current_visited_color

    # Clear canvas, draw grid and cells and visited cell
    _VARS['canvas'].TKCanvas.delete("all")
    Draw()
    draw_player_direction(_VARS['playerPos'][0], _VARS['playerPos'][1], event)
    
    # recalculate player position
    yPos = int(math.ceil(_VARS['playerPos'][1]/cellSize))
    xPos = int(math.ceil(_VARS['playerPos'][0]/cellSize))

    '''
        Answer question
    '''
    if (xPos, yPos) == bus_stations[0]:
        if Q_1:
            Update_content(1)
            Q_1 = False
        if _VARS['window']['content_1'].visible == True:
            if check_answer(1, event):
                current_visited_color = check_answer(1, event)
                Update_content(0)
                Q_1 = True
    elif (xPos, yPos) == bus_stations[1]:
        if Q_2:
            Update_content(2)
            Q_2 = False
        if _VARS['window']['content_2'].visible == True:
            if check_answer(2, event):
                current_visited_color = check_answer(2, event)
                Update_content(0)
                Q_2 = True
    elif (xPos, yPos) == bus_stations[2]:
        if Q_3:
            Update_content(3)
            Q_3 = False
        if _VARS['window']['content_3'].visible == True:
            if check_answer(3, event):
                current_visited_color = check_answer(3, event)
                Update_content(0)
                Q_3 = True
    elif (xPos, yPos) == bus_stations[3]:
        Update_content(4)
    else:
        Update_content(0)


    # Check for Exit:
    if [xPos, yPos] == exitPos:
        _VARS['window']['-exit-'].update('Found the exit !')
        Grd = 0
        for item in Grade:
            Grd += Grade[item]
        goal = Grd
        Update_content(5)
        _VARS['window']['content_5'].update('Chúc mừng bạn đạt %s điểm!!\nĐáp án câu 1 là A, bạn %s\nĐáp án câu 2 là A, bạn %s\nĐáp án câu 3 là A, bạn %s' % (goal, Ans['Cau1'], Ans['Cau2'], Ans['Cau3']))
    else:
        _VARS['window']['-exit-'].update('')

_VARS['window'].close()
