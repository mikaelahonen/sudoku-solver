# Sudoku solver

## Example notebook
See the solver example in the [notebook](https://nbviewer.jupyter.org/github/mikaelahonen/sudoku-solver/blob/master/notebook.ipynb).

## Code structure
[config.py](config.py). Set constant variables.

[module.py](module.py). Functions needed for sudoku solving.

[notebook.ipynb](notebook.ipynb). Combine the functions to solve sudokus.

## Approaching the sudoku problem
So far can solve simple sudokus where you can reason the number for each cell with full certainty.

### Sudoku solving algorithms
* Iterative testing
* Different strategies


### Create a 3D boolean sudoku array
* Dimension 0: Row
* Dimension 1: Column
* Dimension 2: Value as boolean array

Value **True** means that it's possible that the answer of this cell is this number.

#### Example 1: Cell has value 1

`[True, False, False, False, False, False, False, False, False]`

#### Example 2: Cell has value 8

`[False, False, False, False, False, False, False, True, False]`

#### Example 3: Cell can have any value
This would be the case if there are no numbers in the same row, column or box.

`[True, True, True, True, True, True, True, True, True]`

#### Example 4: Cell has to be either 2, 8 or 9
This would be the case if there are no numbers in the same row, column or box.

`[False, True, False, False, False, False, False, True, True]`
