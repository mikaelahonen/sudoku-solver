import sys
import importlib

importlib.reload(sys.modules['config'])
from config import *

import numpy as np




###############################
### Array conversion
###############################

#Convert human readable array to better format for python
def convert_input_2d(arr):
  
    #Reshape to 9x9
    arr = np.reshape(arr, (rows, cols))

    #Convert zeros to nan
    arr = np.where(arr==0, 0, arr)

    #Reduce one to make 
    arr = arr - 1

    return arr


#Convert 2d array to boolean 3d array
def convert_2d_3d(arr_2d):
    
    #Initialize 9x9x9 array rows x cols x boolean
    #Mark initially all to False
    arr_3d = np.zeros((rows, cols, vals), dtype=bool)

    #The cells having a known number, mark only the known item True
    r_knwon, c_known, v_known = get_known_2d(arr_2d)
    arr_3d[r_knwon, c_known, v_known] = True

    #The cells not having a known number, mark the whole array True
    r_unknown, c_unknown, v_unknown = get_known_2d(arr_2d, unknown=True)
    arr_3d[r_unknown, c_unknown] = np.repeat(True, vals)
    
    return arr_3d

def convert_3d_2d(arr_3d):
    
    #Initialize 9x9 array rows x cols
    #Mark initially all to -1 which marks "not known"
    arr_2d = np.zeros((rows, cols))-1
    
    #Get known row and column indexes
    r_known, c_known, v_known = get_known_3d(arr_3d)
    
    #Mark known values
    arr_2d[r_known, c_known] = v_known
    
    return arr_2d


###############################
### Matrix helper functions
###############################

#Get known values from 2d matrix
def get_known_2d(arr_2d, unknown=False):
     
    #Get index numbers of rows and columns having a (un)known value 
    r_i, c_i  = np.where((arr_2d == no_val) == unknown)

    #Get (un)known values
    v_i = arr_2d[r_i, c_i]

    #r_i: row index
    #c_i: column index
    #v_i: the known sudoku number that will be marked as true in the boolean array
    return r_i, c_i, v_i


def get_known_3d(arr_3d_arg):
    
    arr_3d = arr_3d_arg.copy()
    
    #Get row and cell coordinates for cells that are NOT known for sure (have more than 1 possible values)
    r_i_unknown, c_i_unknown  = np.where(arr_3d.sum(axis=2) > 1)
       
    #Mark unknown cells to false
    arr_3d[r_i_unknown, c_i_unknown] = np.repeat(False, vals)

    #Get indexes of all cells having the valueTrue
    r_i, c_i, v_i = np.where(arr_3d)
    
    return r_i, c_i, v_i


###############################
### Retrieve information
###############################

def count_knowns_2d(arr_2d):
    
    known_count = (arr_2d!=-1).sum()

    return known_count

def print_grid(arr):
    
    arr = arr+1
    
    h = "-"
    v = "|"
    corner = "+"    
    border_line = "\n" + corner + ((h*3*cols_box)+corner)*int(cols/cols_box)
    grid = border_line
    
    #Loop each cell
    for r in range(rows):
        grid += "\n" + v
        for c in range(cols):
            num = str(int(arr[r,c]))
            
            #Empty for zeros
            if num == "0":
                num = " "
            
            #Sudoku numeber
            grid += " " + num + " "
        
            #Box border for columns
            if c%cols_box == 2:
                grid += v
        
        #Box border for rows
        if r%rows_box == 2:
            grid += border_line
    
    print(grid)

###############################
### Range functions
###############################

#Get box range accoring to the cell coordinates
def get_box_rng(r, c):
  
    #Example: 7 > [6,6,6,7,7,7,8,8,8]
    rng_row = np.arange(rows_box).repeat(rows_box) + r//rows_box*rows_box

    #Example: 7 > [6,7,8,6,7,8,6,7,8]
    rng_col = np.tile(np.arange(cols_box), (cols_box)) + c//cols_box*cols_box

    return rng_row, rng_col

def get_ranges(arr, r, c):

    #Get value by row
    rng_row = arr[np.repeat(r, rows), np.arange(cols), :]

    #Get values by column 
    rng_col = arr[np.arange(rows), np.repeat(c, cols), :]

    #Get values by box
    rng_row_box, rng_col_box = get_box_rng(r, c)
    rng_box = arr[rng_row_box, rng_col_box, :]

    #Concatenate all values
    rng_all = np.concatenate((rng_row, rng_col, rng_box))        

    return rng_all, rng_row, rng_col, rng_box

def get_elimination_array(arr, rng):
  
    cells_with_known = rng[rng.sum(axis=1)==1, :]

    elim = cells_with_known.sum(axis=0)

    #print(elim)
    elim2 = elim==0

    return elim2
    
    
###############################
### Apply the strategies for each cell
###############################

#Go through each cell
def loop_cells(arr, r_loop=range(rows), c_loop=range(cols)):

    #print(arr)
    
    #Loop each cell
    for r in r_loop:
        for c in c_loop:

            #print("\nCell({}, {})".format(r, c))

            #Get the slice of this cell
            cell = arr[r, c, :]

            #Count of possible values in this cell
            cell_psbl_n = cell.sum()

            #Skip if the cell is already known
            if cell_psbl_n == 1:
                #print("1 possible value")
                pass
        
            #There's an error if no possible value
            elif cell_psbl_n == 0:
                #print("0 possible values")
                pass

            else:

                #print("{} possible values".format(cell_psbl_n))

                rng_all, rng_row, rng_col, rng_box = get_ranges(arr, r, c)

                #Strategy 1: Eliminate all knowns

                elim_arr = get_elimination_array(arr, rng_all)

                either_false = cell & elim_arr

                new_psbl_n = either_false.sum()

                #print(cell)
                #print("{} possible after elimination".format(new_psbl_n))
                #print(either_false)

                arr[r ,c] = either_false

                #Strategy 2: Set value, if 

                #By row - Strategy 2

                #By col - Strategy 2

                #By box - Strategy 2

                #print(arr)
        
    return arr