import pandas as pd
import numpy as np

df = pd.read_parquet('/home/meet.shingala/Desktop/Client_Project/LinkedIn_internal/RAGInvest_Flask/RAGInvest/charting_functions/Data/HDFCBANK.NS2020-01-012024-12-16.parquet')
print(df.head())
# print(len(np.array(df.index)))
# print(df.shape)
# print(df['Close'])
# print(df['Close'].index.strftime('%Y-%m-%d').tolist())
# print(df['Close']['HDFCBANK.NS'].values.tolist())
