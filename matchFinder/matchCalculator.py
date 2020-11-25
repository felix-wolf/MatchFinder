from munkres import Munkres, print_matrix

def calculateMatch():
    m = Munkres()
    matrix = [[5, 9, 1],
          [10, 3, 2],
          [8, 7, 4]]
    indexes = m.compute(matrix)
    print(indexes)
    print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = matrix[row][column]
        total += value
        print(f'({row}, {column}) -> {value}')
    print(f'total cost: {total}')