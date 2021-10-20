"""
NetId:             , Vivek Tiwari,  ID: 
NetId: calandradese, Caleb Andrade, ID: 110071013
"""

import time
import random

#*****************************************************************************
# Helper functions to initialize Sudoku's game board.
#*****************************************************************************
def rows(line):
    """
    Reads a *.txt file and returns a single string with the read.
    """
    board = []    
    cha = ''
    row = []
    for c in line:
        if c == ',' or c == ';':
            if cha == '-':
                row.append(0)
            else:
                row.append(int(cha))
            if c == ';':
                board.append(row)
                row = []
            cha = ''
            continue
        cha += c
    return board    

def getBoard(filename):
    """
    Returns N, M, K and a 2D array containing the initial 
    sudoku board from 'filename'.    
    """
    board = []
    f = open(filename, 'r')
    line = f.read().replace('\n', '')
    board = rows(line)
    nmk = board.pop(0)    
    return nmk, board


#*****************************************************************************
# Class board for Sudoku's game board.
#*****************************************************************************
class SudokuBoard(object):
    """
    This is a gameboard class mutable object for Sudoku. Basically the board 
    consists of a two dimensional array, each sub-array represents a row of the 
    gameboard. Empty cells '-' are denoted by 0 in the array and by '.' in the 
    string representation, filled cells by its corresponding number.
    
    Following is a 6x6 empty board with 2x3 sub-grids string representation.
    
    |  .  .  .  |  .  .  .  | 
    |  .  .  .  |  .  .  .  | 
    -------------------------
    |  .  .  .  |  .  .  .  | 
    |  .  .  .  |  .  .  .  | 
    -------------------------
    |  .  .  .  |  .  .  .  | 
    |  .  .  .  |  .  .  .  | 

    
    We keep track of empty cells in a dictionary 'self._empty_cells', where
    keys are the lexicographic order position of the cell (left-to-right, 
    top-to-bottom) in the board.
    
    For each row, we define a set 'self._remain_rvals[row]' that keeps track 
    of those values not yet placed in that particular row. Similarly, for each
    col we define a set 'self._remain_cvals[col]'.
    
    To keep track of the number of constraint checks (row, col and sub-grid
    constraints), we have a variable 'self._num_checks' that is incremented
    by the number of legal available values for a particular cell, calculated 
    by the method 'getLegalValues'.     
    """
    def __init__(self, n, m, k, board = None):
        if n%m != 0 or n%k != 0:
            # sanity check for sub-grid dimensions
            raise ValueError('Invalid sub-grid dimensions!')
        self._n = n
        self._m = m
        self._k = k
        self._num_checks = 0
        self._board = [[0 for col in range(n)] for row in range(n)]
        self._empty_cells = {}
         
        # if SudokuBoard was given an initial game board
        if board != None:
            for row in range(n):
                for col in range(n):
                    self._board[row][col] = board[row][col]
        
        # update empty cells            
        for row in range(n):
            for col in range(n):
                if self._board[row][col] == 0:
                    self._empty_cells[n*row + col] = (row, col)
                
        # initialize sets to store the available values for each row and col
        self._remain_rvals = []
        self._remain_cvals = []      
        vals = set(range(1, n + 1))
        
        # update remaining values for each row and col
        for idx in range(n):
            self._remain_rvals.append(vals.difference(set(self._board[idx])))
            temp_col = set([self._board[row][idx] for row in range(n)])
            self._remain_cvals.append(vals.difference(temp_col))                           
       
    def __str__(self):
        """ 
        As string.
        """
        board = ""
        for row in range(self._n):
            board += "| "
            for col in range(self._n):
                if self._board[row][col] == 0:
                    board += " . "
                else:
                    board += " " + str(self._board[row][col])
                    if len(str(self._board[row][col])) == 1:
                        board += " "
                if (col + 1)%self._k == 0:
                    board += " | "
                if (col + 1) == self._n:
                    board += "\n"
            if (row + 1) % self._m == 0 and row + 1 < self._n:
                board += (4*self._n - 2)*'-'
                board += "\n"
                
        return board
        
    def isGoal(self):
        """
        Checks if all cells are filled, assuming all values are legal.
        """
        return len(self.getEmptyCells()) == 0
            
#    def isGoalSure(self):
#        """
#        Verifies a finished board exhaustively.
#        """
#        for idx in range(self._n):
#            if len(self._remain_rvals[idx]) != 0:
#                return False
#            if len(self._remain_cvals[idx]) != 0:
#                return False
#            if len(self.getSubGridVals(idx, idx)) != self._n:
#                return False
#        return True
        
    def getSize(self):
        """
        Returns size of game board.
        """
        return self._n
        
    def getBoard(self):
        """
        Returns the 2D array representing board.
        """
        return self._board        
        
    def setCellValue(self, row, col, value, mc = False):
        """
        Sets value of cell '(row, col)' to 'value', updates remaining values
        for 'row' and 'col'.
        """
        self._board[row][col] = value
        # update remaining values for row and col
        self._remain_rvals[row].discard(value)
        self._remain_cvals[col].discard(value)
        # update dictionary of empty cells
        if value != 0 and not mc:
            self._empty_cells.pop(self._n*row + col)        
        
    def resetCellValue(self, row, col):
        """
        Resets cell '(row, col)' to 0.
        """
        temp = self.getCellValue(row, col)
        self.setCellValue(row, col, 0)
        # update remaining values for row and col
        self._remain_rvals[row].add(temp)
        self._remain_cvals[col].add(temp)
        # update dictionary of empty cells
        self._empty_cells[self._n*row + col] = (row, col)
                
    def isCellEmpty(self, row, col):
        """
        Checks if '(row, col)' is empty or not.
        """
        return self._board[row][col] == 0
        
    def getEmptyCells(self):
        """
        Returns a list of empty cells. 
        """
        return self._empty_cells.values()
        
    def getNeighbors(self, cell, mc = False):
        """
        Returns a set of those empty cells that are in same row, col and 
        sub-grid as 'cell'.
        """
        # cells in same sub-grid as 'cell'
        subGrid = self.getSubGrid(cell[0], cell[1])
        # cells in same column as 'cell'
        column = set([(row, cell[1]) for row in range(self._n)])
        # cells in same row as 'cell'
        row = set([(cell[0], col) for col in range(self._n)])
        neighbors = subGrid.union(column, row)
        # substract 'cell'
        neighbors.discard(cell)
        # loop in neighbors and remove those non-empty
        non_empty = set([])
        for ncell in neighbors:
            if not mc and self.getCellValue(ncell[0], ncell[1]) != 0:
                non_empty.add(ncell)
        return neighbors.difference(non_empty)
        
    def getMRVCells(self, fwd):
        """
        Returns a list of the empty cells sorted according to MRV heuristic. 
        Also, returns a list of the frequencies of remaining values.
        'fwd' refers to forward checking, either on or off.
        """
        cells = []
        # initialize a dictionary to keep track of remaining values' frequencies
        valFreq = {i:0 for i in range(1, self._n + 1)}
        for cell in self._empty_cells.values():
            # list of remaining values for cell
            rv = self.legalValues(cell[0], cell[1])
            # if forward checking is off, discard cells with mrv = 0
            if not fwd and len(rv) == 0:
                continue
            cells.append((cell, len(rv)))
            # update value frequencies
            for val in rv:
                valFreq[val] += 1
        cells.sort(key = lambda item: item[1])
        
        return cells, valFreq
        
    def getCellValue(self, row, col):
        """
        Returns value of cell '(row, col)'.
        """
        return self._board[row][col]
        
    def getSubGridCor(self, row, col):
        """
        Returns left-top corner of sub-grid containing '(row, col)'.
        """
        corner_row = row / (self._n / self._k)
        corner_col = col / (self._n / self._m)
        return corner_row*self._m, corner_col*self._k
        
    def getSubGrid(self, row, col):
        """
        Returns the set of tuples of the sub-grid that contains '(row, col)'.
        """
        # first, obtain the top-left corner of containing sub-grid
        corner_row, corner_col = self.getSubGridCor(row, col)
        # initialize a list to append sub-grid's elements
        sub_grid = []
        # loop sub-grid's rows
        for sg_row in range(self._m):
            # loop sub-grid's columns
            for sg_col in range(self._k):
                temp_row = corner_row + sg_row
                temp_col = corner_col + sg_col
                sub_grid.append((temp_row, temp_col))
        return set(sub_grid)
        
    def getLegalValues(self, row, col):
        """
        Returns a set of the legal values available for cell '(row, col)' and
        updates num_checks by adding to this counter the length of the output,
        as each legal move accounts for one constraint check.
        """
        # if cell is not empty, then there is no legal move for this cell
        if not self.isCellEmpty(row, col):
            self._num_checks += 1
            return []
        output_set = self.legalValues(row, col)
        self._num_checks += len(output_set)
        return output_set
        
    def legalValues(self, row, col):
        """
        Returns a set of the legal values available for cell '(row, col)'
        """
        # first, intersect available values for row and col
        rcvals = self._remain_rvals[row].intersection(self._remain_cvals[col])
        # substract from the above set those values already in the sub-grid
        output_set = rcvals.difference(self.getSubGridVals(row, col))
        return output_set        
        
    def getSubGridVals(self, row, col):
        """
        Returns the set of values at cells of sub-grid containing '(row, col)'.
        """
        vals = [self.getCellValue(c[0], c[1]) for c in self.getSubGrid(row, col)]
        return set(vals).difference(set([0]))    
    
    
#*****************************************************************************
# Helper functions for heuristics.
#*****************************************************************************
def initialize(filename):
    """
    Initializes and returns Sudoku board object.
    """
    data = getBoard(filename) 
    board = SudokuBoard(data[0][0], data[0][1], data[0][2], data[1])
    return board  
    
def results(board, recursion, heuristic):
    """
    Display results of Sudoku after applying heuristic 'recursion' to 'board'.
    """
    tic = time.clock()
    # apply recursion 
    recursion(board)
    toc = time.clock()
    print "\n\nSOLVED BOARD with heuristic: ", heuristic
    print "Number of Constraint Checks: ", board._num_checks
    print "Running time: ", toc - tic
    print
    print board
  
 
def arcConsistency(board, cell):
    """
    Returns a list of values for cell if arc consistency holds.
    """
    cellVals = board.getLegalValues(cell[0], cell[1])
    discardVal = set([])
    for ncell in board.getNeighbors(cell):
        for xval in cellVals:
            consistency = False
            for yval in board.getLegalValues(ncell[0], ncell[1]):
                if xval != yval:
                    consistency = True
                    break
            if not consistency:
                discardVal.add(xval)
    return list(cellVals.difference(discardVal))
    
def recursiveLoop(board, domain, cell, recursiveBT):
    """
    Loops through cell's domain values. Returns a feasible solution or none.
    """
    for value in domain:
        board.setCellValue(cell[0], cell[1], value)
        result = recursiveBT(board)
        if result != None:
            return result
        board.resetCellValue(cell[0], cell[1])
    return None
    
#def minConHeu(board, cell):
#    """
#    Returns the value of least conflict for cell, with respect to the
#    value that appears less times in all its neighbors.
#    """
#    cell_values = board.legalValues(cell[0], cell[1])
#    board._num_checks += len(cell_values) # update num_checks
#    if len(cell_values) != 0:
#        value = random.choice(list(cell_values))
#    else: 
#        least_freq = []
#        freq = {i:0 for i in range(1, 1 + board._n)}
#        for nc in board.getNeighbors(cell, mc = True):
#            freq[board.getCellValue(nc[0], nc[1])] += 1
#        tuples = freq.items()
#        random.shuffle(tuples)
#        tuples.sort(key = lambda x: x[1])
#        least_freq.append(tuples.pop(0))
#        for x in tuples:
#            if x[1] == least_freq[0][1]:
#                least_freq.append(x)
#            else:
#                break
#        value = random.choice(least_freq)[0]
#    return value
      
#*****************************************************************************
# Implementation of five heuristics to solve Sudoku.
#*****************************************************************************
def backtracking(filename):
    """
    Backtracking basic implemetation for Sudoku.
    """
    def recursiveBT(board):
        """
        Recursive DFS to explore Sudoku's search tree.
        """
        if board.isGoal():
            return board.getBoard()
        # select an available cell: row = cell[0], col = cell[1]
        cell = board.getEmptyCells()[0] 
        # cell's domain of remaining values
        domain = board.getLegalValues(cell[0], cell[1])
        # loop values in domain (legal moves) for cell, apply recursion
        return recursiveLoop(board, domain, cell, recursiveBT)
                
    board = initialize(filename)
    results(board, recursiveBT, 'Backtracking')
    
    return board.getBoard(), board._num_checks

def backtrackingMRV(filename, fwdCheck = False):
    """
    BacktrackingMRV basic implemetation for Sudoku, 'fwdCheck' is a boolean 
    variable, if True then forward checking is active, else is deactivated.
    """
    def recursiveBT(board):
        """
        Recursive DFS to explore Sudoku's search tree.
        """
        if board.isGoal():
            return board.getBoard()
        # obtain list of assignable cells sorted according to mrv 
        mrv = board.getMRVCells(fwdCheck)
        # if list of assignable cells is empty abort search
        if len(mrv[0]) == 0:
            return None
        # forward checking, abort if most const. var. has 0 legal values
        if mrv[0][0][1] == 0:
            return None
        # frequencies of remaining values in the board
        valFreq = mrv[1]
        # select an available cell with least mrv
        cell = mrv[0][0][0]
        # remaining values for cell
        domain = list(board.getLegalValues(cell[0], cell[1]))
        # sort domain by least constraining value
        domain.sort(key = lambda item: valFreq[item]) 
        # loop values in domain (legal moves) for cell, apply recursion
        return recursiveLoop(board, domain, cell, recursiveBT)
    
    board = initialize(filename)
    if fwdCheck:
        variant = 'Backtracking + MRV + fwd'
    else:
        variant = 'Backtracking + MRV'
        
    results(board, recursiveBT, variant)

def backtrackingMRVcp(filename):
    """
    BacktrackingMRV basic implemetation for Sudoku with arc consistency.
    """
    def recursiveBT(board):
        """
        Recursive DFS to explore Sudoku's search tree.
        """
        if board.isGoal():
            return board.getBoard()
        # obtain list of assignable cells sorted according to mrv 
        mrv = board.getMRVCells(False)
        # if list of assignable cells is empty abort search
        if len(mrv[0]) == 0:
            return None
        # frequencies of remaining values in the board
        valFreq = mrv[1]
        # select an available cell with least mrv
        cell = mrv[0][0][0]
        # cell's domain after checking arc consistency
        domain = arcConsistency(board, cell)
        if len(domain) == 0:
            return None
        # sort domain by least constraining value
        domain.sort(key = lambda item: valFreq[item])                
        # loop values in domain (legal moves) for cell, apply recursion
        return recursiveLoop(board, domain, cell, recursiveBT)        
    
    board = initialize(filename)
    results(board, recursiveBT, 'backtrackingMRVcp')
            
    return board.getBoard(), board._num_checks
    
def minConflict(filename):
    return ([], 0)

#def minConflict(filename):
#    """
#    MinConflict basic implemetation for Sudoku.
#    """
#    tic = time.clock()
#    board = initialize(filename)
#    initial_cells = board.getEmptyCells()
#    # assign random values in range (1,n) to empty cells
#    for cell in initial_cells:
#        ran_value = random.randint(1, board._n)
#        board.setCellValue(cell[0], cell[1], ran_value, mc = True)
#    
#    while not board.isGoalSure():
#        # pick a random cell
#        cell = random.choice(initial_cells)
#        # pick a value for this cell according to min-conf-heuristic
#        value = minConHeu(board, cell)           
#        board.setCellValue(cell[0], cell[1], value, mc = True)
#                
#    toc = time.clock()
#    print "\n\nSOLVED BOARD with heuristic: MinConflict"
#    print "Number of Constraint Checks: ", board._num_checks
#    print "Running time: ", toc - tic
#    print
#    print board
#                
#    return board.getBoard(), board._num_checks
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    