def mult_scalar(matrix, scale):
    # multiplies each individual element within matrix by scale
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] *= scale

    return matrix

def mult_matrix(a, b):
    # returns None if the two matrices are incompatible for multiplication
    if len(a[0]) != len(b):
        return None
    # transposes matrix b (swaps rows with columns)
    bChanged = []
    for i in range(len(b[0])):
        bChanged.append([])
        for k in range(len(b)):
            bChanged[i].append(b[k][i])

    matrix = []
    for i in range(len(a)):
        # adds a new row to the product matrix
        matrix.append([])
        # multiples the first row elements of matrix a with the corresponding element in each row of matrix bChanged
        for j in range(len(bChanged)):
            # reset sum for each row in bChanged
            sum = 0
            for k in range(len(bChanged[0])):
                sum += a[i][k] * bChanged[j][k]
            # adds the product sum of each row in matrix bChanged as a new element in the product matrix (in row i)
            matrix[i].append(sum)

    return matrix

def euclidean_dist(a, b):
    sum = 0
    # gets the difference of each element in matrix a and b and square it, then add it to sum
    for i in range(len(a[0])):
        sum += (a[0][i] - b[0][i]) ** 2
    # returns the square root of sum (euclidean distance)
    return sum ** (1 / 2)
