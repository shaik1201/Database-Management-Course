cols = ['a', 'b']
rows = [[1, 2], [3, 4]]

x = [dict(zip(cols, row)) for row in rows]
print(x)