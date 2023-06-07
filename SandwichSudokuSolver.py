import gurobipy as gp
from gurobipy import GRB
import numpy as np
import json
import math





def get_board( path):
        f = open(path)
        data = json.load(f)
        size = data["size"]
        numbers_on_board = data["existence_numbers_on_board"]
        numbers_on_rows = data["numbers_on_rows"]
        numbers_on_columns = data["numbers_on_columns"]
        return size, numbers_on_board, numbers_on_rows, numbers_on_columns
class SandwichSudoku:  
     
    def __init__(self, size, numbers_on_board, numbers_on_rows, numbers_on_columns, T, bigM):
        self.size = size
        self.numbers_on_board = numbers_on_board
        self.numbers_on_rows = numbers_on_rows
        self.numbers_on_columns = numbers_on_columns
        self.T = T
        self.bigM = bigM
        self.sqrt = int(math.sqrt(self.size))
        
        
    
    #The condition that every cell is filled with a number from 1 to 9
    
    def all_cell_filled_condition(self):
        for i in range(self.size):
            for j in range(self.size):
                sum = 0
                for k in range(self.size):
                    sum += self.T[i][j][k]
                model.addConstr(sum == 1)


    # The condition that numbers on the same row must be different
    def different_condition_rows(self):
        for k in range(self.size):
            for i in range(self.size):
                sum = 0
                for j in range(self.size):
                    sum += self.T[i][j][k]
                model.addConstr(sum == 1)
        
                
    # The condition that numbers on the same column must be different
    def different_condition_columns(self):
        for k in range(self.size):
            for i in range(self.size):
                sum = 0
                for j in range(self.size):
                    sum += self.T[j][i][k]
                model.addConstr(sum == 1)
                
    #The condition that numbers in a 3x3 fixed region must 
    def different_condition_regions(self):
        for k in range(self.size):
            for i in range(0, self.size, self.sqrt):
                for j in range(0, self.size, self.sqrt):
                    sum = 0
                    for x in range(0,self.sqrt):
                        for y in range(0,self.sqrt):
                            sum += self.T[i+x][j+y][k]
                    model.addConstr(sum == 1)
                    
    #The condition for numbers that are already filled in the board
    def fill_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                k = self.numbers_on_board[i][j]
                if k != 0:
                    model.addConstr(self.T[i][j][k-1] == 1)

    #The sandwich condition on rows
    def sandwich_rows_condition(self):
        for i in range(self.size):
            s = self.numbers_on_rows[i]
            for m in range(self.size):
                for n in range(m, self.size):
                    sum = 0
                    for x in range(m, n+1):
                        for k in range(1, self.size+1):
                            sum += self.T[i][x][k-1]*k
                    sum += (10**3) * (self.T[i][m][0]+self.T[i][n][size-1])
                    model.addConstr(sum - s - 10 <= 2* (self.bigM))
                    sum -= 2*(10**3) * (self.T[i][m][0]+self.T[i][n][size-1])
                    model.addConstr(sum - s - 10 >= -2*(self.bigM))
        
        
        for i in range(size):
            s = self.numbers_on_rows[i]
            for m in range(self.size):
                for n in range(m, self.size):
                    sum = 0
                    for x in range(m, n+1):
                        for k in range(1, self.size+1):
                            sum += self.T[i][x][k-1]*k
                    sum += (10**3) * (self.T[i][n][0]+self.T[i][m][size-1])
                    model.addConstr(sum - s - 10 <= 2* (self.bigM))
                    sum -= 2*(10**3) * (self.T[i][n][0]+self.T[i][m][size-1])
                    model.addConstr(sum - s - 10 >= -2*(self.bigM))
                    
    #The sandwich condition on columns:
    def sandwich_columns_condition(self):
        for i in range(self.size):
            s = self.numbers_on_columns[i]
            for m in range(self.size):
                for n in range(m, self.size):
                    sum = 0
                    for x in range(m, n+1):
                        for k in range(1, self.size+1):
                            sum += self.T[x][i][k-1]*k
                    sum += (10**3) * (self.T[m][i][0]+self.T[n][i][size-1])
                    model.addConstr(sum - s - 10 <= 2* (self.bigM))
                    sum -= 2*(10**3) * (self.T[m][i][0]+self.T[n][i][size-1])
                    model.addConstr(sum - s - 10 >= -2*(self.bigM))
        
        
        for i in range(size):
            s = self.numbers_on_columns[i]
            for m in range(self.size):
                for n in range(m, self.size):
                    sum = 0
                    for x in range(m, n+1):
                        for k in range(1, self.size+1):
                            sum += self.T[x][i][k-1]*k
                    sum += (10**3) * (self.T[n][i][0]+self.T[m][i][size-1])
                    model.addConstr(sum - s - 10 <= 2* (self.bigM))
                    sum -= 2*(10**3) * (self.T[n][i][0]+self.T[m][i][size-1])
                    model.addConstr(sum - s - 10 >= -2*(self.bigM))

    #print the result
def print_board( size, values):
    X = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(0, size):
        for j in range(0, size):
            for k in range(0, size):
                if values[size*size*i + size*j + k] == 1:
                    X[i][j] = k+1
        
    for i in range(len(X)):
        print(X[i])
        

                
if __name__ == "__main__":
    model = gp.Model('SandwichSudokuSolver')
    size, numbers_on_board, numbers_on_rows, numbers_on_columns = get_board('board_data1.json')
    T = model.addMVar(shape = (size, size, size), lb = 0, ub = 1, vtype = GRB.INTEGER, name = "x") #shape of T: (row, column, variables in each cell)
    
    sandwich = SandwichSudoku(size, numbers_on_board, numbers_on_rows, numbers_on_columns, T, 10**3)
    
    sandwich.all_cell_filled_condition()
    sandwich.different_condition_rows()
    sandwich.different_condition_columns()
    sandwich.different_condition_regions()
    sandwich.fill_numbers()
    sandwich.sandwich_rows_condition()
    sandwich.sandwich_columns_condition()
    
    model.setObjective(1, sense = GRB.MAXIMIZE)

    model.optimize()
    print('-' * 50)
    if model.status == GRB.OPTIMAL:
        print('The status meaning is OPTIMAL')
        
        
    values = model.getAttr("X", model.getVars()) #get the result 
    print_board(size, values)
    
    
    
    

        
    
                     
            
    


