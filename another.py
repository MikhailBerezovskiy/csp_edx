import sys
import csv
import math

class sudoku:
    def __init__(self):
        self.testing_sequences = self.load_file()

        for each in self.testing_sequences:
            print (each)

    def load_file(self):
        # load examples from start csv
        li = []
        with open('sudokus_start.csv', newline='') as input_file:
            file_reader = csv.reader(input_file)
            for row in file_reader:
                li.append(row[0])
        return li


    def csp(self, string_board):
        # X = matrix of variables
        # C = constraints test
        # D = domain
        D = list(range(1,10))
        

    # CSP
    # X

    # Domain
    # Constraints
    # AllDiff for all vx and vy



init = sudoku()