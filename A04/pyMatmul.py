def matmul(A, B):
    '''Return the matrix product of two 2D n x n lists'''
    n = len(A) 
    C = []
    #Initialze C to a 2D list of n x n filled with 0s
    for r in range(n):
        C.append([0] * n)

    #https://stackoverflow.com/questions/10508021/matrix-multiplication-in-pure-python
    #I used this to help me, but I changed it a bit
    #Since both arrays are n x n I don't need to individually get the len of each column 
    # or check if they can be multiplied
    for r in range(n):
        for B_col_v in range(n):
            for A_col_v in range(n):
                #sum all of the values in the same row of A and the same column of B
                C[r][B_col_v] += A[r][A_col_v] * B[A_col_v][B_col_v]
    return C