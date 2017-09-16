# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 15:52:54 2017

@author: Wenchang
"""
import numpy as np

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

GOOD = list( range(1,10) )

import itertools
def viewPuzzle(m, newCoordinates, guessCoords):
    keys = list(newCoordinates.keys())
    for i in range(9):
        for j in range(9):
            if [i, j] in list(itertools.chain.from_iterable(newCoordinates.values())):
                if [i,j] in newCoordinates[keys[0]]:
                    print(' ' + bcolors.UNDERLINE + bcolors.BOLD + bcolors.OKGREEN + str(m[i][j]) + bcolors.ENDC, end = ' '),
                elif [i,j] in newCoordinates[keys[1]]:
                    print(' ' + bcolors.UNDERLINE + bcolors.BOLD + bcolors.OKBLUE + str(m[i][j]) + bcolors.ENDC, end=' '),
                else:
                    print(' X', end=' '),
            elif [i, j] in guessCoords:
                print(' ' + bcolors.UNDERLINE + bcolors.BOLD + bcolors.WARNING + str(m[i][j]) + bcolors.ENDC, end=' '),
            elif m[i][j] == 0:
                print(' _', end=' '),
            else:
                print(' ' + str(m[i][j]), end = ' '),
        print()

def viewBlank(m):
    solutionSpace = updateSolutionSpace(m)
    for i in range(9):
        for j in range(9):
            if m[i][j] == 0:
                possibleCount = len( solutionSpace[tuple([i,j])] )
                print(' ' + bcolors.UNDERLINE + bcolors.BOLD + bcolors.FAIL + str(possibleCount) + bcolors.ENDC, end = ' '),
            else:
                print(' ' + str(m[i][j]), end=' '),
        print()

def viewSolutionSpace():
    solutionSpace = updateSolutionSpace(m)
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
    col.sort()
    return col == GOOD

def checkRow(m,rowID):
    row = getRow(m, rowID)
    row.sort()
    return row == GOOD

def checkBlock(m, rowID, colID):
    blockList = getBlockList(m, rowID, colID)
    return blockList == GOOD

def isPossible(m,rowID, colID, x):
    blockList = getBlockList(m, rowID, colID)
    row = getRow(m, rowID)
    col = getCol(m, colID)
    if (x in blockList or x in row or x in col or x not in GOOD):
        return False
    else:
        return True

def getPossible(m, rowID, colID):
    possibleX = []
    if m[rowID][colID] == 0:
        for x in GOOD:
            if(isPossible(m,rowID, colID, x)):
                possibleX.append(x)
        if len( possibleX ) == 0:
            raise Exception('此空无解，坐标({:2},{:2})'.format(rowID, colID))
    else:
        raise Exception('已经填了，坐标({:2},{:2})'.format(rowID, colID))
    return possibleX

def getZeroNumber(m):
        return 81 - len(np.nonzero(m)[0])

def getBlankCoord(m):
    blank = []
    blank.clear()
    for i in range(9):
        for j in range(9):
            if(m[i][j]==0):
                blank.append([i,j])
    return blank

def updateSolutionSpace(m):
    solutionSpace = {}
    solutionSpace.clear()
    #更新空格列表
    blank = getBlankCoord(m)
    #更新解空间
    for coord in blank:
        solutionSpace[tuple(coord)] = getPossible(m,coord[0],coord[1])
    return solutionSpace

def solveByCoord(m):
    newCoordinates = []
    # 更新空格列表
    blank = getBlankCoord(m)
    #更新空格坐标和解空间
    solutionSpace = updateSolutionSpace(m)
    for coord in blank:
        if( len( solutionSpace.get( tuple(coord) ) ) == 1 ):
            m[coord[0]][coord[1]] = solutionSpace.get( tuple(coord) )[0]
            newCoordinates.append(coord)
    return (m,newCoordinates)


def fillUnit(m, unitCoords):
    valueList = []
    newCoordinates = []
    blank = getBlankCoord(m)
    solutionSpace = updateSolutionSpace(m)
    for coord in unitCoords:
        valueList.append(m[coord[0]][coord[1]])
    if len( np.nonzero(valueList)[0] ) != 9:
        residual = list( set(GOOD+[0,]) - set(valueList)  )
        for x in residual:
            possibleCoords = []
            for coord in unitCoords:
                if coord in blank and x in solutionSpace[tuple(coord)]:
                    possibleCoords.append(coord)
            if len( possibleCoords ) == 1:
                m[possibleCoords[0][0]][possibleCoords[0][1]] = x
                newCoordinates.append(possibleCoords[0])
    return (m, newCoordinates)

def solveByCompletion(m):
    newCoordinates = []
    #更新空格坐标和解空间
    solutionSpace = updateSolutionSpace(m)
    #检查行完整性
    for i in range(9):
        rowCoords = []
        for j in range(9):
            rowCoords.append([i,j])
        (m, _newCoords) = fillUnit(m, rowCoords)
        newCoordinates = newCoordinates + _newCoords
    #更新空格坐标和解空间
    solutionSpace = updateSolutionSpace(m)
    #检查列完整性
    for i in range(9):
        colCoords = []
        for j in range(9):
            colCoords.append([j,i])
        (m,_newCoords) = fillUnit(m, colCoords)
        newCoordinates = newCoordinates + _newCoords
    #更新空格坐标和解空间
    solutionSpace = updateSolutionSpace(m)
    #检查块完整性
    for i in range(1,7+3,3):
        for j in range(1,7+3,3):
            blockCoords = getBlockListCoords(m, i, j)
            (m, _newCoords) = fillUnit(m, blockCoords)
            newCoordinates = newCoordinates + _newCoords
    #更新空格坐标和解空间
    solutionSpace = updateSolutionSpace(m)
    return (m, newCoordinates)

def fill(m):
    zeroNumber = getZeroNumber(m)
    while (zeroNumber > 0):
        newCoordinates = {}
        zeros = [0, 0]
        (m,newCoordinates['byCoords']) = solveByCoord(m)
        zeros[0] = getZeroNumber(m)
        (m, newCoordinates['byCompletion']) = solveByCompletion(m)
        zeros[1] = getZeroNumber(m)
        if zeros[-1] == zeroNumber:  # 沒法填了
            if zeroNumber == 0:
                print('填完了,Yeah!')
            else:
                print('还剩{:2}个数字没有填'.format(zeroNumber))
            viewBlank(m)
            break
        else:
            print('按空格填了{:2}个，按完成度填了{:2}个，還剩下{:2}個'.format(len(newCoordinates['byCoords']), len(newCoordinates['byCompletion']), zeros[-1]))
            viewPuzzle(m, newCoordinates, [])
        zeroNumber = zeros[-1]
    return (m, zeroNumber)

import copy
def guess(m):
    solutionSpace = updateSolutionSpace(m)
    minSolutionKey = getMinSolutionKey(solutionSpace)
    m_copy = copy.deepcopy(m)
    for guessValue in solutionSpace[minSolutionKey]:
        m = copy.deepcopy(m_copy)
        print('猜測在({:2},{:2})，應該填寫{:2}'.format(minSolutionKey[0],minSolutionKey[1],guessValue))
        m[minSolutionKey[0]][minSolutionKey[1]] = guessValue
        viewPuzzle(m, {}, [list(minSolutionKey)])
        try:
            (m, zeroNumber) = fill(m)
            if zeroNumber == 0:
                print('通過猜測填完了')
                break
            else:
                print('再猜一次')
                m = guess(m)
        except Exception as e:
            print(e)
            print('猜錯了')
    return m

def getMinSolutionKey(solutionSpace):
    minSolutionKey = list(solutionSpace.keys())[0]
    minSolutionLength = len(solutionSpace[minSolutionKey])
    for solutionKey in solutionSpace.keys():
        if len(solutionSpace[solutionKey]) < minSolutionLength:
            minSolutionKey = solutionKey
            minSolutionLength = len(solutionSpace[solutionKey])
    return minSolutionKey

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

m_Evil =[
    [0,0,0,0,0,9,1,0,0],
    [1,0,5,0,0,6,0,3,0],
    [8,0,0,5,0,0,0,0,4],
    [4,0,0,0,2,0,0,0,5],
    [0,0,9,0,0,0,7,0,0],
    [3,0,0,0,8,0,0,0,9],
    [9,0,0,0,0,8,0,0,2],
    [0,3,0,7,0,0,4,0,6],
    [0,0,8,4,0,0,0,0,0]
]

def main():
    m = m_Evil
    viewPuzzle(m, {},[])
    zeroNumber = 81 - len(np.nonzero(m)[0])
    if zeroNumber > 0:
        (m, zeroNumber) = fill(m)
        m = guess(m)
    # updateSolutionSpace(m)
    # viewSolutionSpace()

if __name__ == "__main__":
    main()