# Use while loop for below loop
for i in range(1, 6):
    print(f"Iteration {i}: i = {i}")


# Use while loop for below loop
for i in range(1, 4):
    for j in range(1, 4):
        print(f"Outer loop i = {i}, Inner loop j = {j}")

# Write the output of below loop
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i * j}")

# visualization
# Simple Loop
n = 5
factorial = 1
while n > 0:
    factorial *= n
    print(f"n = {n}, Current factorial = {factorial}")
    n -= 1

# Nested Loop
n = 5
for i in range(1, n + 1):
    for j in range(n - i):
        print(" ", end="")
    
    for j in range(1, i + 1):
        print(j, end="")

    for j in range(i - 1, 0, -1):
        print(j, end="")
    print()

# Break
for i in range(1, 4):
    for j in range(1, 4):
        if j == 2:
            break
        print(f"Outer loop i = {i}, Inner loop j = {j}")
    print("---- End of inner loop ----")

# Continue
for i in range(1, 4):
    for j in range(1, 4):
        if j == 2:
            continue
        print(f"Outer loop i = {i}, Inner loop j = {j}")
    print("---- End of inner loop ----")

# Problems
# 1. Print the below Pattern using loop
"""

*
**
***
****
***** 

"""
# 2. print the numbers in below pattern.
"""
(1, 1)
(1, 2)
(1, 3)
(1, 4)
(1, 5)
(1, 6)
(2, 2)
(2, 4)
(2, 6)
(3, 3)
(3, 6)
(4, 4)

"""

# 3. Find the Transpose of a matrix 
n = 5
for i in range(1, n + 1):
    print(f"Generating Row {i}: ", end='')
    
    for j in range(i):
        print('*', end='')
    
    print()

print("Pattern printing completed!")


n1 = 4
n2 = 6

i = 1
while i <= n1:
    j = 1
    while j <= n2:
        if j % i == 0:
            print(f"({i}, {j})")
        j += 1
    i += 1

A = [
    [1, 2, 3],
    [4, 5, 6]
]

m = len(A)
n = len(A[0])

A_T = [[0 for _ in range(m)] for _ in range(n)]
i = 0
while i < m:
    j = 0
    while j < n:
        A_T[j][i] = A[i][j]
        j += 1
    i += 1

for row in A_T:
    print(row)
