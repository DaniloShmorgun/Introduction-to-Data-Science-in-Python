import pandas as pd
import numpy as np
import re

# a = np.arange(8)
# b = a[4:6]
# print(a)
# print(b)
# b[:] = 40
# print(b)
# c = a[4] + a[6]
# print(c)


# def result():
#     s = 'ACAABAACAAABACDBADDDFSDDDFFSSSASDAFAAACBAAAFASD'

#     result = []
#     # compete the pattern below
#     pattern = '.{1}(?=AAA)'
#     for item in re.finditer(pattern,s):
#       # identify the group number below.
#       result.append(item.group())
      
#     return result

# t = result()
# print(t)

# df = pd.Series(data=[4, 7, -5, 3], index=['d', 'b','a','c'])
# print(df.index[0])

S = pd.Series(np.arange(5), index=['a', 'b', 'c', 'd', 'e'])
print(S[['b', 'c', 'd']])
print(S['b':'e'])