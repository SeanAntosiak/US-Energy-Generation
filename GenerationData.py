import numpy as np
import pandas as pd

# importing dataframe from a csv in my GitHub
gen0 = pd.read_csv('https://github.com/SeanAntosiak/LS-DS6-Unit-1-Project-Files/blob/master/datasets/annual_generation_state.csv?raw=true',  # noqa
                    skiprows=1, thousands=',')

# takes only the rows corosponding to state total generation
gen0 = gen0[gen0['TYPE OF PRODUCER'] == 'Total Electric Power Industry']

# removes the type of producer column since it's all the same (state total)
gen = gen0.drop(columns=['TYPE OF PRODUCER'])

# changes both instances of 'US total' to have the same name
gen['STATE'].replace({'US-Total': 'US', 'US-TOTAL': 'US'}, inplace=True)

# renames columns
gen.rename(columns={'ENERGY SOURCE': 'SOURCE',
                    'GENERATION (Megawatthours)': 'Mwh'},
           inplace=True)

# converts Megawatthours coulumn to Intiger
gen['Mwh'] = gen['Mwh'].apply(int)
