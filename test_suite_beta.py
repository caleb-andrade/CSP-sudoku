# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 19:14:25 2015
Caleb Andrade
"""

import csp_beta as csp

def testMethod(answer, expected_answer, test_number):
    """
    Testing method.
    """
    if answer == expected_answer:
        print "test", test_number, " passed!"
    else:
        print "test ", test_number, " failed"

def testMRV(game):
    getMRV = game.getMRVCells(False)
    cells, valFreq = getMRV[0], getMRV[1]
    print "\n\nTesting getMRVCells: \n"
    print cells
    print "\nRemaining values frequencies: \n"
    print valFreq  
    
def testNeighbors(game, cell):
    print "\nTesting getNeighbors for cell: ", cell
    neighbors = list (game.getNeighbors(cell))
    neighbors.sort()
    print neighbors
    
def testBT(filename):
    """
    Tests five heuristics for a given board.
    """
    print '\n*********************', filename, '********************'
    print "\nINITIAL BOARD: \n"
    nmk = csp.getBoard('game.txt')[0]
    board = csp.getBoard(filename)[1]
    game = csp.SudokuBoard(nmk[0], nmk[1], nmk[2], board)
    print game
    csp.backtracking(filename) 
    csp.backtrackingMRV(filename, fwdCheck = False)  
    csp.backtrackingMRV(filename, fwdCheck = True)
    csp.backtrackingMRVcp(filename)
    csp.minConflict(filename)    

# TESTING BACKTRACKING HEURISTICS ON DIFFERENT INPUTS

testBT('game.txt')
testBT('game1.txt')
testBT('game2.txt')
testBT('game3.txt')
# next two boards might be too difficult
#testBT('game4.txt')
#testBT('game5.txt')

"""
# Testing getBoard method
nmk = csp.getBoard('game.txt')[0]
board = csp.getBoard('game.txt')[1]

# TESTING SUDOKU CLASS METHODS
game = csp.SudokuBoard(nmk[0], nmk[1], nmk[2], board)
print "\n\nNumber of constraint checks so far: ", game._num_checks
print "\n\nIs this game board finished? ", game.isGoal()
testMRV(game)

print "\nTesting __str__()\n"
print game

print "\nTesting 'self._remain_rvals'\n"
for i in range(nmk[0]):
    print game._remain_rvals[i]

print "\n\nTesting 'self._remain_cvals'\n"
for i in range(nmk[0]):
    print game._remain_cvals[i]
    
print "\n\nTesting getEmptyCells"
print len(game.getEmptyCells())

print "\n\nTesting getSubGridCor(row, col)\n"
testMethod(game.getSubGridCor(0, 0), (0, 0), '1')
testMethod(game.getSubGridCor(2, 3), (0, 0), '2')
testMethod(game.getSubGridCor(0, 11), (0, 8), '3')
testMethod(game.getSubGridCor(2, 9), (0, 8), '4')
testMethod(game.getSubGridCor(4, 5), (3, 4), '5')
testMethod(game.getSubGridCor(4, 7), (3, 4), '6')
testMethod(game.getSubGridCor(5, 10), (3, 8), '7')
testMethod(game.getSubGridCor(3, 9), (3, 8), '8')
testMethod(game.getSubGridCor(6, 0), (6, 0), '9')
testMethod(game.getSubGridCor(8, 2), (6, 0), '10')
testMethod(game.getSubGridCor(7, 4), (6, 4), '11')
testMethod(game.getSubGridCor(8, 7), (6, 4), '12')
testMethod(game.getSubGridCor(9, 11), (9, 8), '13')

print "\n\nTesting getSubGrid\n"
sub_grid0 = set([(0, 0), (0, 1), (0, 2), (0, 3), 
                 (1, 0), (1, 1), (1, 2), (1, 3),
                 (2, 0), (2, 1), (2, 2), (2, 3)])
sub_grid1 = set([(0, 4), (0, 5), (0, 6), (0, 7), 
                 (1, 4), (1, 5), (1, 6), (1, 7),
                 (2, 4), (2, 5), (2, 6), (2, 7)])
sub_grid2 = set([(0, 8), (0, 9), (0, 10), (0, 11), 
                 (1, 8), (1, 9), (1, 10), (1, 11),
                 (2, 8), (2, 9), (2, 10), (2, 11)])
sub_grid3 = set([(3, 0), (3, 1), (3, 2), (3, 3), 
                 (4, 0), (4, 1), (4, 2), (4, 3),
                 (5, 0), (5, 1), (5, 2), (5, 3)])
sub_grid4 = set([(3, 4), (3, 5), (3, 6), (3, 7), 
                 (4, 4), (4, 5), (4, 6), (4, 7),
                 (5, 4), (5, 5), (5, 6), (5, 7)])
sub_grid5 = set([(3, 8), (3, 9), (3, 10), (3, 11), 
                 (4, 8), (4, 9), (4, 10), (4, 11),
                 (5, 8), (5, 9), (5, 10), (5, 11)])
sub_grid6 = set([(6, 0), (6, 1), (6, 2), (6, 3), 
                 (7, 0), (7, 1), (7, 2), (7, 3),
                 (8, 0), (8, 1), (8, 2), (8, 3)])
sub_grid7 = set([(6, 4), (6, 5), (6, 6), (6, 7), 
                 (7, 4), (7, 5), (7, 6), (7, 7),
                 (8, 4), (8, 5), (8, 6), (8, 7)])
sub_grid8 = set([(6, 8), (6, 9), (6, 10), (6, 11), 
                 (7, 8), (7, 9), (7, 10), (7, 11),
                 (8, 8), (8, 9), (8, 10), (8, 11)])
sub_grid9 = set([(9, 0), (9, 1), (9, 2), (9, 3), 
                 (10, 0), (10, 1), (10, 2), (10, 3),
                 (11, 0), (11, 1), (11, 2), (11, 3)])
sub_grid10 = set([(9, 4), (9, 5), (9, 6), (9, 7), 
                  (10, 4), (10, 5), (10, 6), (10, 7),
                  (11, 4), (11, 5), (11, 6), (11, 7)])
sub_grid11 = set([(9, 8), (9, 9), (9, 10), (9, 11), 
                  (10, 8), (10, 9), (10, 10), (10, 11),
                  (11, 8), (11, 9), (11, 10), (11, 11)])

testMethod(game.getSubGrid(2, 2), sub_grid0, '1')
testMethod(game.getSubGrid(2, 6), sub_grid1, '2')
testMethod(game.getSubGrid(1, 9), sub_grid2, '3')
testMethod(game.getSubGrid(4, 2), sub_grid3, '4')
testMethod(game.getSubGrid(3, 5), sub_grid4, '5')
testMethod(game.getSubGrid(5, 8), sub_grid5, '6')
testMethod(game.getSubGrid(6, 2), sub_grid6, '7')
testMethod(game.getSubGrid(8, 5), sub_grid7, '8')
testMethod(game.getSubGrid(6, 11), sub_grid8, '9')
testMethod(game.getSubGrid(10, 1), sub_grid9, '10')
testMethod(game.getSubGrid(11, 5), sub_grid10, '11')
testMethod(game.getSubGrid(10, 8), sub_grid11, '12')

# test getNeighbors
for i in range(nmk[0]/3):
    testNeighbors(game, (3*i, 3*i))

print "\nTesting setCellValue(value, row, col)\n"
for i in range(nmk[0]):
    game.setCellValue(i, i, i + 1)
print game

# test getNeighbors
for i in range(nmk[0]/3):
    testNeighbors(game, (3*i, 3*i))

print "\n\nTesting getSubGridVals for each sub-grid of current board\n"
print game.getSubGridVals(2, 0)
print game.getSubGridVals(1, 6)
print game.getSubGridVals(0, 10)
print game.getSubGridVals(5, 3)
print game.getSubGridVals(4, 6)
print game.getSubGridVals(3, 9)
print game.getSubGridVals(8, 0)
print game.getSubGridVals(8, 6)
print game.getSubGridVals(7, 10)
print game.getSubGridVals(9, 2)
print game.getSubGridVals(10, 5)
print game.getSubGridVals(11, 11)

print "\n\nTesting getLegalMoves for col 0\n"
for row in range(game.getSize()):
    print game.getLegalValues(row, 0)
    print "Number of constraint checks so far: ", game._num_checks
    print
    
testMRV(game)

vals = set([i for i in range(1, nmk[0] + 1)])
print "\nTesting 'self._remain_rvals'\n"
for i in range(nmk[0]):
    testMethod(game._remain_rvals[i], vals.difference(set([i+1])), i + 1)

print "\n\nTesting 'self._remain_cvals'\n"
for i in range(nmk[0]):
    testMethod(game._remain_cvals[i], vals.difference(set([i+1])), i + 1)
    
print "\n\nTesting getEmptyCells\n\n", game.getEmptyCells()
    
print "\n\nTesting resetCellValue(row, col)\n"
for i in range(nmk[0]):
    game.resetCellValue(i, i)
print game

print "\n\nTesting getEmptyCells"
print len(game.getEmptyCells())

print "\nTesting setCellValue & remaining value\n"
game.setCellValue(6, 4, 1)
game.setCellValue(6, 5, 2)
game.setCellValue(6, 6, 3)
game.setCellValue(6, 7, 4)
game.setCellValue(7, 4, 5)
game.setCellValue(7, 5, 6)
game.setCellValue(7, 6, 7)
game.setCellValue(7, 7, 8)
game.setCellValue(8, 4, 9)
game.setCellValue(8, 5, 10)
game.setCellValue(8, 6, 11)
game.setCellValue(8, 7, 12)
print game
print "\nTesting getEmptyCells"
print game.getEmptyCells()
print
testMethod(game._remain_rvals[6], vals.difference(set([1, 2, 3, 4])), 'row 6')
testMethod(game._remain_rvals[7], vals.difference(set([5, 6, 7, 8])), 'row 7')
testMethod(game._remain_rvals[8], vals.difference(set([9, 10, 11, 12])), 'row 8')
print
testMethod(game._remain_cvals[4], vals.difference(set([1, 5, 9])), 'col 4')
testMethod(game._remain_cvals[5], vals.difference(set([2, 6, 10])), 'col 5')
testMethod(game._remain_cvals[6], vals.difference(set([3, 7, 11])), 'col 6')
testMethod(game._remain_cvals[7], vals.difference(set([4, 8, 12])), 'col 7')

print "\n\nTesting getSubGridVals for each sub-grid of current board\n"
print game.getSubGridVals(2, 0)
print game.getSubGridVals(1, 6)
print game.getSubGridVals(0, 10)
print game.getSubGridVals(5, 3)
print game.getSubGridVals(4, 6)
print game.getSubGridVals(3, 9)
print game.getSubGridVals(8, 0)
print game.getSubGridVals(6, 4)
print game.getSubGridVals(7, 10)
print game.getSubGridVals(9, 2)
print game.getSubGridVals(10, 5)
print game.getSubGridVals(11, 11)
print
print game
print "\nTesting getLegalValues for principal diagonal\n"
for idx in range(game.getSize()):
    print game.getLegalValues(idx, idx)
    print "Number of constraint checks so far: ", game._num_checks
    print

testMRV(game)

print "\nTesting 'self._remain_rvals'\n"
for i in range(nmk[0]):
    print game._remain_rvals[i]

print "\n\nTesting 'self._remain_cvals'\n"
for i in range(nmk[0]):
    print game._remain_cvals[i]

"""




