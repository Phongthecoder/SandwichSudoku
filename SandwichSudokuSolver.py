import gurobipy as gp
from gurobipy import GRB
import numpy as np
import json

#get information of the board from json file
def get_board(path):
    f = open(path)
    data = json.load(f)
    size = data["size"]
    numbers_on_board = data["existence_numbers_on_board"]
    numbers_on_rows = data["numbers_on_rows"]
    numbers_on_columns = data["numbers_on_columns"]
    return size, numbers_on_board, numbers_on_rows, numbers_on_columns

#The condition that every cell is filled with a number from 1 to 9
def all_cell_filled_condition(T, size):
    for i in range(size):
        for j in range(size):
            sum = 0
            for k in range(size):
                sum += T[i][j][k]
            model.addConstr(sum == 1)

# The condition that numbers on the same row must be different
def different_condition_rows(T,size):
    for k in range(size):
        for i in range(size):
            sum = 0
            for j in range(size):
                sum += T[i][j][k]
            model.addConstr(sum == 1)
            
# The condition that numbers on the same column must be different
def different_condition_columns(T,size):
    for k in range(size):
        for i in range(size):
            sum = 0
            for j in range(size):
                sum += T[j][i][k]
            model.addConstr(sum == 1)
            
#The condition that numbers in a 3x3 fixed region must 
def different_condition_regions(T,size):
    for k in range(size):
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                sum = 0
                for x in range(0,3):
                    for y in range(0,3):
                        sum += T[i+x][j+y][k]
                model.addConstr(sum == 1)
                
#The condition for numbers that are already filled in the board
def fill_numbers(T, size, numbers_on_board):
    for i in range(size):
        for j in range(size):
            k = numbers_on_board[i][j]
            if k != 0:
                model.addConstr(T[i][j][k-1] == 1)

#The sandwich condition on rows
def sandwich_rows_condition(T, size, numbers_on_rows):
    for i in range(size):
        s = numbers_on_rows[i]
        for m in range(size):
            for n in range(m, size):
                sum = 0
                for x in range(m, n+1):
                    for k in range(1, size+1):
                        sum += T[i][x][k-1]*k
                sum += (10**3) * (T[i][m][0]+T[i][n][size-1])
                model.addConstr(sum - s - 10 <= 2* (10**3))
                sum -= 2*(10**3) * (T[i][m][0]+T[i][n][size-1])
                model.addConstr(sum - s - 10 >= -2*(10**3))
    
    
    for i in range(size):
        s = numbers_on_rows[i]
        for m in range(size):
            for n in range(m, size):
                sum = 0
                for x in range(m, n+1):
                    for k in range(1, size+1):
                        sum += T[i][x][k-1]*k
                sum += (10**3) * (T[i][n][0]+T[i][m][size-1])
                model.addConstr(sum - s - 10 <= 2* (10**3))
                sum -= 2*(10**3) * (T[i][n][0]+T[i][m][size-1])
                model.addConstr(sum - s - 10 >= -2*(10**3))
                
#The sandwich condition on columns:
def sandwich_columns_condition(T,size, numbers_on_columns):
    for i in range(size):
        s = numbers_on_columns[i]
        for m in range(size):
            for n in range(m, size):
                sum = 0
                for x in range(m, n+1):
                    for k in range(1, size+1):
                        sum += T[x][i][k-1]*k
                sum += (10**3) * (T[m][i][0]+T[n][i][size-1])
                model.addConstr(sum - s - 10 <= 2* (10**3))
                sum -= 2*(10**3) * (T[m][i][0]+T[n][i][size-1])
                model.addConstr(sum - s - 10 >= -2*(10**3))
    
    
    for i in range(size):
        s = numbers_on_columns[i]
        for m in range(size):
            for n in range(m, size):
                sum = 0
                for x in range(m, n+1):
                    for k in range(1, size+1):
                        sum += T[x][i][k-1]*k
                sum += (10**3) * (T[n][i][0]+T[m][i][size-1])
                model.addConstr(sum - s - 10 <= 2* (10**3))
                sum -= 2*(10**3) * (T[n][i][0]+T[m][i][size-1])
                model.addConstr(sum - s - 10 >= -2*(10**3))

#print the result
def print_board(size, values):
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
                if values[81*i + 9*j + k] == 1:
                    X[i][j] = k+1
    
    for i in range(len(X)):
        print(X[i])
    

                
if __name__ == "__main__":
    model = gp.Model('SandwichSudokuSolver')
    size, numbers_on_board, numbers_on_rows, numbers_on_columns = get_board('board_data1.json')
    T = model.addMVar(shape = (size, size, size), lb = 0, ub = 1, vtype = GRB.INTEGER, name = "x") #shape of T: (row, column, variables in each cell)
    
    all_cell_filled_condition(T, size)
    different_condition_rows(T,size)
    different_condition_columns(T,size)
    different_condition_regions(T,size)
    fill_numbers(T, size, numbers_on_board)
    sandwich_rows_condition(T, size, numbers_on_rows)
    sandwich_columns_condition(T,size, numbers_on_columns)
    
    model.setObjective(1, sense = GRB.MAXIMIZE)

    model.optimize()
    print('-' * 50)
    if model.status == GRB.OPTIMAL:
        print('The status meaning is OPTIMAL')
        
        
    values = model.getAttr("X", model.getVars()) #get the result 
    print_board(size, values)
    
    
    
    

        
    
                     
            
    


