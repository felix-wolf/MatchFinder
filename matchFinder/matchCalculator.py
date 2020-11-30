from munkres import Munkres, print_matrix
import pandas as pd
import numpy as np
import random

def calculateMatch(file):
    df = pd.read_csv(file)
    newDf = df.replace([np.NAN, "Sechstwahl", "Fünftwahl", "Viertwahl", "Drittwahl", "Zweitwahl", "Erstwahl"],
        [np.infty, 6, 5, 4, 3, 2, 1],)
    #for item in df.values.tolist():
    #   print(item)
    newDf = newDf.iloc[:,1:]
    matrix = np.array(newDf.values.tolist()).tolist()
    random.shuffle(matrix)
    indexes = Munkres().compute(matrix)
    print(indexes)
    print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = matrix[row][column]
        total += value
        print(f'({row}, {column}) -> {value}')
        #print(df[row, column])
    print(f'total cost: {total}, lowest possible cost: {len(matrix)}')
