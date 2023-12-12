matrix = []
a = []
s = input()
while "end" not in s:
    a.append([int(i) for i in s.split()])
    print(a)
    matrix.append(a.copy())
    s=input()
else:
    print(matrix)