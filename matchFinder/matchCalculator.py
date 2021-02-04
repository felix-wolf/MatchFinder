from munkres import Munkres, print_matrix, DISALLOWED
from operator import itemgetter
import pandas as pd
import numpy as np
import random
import copy

def calculateFromCSV(file):
    """
    process data from a csv file into a form the the system can handle

    Parameter
    ----------
    file : []
        the file that holds the data

    Returns
    ----------
    []
        the results
    """

    # read csv file
    df = pd.read_csv(file)
    # replace strings with numbers
    full_matrix = df.replace(
        [np.NAN, "Veto", "Zehntwahl", "Neuntwahl", "Achtwahl", "Siebtwahl",
        "Sechstwahl", "Fünftwahl", "Viertwahl", "Drittwahl", "Zweitwahl", "Erstwahl"],
        [100, DISALLOWED, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    # convert pandas matrix to 2d list
    themen = full_matrix.columns.tolist()
    # pop names
    themen.pop(0)
    # convert matrix to list
    full_matrix = np.array(full_matrix.values.tolist()).tolist()
    return calculateMatchFromList(full_matrix, themen)

def calculateMatchFromList(full_matrix, themen):
    """
    calculate a number of matches from a list input.
    refer to line comments for more details

    Parameter
    ----------
    full_matrix : []
        multi-dimensional array holding the data
    themen: [Thema]
        list of available themen

    Returns
    ----------
    []
        the results
    """

    assignment = []
    # do below number of rows times, to fully rotate the matrix
    for x in range(len(full_matrix)):
        local_assignment = {}
        # rotate the list
        rotate_list(full_matrix, 1)
        # copy the list
        reduced_matrix = copy.deepcopy(full_matrix)
        # delete names of teilnehmer, convert strings to numbers
        for row in range(len(reduced_matrix)):
            for column in range(len(reduced_matrix[row]) - 1):
                if column == 0:
                    reduced_matrix[row].pop(column)
                reduced_matrix[row][column] = int(float(reduced_matrix[row][column]))
        # calculate match
        indexes = Munkres().compute(reduced_matrix)
        #print(indexes)
        #print_matrix(reduced_matrix, msg='Lowest cost through this matrix:')
        total = 0
        studis = []
        for row, column in indexes:
            value = reduced_matrix[row][column]
            total += value
            #print(f'({row}, {column}) -> {value}')
            #print(full_matrix[row][column])
            studis.append([str(full_matrix[row][0]), themen[column], value])
        studis = sorted(studis, key=itemgetter(0))
        local_assignment["studis"] = studis
        local_assignment['total'] = total
        #print(f'total cost: {total}, lowest possible cost: {len(reduced_matrix)}')
        #print(local_assignment)
        assignment.append(local_assignment)

    # remove all duplicates from the list
    for firstassignment in assignment:
        for secondAssignment in assignment:
            if firstassignment == secondAssignment and firstassignment is not secondAssignment:
                assignment.pop(assignment.index(secondAssignment))

    return (assignment)

def rotate_list(lst, x):
    """
    Rotates a matrix given as a list x number of times

    Parameter
    ----------
    lst : []
        the list to rotate
    x : number
        number of rotations to perform

    Returns
    ----------
    []
        the rotated list
    """

    lst[:] =  lst[-x:] + lst[:-x]