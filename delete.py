import pandas as pd
today = pd.to_datetime("today").normalize()
print(today)