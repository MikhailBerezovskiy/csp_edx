import sys
import csv
import math
from copy import deepcopy


class init:
    def __init__(self):
        self.testing_sequences = self.load_file()
        self.testing_board_str = self.testing_sequences[1]
        self.testing_board_di = self.convert_str_to_dict(self.testing_board_str)


    def load_file(self):
        # load examples from start csv
        li = []
        with open('sudokus_start.csv', newline='') as input_file:
            file_reader = csv.reader(input_file)
            for row in file_reader:
                li.append(row[0])
        return li


    def convert_str_to_dict(self, string_board):
        # convert string board to dict
        # format: square 9x9 cells with "A-I" for x and "1-9" for Y
        print (string_board)
        di = {}
        for i in range(len(string_board)):
            # x_val = chr(65 + math.trunc(i/9))
            x_val = math.trunc(i/9)
            y_val = i%9
            sq_val = int(i/27)*3 + int(i%9/3) 
            di_prop = map(str,[x_val,y_val,sq_val])
            di["".join(di_prop)] = int(string_board[i])
        print (di)
        return di

    def print_board(sefl, string_board):
        for i in range(len(string_board)):
            if i%9 == 0:
                print ('\n')
            print (string_board[i], end='\t')
        return print ('\n')  

    def solve(self, string_board):
        # Try AC-3 first, if pass return result
        # Else try bts
        # convert str board to dict before solving
        X = self.board_str_to_dict(string_board)
        D = list(range(1,10))
        # try AC-3
        test_ac3 = self.ac3(X, D)
        if test_ac3["Pass"]:
            return (test_ac3["Board"], "AC3")
        # try bts
        else:
            test_bts = self.bts(X)
            return (test_bts["board"], "BTS")



    def get_actions(self, X):
        # input all cells
        # output dict with avail cell actions
        D = {}
        for cell in X:
            avail_nums = list(range(1,10))
            D[cell] = []
            for i in X:
                if cell[0] == i[0] or cell[1] == i[1] or cell[2] == i[2]:
                    try:
                        avail_nums.remove(X[i])
                    except:
                        pass        
            print (cell, X[cell], avail_nums)
            D[cell] = avail_nums
        print (D)

    def test_constraints(self, X, cell):
        for i in X:
            if cell[0] == i[0] or cell[1] == i[1] or cell[2] == i[2]:
                    

    def test_ac3(self, X, D, R1, R2):
        return True
    # init ac-3

    #  Input:
    #    A set of variables X
    #    A set of domains D(x) for each variable x in X. D(x) contains vx0, vx1... vxn, the possible values of x
    #    A set of unary constraints R1(x) on variable x that must be satisfied
    #    A set of binary constraints R2(x, y) on variables x and y that must be satisfied

    #  Output:
    #    Arc consistent domains for each variable.
    
    #  function ac3 (X, D, R1, R2)
    #  // Initial domains are made consistent with unary constraints.
    #      for each x in X
    #          D(x) := { vx in D(x) | R1(x) }   
    #      // 'worklist' contains all arcs we wish to prove consistent or not.
    #      worklist := { (x, y) | there exists a relation R2(x, y) or a relation R2(y, x) }
    
    #      do
    #          select any arc (x, y) from worklist
    #          worklist := worklist - (x, y)
    #          if arc-reduce (x, y) 
    #              if D(x) is empty
    #                  return failure
    #              else
    #                  worklist := worklist + { (z, x) | z != y and there exists a relation R2(x, z) or a relation R2(z, x) }
    #      while worklist not empty
    
    #  function arc-reduce (x, y)
    #      bool change = false
    #      for each vx in D(x)
    #          find a value vy in D(y) such that vx and vy satisfy the constraint R2(x, y)
    #          if there is no such vy {
    #              D(x) := D(x) - vx
    #              change := true
    #          }
    #      return change


init = init()
st = init.testing_sequences[1]
init.print_board(st)
D = init.get_actions(init.testing_board_di)
