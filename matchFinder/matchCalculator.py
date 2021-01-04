from munkres import Munkres, print_matrix, DISALLOWED
from operator import itemgetter
import pandas as pd
import numpy as np
import random
import copy

def calculateFromCSV(file):
    # csv datei einlesen
    df = pd.read_csv(file)
    # strings mit zahlen ersetzen
    full_matrix = df.replace(
        [np.NAN, "Veto", "Zehntwahl", "Neuntwahl", "Achtwahl", "Siebtwahl",
        "Sechstwahl", "Fünftwahl", "Viertwahl", "Drittwahl", "Zweitwahl", "Erstwahl"],
        [100, DISALLOWED, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    # matrix zu 2d liste konvertieren
    themen = full_matrix.columns.tolist()
    themen.pop(0)
    # convert matrix to list
    full_matrix = np.array(full_matrix.values.tolist()).tolist()
    return calculateMatchFromList(full_matrix, themen)

def calculate_from_db(teilnehmer_pref, themen):
    return calculateMatchFromList(teilnehmer_pref, themen)


def calculateMatchFromList(full_matrix, themen):
    assignment = []
    # matrix mischen (um jede Kombination auszuprobieren)
    for x in range(len(full_matrix)):
        local_assignment = {}
        # liste rotieren
        rotate_list(full_matrix, 1)
        # liste kopieren
        reduced_matrix = copy.deepcopy(full_matrix)
        # Namen entfernen, string to int konvert
        for row in range(len(reduced_matrix)):
            for column in range(len(reduced_matrix[row]) - 1):
                if column == 0:
                    reduced_matrix[row].pop(column)
                reduced_matrix[row][column] = int(float(reduced_matrix[row][column]))
        # match berechnen
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
    lst[:] =  lst[-x:] + lst[:-x]