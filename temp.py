import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})

print(df.mul([1, 2, 3]).sum(axis=1).divide(1))
