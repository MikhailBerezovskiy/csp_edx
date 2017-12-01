import sys
import csv
import math
from collections import deque
from operator import itemgetter
import copy

class sudoku:
    def __init__(self):
        if len(sys.argv) == 2:
            output = self.solve(sys.argv[1])
            f = open('output.txt', 'w')
            f.write(output)
        else:
            self.testing_sequences = self.load_file()[0]
            self.checking_sequences = self.load_file()[1]
            for i in range(len(self.testing_sequences)):
                test = self.solve(self.testing_sequences[i])
                check = self.checking_sequences[i]
                match = test == check
                print (test, match)
                # break
    
    def load_file(self):
        # load examples from start csv
        li_in = []
        li_out = []
        with open('sudokus_start.csv', newline='') as input_file:
            file_reader = csv.reader(input_file)
            for row in file_reader:
                li_in.append(row[0])
        with open('sudokus_finish.csv', newline='') as input_file:
            file_reader = csv.reader(input_file)
            for row in file_reader:
                li_out.append(row[0])
        return (li_in, li_out)


    def convert_str_to_dict(self, string_board):
        # convert string board to dict
        # format: "xyz", x-row, y-col, z-box, first value 000, last 999
        di = {}
        for i in range(len(string_board)):
            x_val = math.trunc(i/9) # col
            y_val = i%9 # row
            sq_val = int(i/27)*3 + int(i%9/3) # box
            di_prop = map(str,[x_val,y_val,sq_val]) # convert to string
            di["".join(di_prop)] = int(string_board[i]) # assign to dictionary
        return di

    def convert_dict_to_str(self, D):
        # input solved matrix of domains D(x)
        # output single string with 81 symbols D(x)
        li = list(range(81)) # create list with 81 lenght
        for x in D:
            # to avoid wrong sequence of dict keys, parse dict key into list item number
            # x = "121", row#1 col#2 box#1
            if type(D[x]) is list:
                val = D[x][0]
            else:
                val = D[x]
            li[9*int(x[0])+int(x[1])] = val 
        return "".join(map(str,li))

    def print_board(sefl, string_board): # in case to check visualy board, not in use
        for i in range(len(string_board)):
            if i%9 == 0:
                print ('\n')
            print (string_board[i], end='\t')
        return print ('\n')  

    #
    # Solver
    #
    def solve(self, string_board):
        # Try AC-3 first, if pass return result
        # Else try bts
        # convert str board to dict before solving
        self.X = self.convert_str_to_dict(string_board)

        test_ac3 = self.ac3(self.X)
        if test_ac3["Pass"]:
            return (self.convert_dict_to_str(test_ac3["Board"]) + " AC3")
        else:
            test_bts = self.bts(self.X) 
            return (self.convert_dict_to_str(test_bts["Board"]) + " BTS")
        
    def ac3(self, X):
        self.D = self.unary_constraints(X) # assign Domain matrix with unary constraints
        q = self.q # assign local queue
        while len(q) != 0:
            arc = q.popleft()
            x,y = arc
            if self.arc_reduce(x,y,self.D[x],self.D[y]):
                if len(self.D[x]) == 0: # D(x) is empty, no solution
                    return {"Pass": False, "Board": self.D} 
                else:
                    N = self.get_neighbors(X,x,y)
                    for n in N:
                        q.append(n)
        # check solution: each domain should have only single value
        for x in self.D:
            if len(self.D[x]) > 1:
                return {"Pass": False, "Board": self.D}
        
        # if not broken yet, finaly return success
        return {"Pass": True, "Board": self.D}

    def unary_constraints(self, X):
        # input all cells
        # output dict with avail cell actions
        self.q = deque([])
        D = {} # init Domains matrix
        for cell in X:
            domain = list(range(1,10)) # available domains
            if X[cell] != 0: D[cell] = [X[cell]] # check given values on board, and assign D(x)
            else:
                D[cell] = []
                for i in X:
                    # check neighboring rows, cols, and box
                    if cell[0] == i[0] or cell[1] == i[1] or cell[2] == i[2]: 
                        try:
                            if cell != i:
                                self.q.append([cell, i]) # update arc consistancy queue
                                domain.remove(X[i]) # filter domain for unary constraint, AllDiff with rows,cols,box
                        except:
                            pass
                D[cell] = domain # assign unary filtered domain to D(x)
        return D # domain matrix

    def arc_reduce(self, x, y, Dx, Dy):
        # input x, y and their available domains
        # constraint check if D(y) is single value domain
        # and vy (D(y)) in D(x) then remove vx
        # output filtered out domain of x D(x) and change
        change = False
        for vx in Dx:
            if vx in Dy and len(Dy) == 1:
                self.D[x].remove(vx)
                change = True
                return change
        return change
    
    def get_neighbors(self, X, x, y):
        # update working list queue (self.q) after arc constancy changed
        Nli = [] # neighbors list
        for xi in X:
            for xj in X:
                if xi == x and xj == y:
                    continue
                if xi[0] == xj[0] or xi[1] == xj[1] or xi[2] == xj[2]:
                    if xi != xj and len(self.D[xj]) == 1:
                        Nli.append([xi, xj])    
        return Nli

    def bts(self, X):
        D = self.unary_constraints(X)
        A = self.fisrt_assignment(X)
        X_mrv = self.mrv(D,A)
        return self.rec_bts(D,A,X_mrv)

    def rec_bts(self, D, A, X_mrv):
        
        if len(A.keys()) == 81:
            return {"Pass": True, "Board": A}
        
        x = X_mrv[0][1]
        for vx in D[x]:
            d1 = copy.deepcopy(D)
            fc = self.forward_checking(x, vx, d1, A)
            if fc != False:
                A[x] = vx
                X_mrv = self.mrv(fc,A)
                result = self.rec_bts(fc,A,X_mrv)
                if result != False:
                    return result
                del A[x]
        return False

    def forward_checking(self, x, vx, D, A):
        for xi in A:
            if xi[0] == x[0] or xi[1] == x[1] or xi[2] == x[2]:
                if vx == A[xi]:
                    return False
        for xj in D:
            if xj == x:
                continue
            if xj[0] == x[0] or xj[1] == x[1] or xj[2] == x[2]:
                if vx in D[xj]:
                    D[xj].remove(vx)
        return D

    def fisrt_assignment(self, X):
        di = {}
        for x in X:
            if X[x] != 0:
                di[x] = X[x]
        return di
    
    def mrv(self, D, A):
        li = []
        for x in D:
            if x not in A:
                li.append([len(D[x]), x])
        li.sort()
        return li

sudoku()


