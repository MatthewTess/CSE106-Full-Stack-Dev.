import numpy as np

A = np.array([[1,2,3],[4,5,6],[7,8,9]])
B = np.array([[3,1,4],[2,6,1],[2,9,7]])
addition = np.add(A,B)

print("Sum of matrix is A+B :\n",addition)
product = np.dot(A,B)

print("product of matrix is AxB:\n", product)
diterminate=np.linalg.det(A)

print("diterminate of matrix A is:",diterminate)
inverse = np.linalg.inv(B)

print("Inverse of matrix B is:\n",inverse)
eigen, v = np.linalg.eig(A)

print("The eigenvalue of matrix A is:\n",eigen)