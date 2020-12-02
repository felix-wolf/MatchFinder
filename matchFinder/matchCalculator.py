from munkres import Munkres, print_matrix
import pandas as pd
import numpy as np
import random
import copy

def calculateMatch(file):
    # csv datei einlesen
    df = pd.read_csv(file)
    # strings mit zahlen ersetzen
    full_matrix = df.replace(
        [np.NAN, "Sechstwahl", "Fünftwahl", "Viertwahl", "Drittwahl", "Zweitwahl", "Erstwahl"],
        [np.infty, int(6), int(5), int(4), int(3), int(2), int(1)])
    #reduced_matrix = full_matrix.iloc[:,1:]
    # matrix zu 2d liste konvertieren
    full_matrix = np.array(full_matrix.values.tolist()).tolist()
    assignment = {}
    # matrix mischen (um jede Kombination auszuprobieren)
    for x in range(len(full_matrix)):
        local_assignment = {}
        # liste kopieren
        reduced_matrix = copy.deepcopy(full_matrix)
        # liste rotieren
        rotate(full_matrix, 1)
        # Namen entfernen, string to int konvert
        for row in range(len(reduced_matrix)):
            for column in range(len(reduced_matrix[row]) - 1):
                if column is 0:
                    reduced_matrix[row].pop(column)
                reduced_matrix[row][column] = int(reduced_matrix[row][column])
        # match berechnen
        indexes = Munkres().compute(reduced_matrix)
        #print(indexes)
        #print_matrix(reduced_matrix, msg='Lowest cost through this matrix:')
        total = 0
        for row, column in indexes:
            value = reduced_matrix[row][column]
            total += value
            #print(f'({row}, {column}) -> {value}')
            local_assignment[str(full_matrix[row][0])] = value
        #print(f'total cost: {total}, lowest possible cost: {len(reduced_matrix)}')
        #print(local_assignment)
        assignment[x] = dict(sorted(local_assignment.items()))
        #assignment['total'] = total
    for i in range(len(assignment) - 1):
        k = i + 1
        if assignment[i] == assignment[k]:
            assignment.pop(i)
    return (assignment)

def rotate(lst, x):
    lst[:] =  lst[-x:] + lst[:-x]