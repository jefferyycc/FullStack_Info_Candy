from itertools import product
import pandas as pd
import sqlite3 as sql

size = [0, 5, 10, 15]
combination = product(size, size, size, size)
possbile = []
for c in combination:
    if 0 < sum(c) <= 15:
        possbile.append(list(c))
box_id = ["".join([str(d).zfill(2) for d in p]) for p in possbile]

pd.concat([pd.DataFrame(box_id), pd.DataFrame(possbile)], axis=1)
df = pd.DataFrame(possbile)
df.index = box_id
df.columns = ['C1', 'C2', 'C3', 'C4']

df = df.stack().to_frame().reset_index(level=1,col_level=0).reset_index(level=0)
df.columns = ['box_id', 'candy_name', 'candy_amount']

conn = sql.connect('app.db')
df.to_sql("Box", conn, if_exists="replace", index=False)