# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 15:52:54 2017

@author: Wenchang
"""
import numpy as np

good = list( range(1,10) )
blank = []
newCoords = []
solutionSpace = {():[]}

def viewPuzzle(m, newCoords):
    print('现在的样子：')
    for i in range(9):
        for j in range(9):
            if [i,j] in newCoords:
                print('|' + str(m[i][j]) + '|', end = ''),
            else:
                print(' ' + str(m[i][j]) + ' ', end = ''),
                         
        print()

def viewSolutionSpace():
    for key in solutionSpace.keys():
                print( str(key) + ':' + str(solutionSpace[key]))

def getBlockListCoords(m, rowID, colID):
    coords = []
    for i in range ( int(rowID/3)*3, int(rowID/3)*3 + 3 ):
        for j in range ( int(colID/3)*3, int(colID/3)*3 + 3 ):
            coords.append( [i,j] )
    return coords

def getBlockList(m, rowID, colID):
    blockList = []
    for coord in getBlockListCoords(m, rowID, colID):
            blockList.append(m[coord[0]][coord[1]])
    return blockList

def getCol(m, colID):
    col = []
    for i in range(9):
        col.append(m[i][colID])
    return col

def getRow(m, rowID):
    row = []
    for i in range(9):
        row.append(m[rowID][i])
    return row

def checkCol(m,colID):
    col = getCol(m, colID)
    col.sort
    return col == good

def checkRow(m,rowID):
    row = getRow(m, rowID)
    row.sort
    return row == good

def checkBlock(m, rowID, colID):
    blockList = getBlockList(m, rowID, colID)
    return blockList == good

def isPossible(m,rowID, colID, x):
    blockList = getBlockList(m, rowID, colID)
    row = getRow(m, rowID)
    col = getCol(m, colID)
    if (x in blockList or x in row or x in col or x not in good):
        return False
    else:
        return True

def getPossible(m, rowID, colID):
    possibleX = []
    if m[rowID][colID] == 0:
        for x in good:
            if(isPossible(m,rowID, colID, x)):
                possibleX.append(x)
        if len( possibleX ) == 0:
            raise Exception('此空无解，坐标({:2},{:2})'.format(rowID, colID))
    else:
        raise Exception('已经填了，坐标({:2},{:2})'.format(rowID, colID))
    return possibleX

def getSolverState(m):
        return 81 - len(np.nonzero(m)[0])

def updateSolutionSpace(m):
    blank.clear()
    newCoords.clear()
    solutionSpace.clear()
    #更新空格列表
    for i in range(9):
        for j in range(9):
            if(m[i][j]==0):
                blank.append([i,j])
    #更新解空间
    for coord in blank:
        solutionSpace[tuple(coord)] = getPossible(m,coord[0],coord[1])

def solveByCoord(m):
    #更新空格坐标和解空间
    updateSolutionSpace(m)
    for coord in blank:
        if( len( solutionSpace.get( tuple(coord) ) ) == 1 ):
            m[coord[0]][coord[1]] = solutionSpace.get( tuple(coord) )[0]
    return getSolverState(m)
    

def fillUnit(m, unitCoords):
    valueList = []
    for coord in unitCoords:
        valueList.append(m[coord[0]][coord[1]])
    if len( np.nonzero(valueList)[0] ) != 9:
        residual = list( set(good+[0,]) - set(valueList)  )
        for x in residual:
            possibleCoords = []
            for coord in unitCoords:
                if coord in blank and x in solutionSpace[tuple(coord)]:
                    possibleCoords.append(coord)
            if len( possibleCoords ) == 1:
                m[possibleCoords[0][0]][possibleCoords[0][1]] = x

def solveByCompletion(m):
    #更新空格坐标和解空间
    updateSolutionSpace(m)
    #检查行完整性
    for i in range(9):
        rowCoords = []
        for j in range(9):
            rowCoords.append([i,j])
        fillUnit(m, rowCoords)
    #更新空格坐标和解空间
    updateSolutionSpace(m)
    #检查列完整性
    for i in range(9):
        colCoords = []
        for j in range(9):
            colCoords.append([j,i])
        fillUnit(m, colCoords)
    #更新空格坐标和解空间
    updateSolutionSpace(m)
    #检查块完整性
    for i in range(1,7+3,3):
        for j in range(1,7+3,3):
            blockCoords = getBlockListCoords(m, i, j)
            fillUnit(m, blockCoords)
    #更新空格坐标和解空间
    updateSolutionSpace(m)
    return getSolverState(m)

def solveByCompletionPath(m):
    zeroNumber = 81 - len(np.nonzero(m)[0])
    while zeroNumber > 0:
        #更新空格坐标和解空间
        updateSolutionSpace(m)
        

m = []
for i in range(9):
    m.append([])
    for j in range(9):
         m[i].append(0)

m1 = [[0,3,5,0,0,0,0,1,0],
      [9,0,0,0,0,0,0,0,0],
      [0,2,6,0,3,0,9,8,7],
      [0,0,7,6,1,0,4,0,0],
      [5,9,1,0,7,0,8,2,6],
      [0,0,4,0,9,8,5,0,0],
      [7,5,2,0,4,0,1,6,0],
      [0,0,0,0,0,0,0,0,9],
      [0,1,0,0,0,0,2,3,0]
         ]

m2 = [[0,0,0,3,0,0,0,0,9],
     [0,0,0,0,0,9,8,0,4],
     [0,8,0,2,0,0,6,5,0],
     [0,6,0,0,0,0,9,0,5],
     [7,0,3,0,0,0,2,0,6],
     [9,0,2,0,0,0,0,4,0],
     [0,4,5,0,0,1,0,7,0],
     [8,0,1,7,0,0,0,0,0],
     [2,0,0,0,0,6,0,0,0],
        ]

m3 = [[0,9,8,0,0,3,0,0,0],
     [5,0,0,0,2,0,0,0,0],
     [0,0,0,0,0,4,0,5,9],
     [0,0,2,1,0,0,0,9,0],
     [0,0,7,0,4,0,5,0,0],
     [0,6,0,0,0,7,8,0,0],
     [3,7,0,4,0,0,0,0,0],
     [0,0,0,0,3,0,0,0,6],
     [0,0,0,5,0,0,1,7,0]
        ]

m = m3

viewPuzzle(m,[])

zeroNumber = 81 - len(np.nonzero(m)[0])

while(zeroNumber > 0):
    _zeroNumber = solveByCoord(m)
    __zeroNumber = solveByCompletion(m)
    if __zeroNumber == zeroNumber:
        zeroNumber = __zeroNumber
        print('还剩{:2}个数字没有填'.format(zeroNumber))
        break
    else:
        print('按空格填了{:2}个，按完成度填了{:2}个'.format(zeroNumber-_zeroNumber, _zeroNumber - __zeroNumber))
        zeroNumber = _zeroNumber


viewPuzzle(m,[])
updateSolutionSpace(m)
viewSolutionSpace()