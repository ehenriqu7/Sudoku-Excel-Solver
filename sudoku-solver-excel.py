"""
Sudoku Solver from Excel file
This scrip reads the Sudoku grid from an Excel file and returns the solution on a new excel file.
algorithm:

"""
from typing import List

import numpy as np
import time
from os import path

sudoku_size = 9
full_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
excel_input_file = "input.csv"
excel_result_file = "output.csv"

sudoku_easy = [[0, 6, 0, 0, 8, 0, 4, 2, 0],
               [0, 1, 5, 0, 6, 0, 3, 7, 8],
               [0, 0, 0, 4, 0, 0, 0, 6, 0],
               [1, 0, 0, 6, 0, 4, 8, 3, 0],
               [3, 0, 6, 0, 1, 0, 7, 0, 5],
               [0, 8, 0, 3, 5, 0, 0, 0, 0],
               [8, 3, 0, 9, 4, 0, 0, 0, 0],
               [0, 7, 2, 1, 3, 0, 9, 0, 0],
               [0, 0, 9, 0, 2, 0, 6, 1, 0]]

sudoku_med = [[0, 0, 1, 4, 0, 0, 9, 0, 0],
              [3, 4, 0, 2, 7, 6, 0, 0, 1],
              [0, 5, 0, 0, 8, 0, 0, 7, 0],
              [7, 0, 0, 0, 5, 0, 0, 1, 0],
              [0, 0, 0, 0, 4, 0, 6, 8, 5],
              [5, 0, 8, 0, 0, 0, 7, 0, 0],
              [0, 2, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 5, 0, 6, 0, 3, 0, 2],
              [6, 0, 0, 0, 2, 0, 0, 0, 0]]

sudoku = [[1, 0, 0, 0, 5, 0, 0, 4, 0],
          [0, 0, 0, 9, 0, 0, 0, 0, 1],
          [0, 0, 0, 0, 0, 3, 8, 0, 0],
          [0, 5, 0, 8, 0, 2, 4, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [4, 0, 0, 0, 0, 0, 7, 5, 3],
          [5, 0, 0, 3, 0, 0, 0, 6, 0],
          [0, 2, 0, 0, 0, 1, 3, 7, 0],
          [0, 6, 0, 4, 0, 9, 0, 0, 0]]

# Expert
sudoku_expert = [[0, 0, 0, 0, 0, 7, 0, 8, 1],
                 [5, 0, 0, 9, 0, 4, 0, 0, 0],
                 [0, 2, 0, 0, 0, 3, 0, 0, 0],
                 [0, 8, 0, 0, 0, 0, 0, 7, 3],
                 [0, 6, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 4, 5, 6, 0, 2, 0, 0],
                 [4, 0, 0, 8, 0, 0, 0, 1, 7],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 9, 0, 0, 2, 0]]

sudoku_insane = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 3, 6, 0, 0, 0, 0, 0],
                 [0, 7, 0, 0, 9, 0, 2, 0, 0],
                 [0, 5, 0, 0, 0, 7, 0, 0, 0],
                 [0, 0, 0, 0, 4, 5, 7, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 3, 0],
                 [0, 0, 1, 0, 0, 0, 0, 6, 8],
                 [0, 0, 8, 5, 0, 0, 0, 1, 0],
                 [0, 9, 0, 0, 0, 0, 4, 0, 0]]


def populate_hints_by_box(test):
    # global test
    hint_by_box = np.full((9, 9), {})
    for row in [0, 3, 6]:  # run through rows
        for col in [0, 3, 6]:
            hint = full_set.difference(set(test[row:row + 3, col:col + 3].flatten()))
            hint_by_box[row:row + 3, col:col + 3] = hint
    return hint_by_box


def get_list_of_hints(su):
    global full_set, sudoku_size, nr_iter
    hint_by_box = populate_hints_by_box(su)
    hints = np.full((9, 9), {})

    for row in range(sudoku_size):  # run through rows
        hint_by_row = full_set.difference(set(su[row, :]))
        for col in range(sudoku_size):
            hint_by_col = full_set.difference(set(su[:, col]))
            if su[row, col] == 0:  # check only empty spaces
                nr_iter += 1
                hint = set(hint_by_row & hint_by_col & hint_by_box[row, col])
                if len(hint) == 0: return []
                hints[row, col] = hint
                if len(hint) == 1: return sorted_list(hints)
    return sorted_list(hints)


def get_len_of_hints(hints):
    global sudoku_size
    len_of_hints = np.full((sudoku_size, sudoku_size), 0)
    for row in range(sudoku_size):
        for col in range(sudoku_size):
            len_of_hints[row, col] = len(hints[row, col])
    return len_of_hints


def sorted_list(hints):
    smallest_list = []
    len_hints = get_len_of_hints(hints)
    for row in range(sudoku_size):
        for col in range(sudoku_size):
            smallest_list.append({"axis": (row, col), "values": hints[row, col], "len": len_hints[row, col]})
    smallest_list.sort(key=lambda x: x['len'])
    smallest_list = [x for x in smallest_list if x['len'] != 0]
    return smallest_list


def print_sudoku(sudoku):
    print(" ")
    for i in range(len(sudoku)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(sudoku[i])):
            if j == 3 or j == 6:
                line += "| "
            line += str(sudoku[i][j]) + " "
        print(line)


def solve(sudoku):
    global nr_loops
    nr_loops += 1
    if 0 not in sudoku:
        print("Found solution")
        return True
    for item in get_list_of_hints(sudoku):
        for val in item['values']:
            sudoku[item['axis']] = val
            if solve(sudoku) == True:
                return True
            else:
                sudoku[item['axis']] = 0
        return False


def read_sudoku_from_file(my_file):
    """
    this function will read a Sudolu matrix from a file
    """
    sudoku_array = np.full((9, 9), 0)
    try:
        with open(my_file, "r") as f:
            for ln, line in enumerate(f):
                line_list = [x for x in line.split(',')]
                sudoku_array[ln] = line_list
    except:
        print("Input file not found")
        return []
    return sudoku_array


def write_result_to_file(sudoku, my_file):
    my_file = '/'.join([path.dirname(__file__), my_file])
    my_file = path.normpath(my_file)
    print(my_file)
    try:
        with open(my_file, "w") as f:
            for line in sudoku:
                l = np.array2string(line, separator=',')
                f.write(l[1:-1] + "\n")
        return True
    except:
        return False


sudoku = read_sudoku_from_file(excel_input_file)

if len(sudoku) != 0:
    nr_iter = 0
    nr_loops = 0

    start_time = time.time()
    solve(sudoku)
    elapsed = time.time() - start_time

    print(f"Process time: {elapsed}")
    print(f"Nr of hints calculations = {nr_iter}")
    print(f"Nr of Solve iterations = {nr_loops}")

    print_sudoku(sudoku)

    write_result_to_file(sudoku, excel_result_file)
