import pandas as pd
from services.db_ops.populate_master_data import populate_disciplines_from_dataframe


path_disc = r"C:\Users\sam19\OneDrive\4. Samitha\01. Projects (C)\iplan-EPPR\EPPR-MVP\Spporting Docs\populate_discplines.xlsx"
df_disc = pd.read_excel(path_disc)

print(df_disc)

populate_disciplines_from_dataframe(df_disc)