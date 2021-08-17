import pandas as pd

n_rows = 1000000
columns = [f"column_{i}" for i in range(1, 25)]
dummy_column_values = list(range(0, n_rows))
data = { col: dummy_column_values for col in columns}
df = pd.DataFrame(data)

df.to_csv('data/data.csv')