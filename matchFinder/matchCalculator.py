from munkres import Munkres, print_matrix
import pandas as pd
import numpy as np



def calculateMatch(file):
    df = pd.read_csv(file)
    df.replace([np.NAN, "Sechstwahl", "Fünftwahl", "Viertwahl", "Drittwahl", "Zweitwahl", "Erstwahl"],[np.infty, 6, 5, 4, 3, 2, 1], inplace=True)
    df = df.iloc[:,1:]
    matrix = np.array(df.values.tolist())
    print(matrix)
    m = Munkres()
    matrix = [[1, 2, 3, 4],
                [4, 3, 2, 1],
                [1, 3, 2, 4],
                [4, 2, 3, 1]]
    indexes = m.compute(matrix)
    print(indexes)
    print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = matrix[row][column]
        total += value
        print(f'({row}, {column}) -> {value}')
    print(f'total cost: {total}')