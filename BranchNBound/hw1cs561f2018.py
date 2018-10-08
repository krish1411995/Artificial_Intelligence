#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:48:18 2018

@author: krishmehta
"""

import numpy as np
import time
import sys

length_of_matrix = -1
no_of_officers = -1
no_of_vehicles = -1
dict_freq_count = {}
frequency_sorted = []
frequency_scooter = []
row_look_up = []
column_look_up = []
slash_look_up = []
back_slash_look_up = []
max_value = 0
current_value = 0
length_of_list = -1
number_iterate = 0


# this function checks whether the queen can be placed or not and also check whether the sum of the remaining queen is less than or equal to max
def check_if_safe(row, column, index):
    if max_value >= current_value + no_of_officers * frequency_sorted[index][2]:
        return bool(0)
    if back_slash_look_up[int(back_slash[row][column])] or slash_look_up[int(slash[row][column])] or row_look_up[row] or \
            column_look_up[column]:
        return bool(0)
    return bool(1)


# this is the recursive function which checks the max values and continously updates the output file with the max value.
# This function also updates all the arrays where the queens are placed
def solve_officer_util(index):
    global no_of_officers, current_value, max_value
    global number_iterate
    if no_of_officers == 0:
        number_iterate = 1
        if max_value < current_value:
            max_value = current_value
            with open("output.txt", "w") as file:
                file.write(str(max_value) + "\n")
            file.close()
        return
    for i in range(index, length_of_list):
        row = frequency_sorted[i][1]
        column = frequency_sorted[i][0]
        value_column = frequency_sorted[i][2]
        if no_of_officers == 2:
            number_iterate = 0

        if number_iterate == 1:
            return
        global b
        b = time.time()
        if b - a > 180:
            sys.exit()
        if check_if_safe(row, column, i):

            row_look_up[row] = bool(1)
            column_look_up[column] = bool(1)
            current_value = current_value + value_column
            no_of_officers = no_of_officers - 1
            slash_look_up[int(slash[row][column])] = bool(1)
            back_slash_look_up[int(back_slash[row][column])] = bool(1)

            if solve_officer_util(i + 1):
                return bool(1)
            row_look_up[row] = bool(0)
            column_look_up[column] = bool(0)
            slash_look_up[int(slash[row][column])] = bool(0)
            back_slash_look_up[int(back_slash[row][column])] = bool(0)
            current_value = current_value - value_column
            no_of_officers = no_of_officers + 1


def place_officers():
    index = 0
    global length_of_list
    length_of_list = len(frequency_sorted)
    while index < length_of_list:
        solve_officer_util(index)
        index = index + 1
        if max_value >= frequency_sorted[index][2] * no_of_officers:
            break
        initalize_matrix()
    return bool(1)


# intitialize all the arrays
def initalize_matrix():
    global back_slash, slash, back_slash_look_up, slash_look_up, row_look_up, column_look_up
    row_look_up = [False] * length_of_matrix
    column_look_up = [False] * length_of_matrix
    slash_look_up = [False] * length_of_matrix * 2
    back_slash_look_up = [False] * length_of_matrix * 2
    back_slash = np.ones((length_of_matrix, length_of_matrix))
    slash = np.ones((length_of_matrix, length_of_matrix))
    for i in range(0, length_of_matrix):
        for j in range(0, length_of_matrix):
            back_slash[j][i] = j - i + (length_of_matrix - 1)
            slash[j][i] = j + i

# fetches the value from the file
def fetch_values():
    global length_of_matrix
    global no_of_officers
    global no_of_vehicles
    global frequency_sorted
    with open('input.txt', 'r') as f:
        data = f.readlines()
        length_of_matrix = int(data[0])
        no_of_officers = int(data[1])
        no_of_vehicles = int(data[2])
        board = np.zeros((length_of_matrix, length_of_matrix))
        for item in data[3:]:
            splitted = item.strip('\n').split(',')
            board[int(splitted[1])][int(splitted[0])] = board[int(splitted[1])][int(splitted[0])] + 1
    for j in range(0, length_of_matrix):
        for i in range(0, length_of_matrix):
            frequency_scooter.append((i, j, board[j][i]))
    dtype = [('column', int), ('row', int), ('count', long)]
    temp_sorted = np.array(frequency_scooter, dtype=dtype)
    frequency_sorted = np.sort(temp_sorted, order='count')
    frequency_sorted = frequency_sorted[::-1]


def main():
    global a
    a = time.time()
    fetch_values()
    initalize_matrix()
    place_officers()

if __name__ == '__main__':
    main()


# I have learnt Branch and bound algo for n queen from geeks for geeks
