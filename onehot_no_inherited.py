import pandas as pd

data = pd.read_excel('41467_2021_22809_MOESM3_ESM.xlsx', sheet_name='All Structures')

col_list = []
col_list.extend(pd.unique(data['Space Group']).tolist())            #1
col_list.extend(pd.unique(data['Global Point Group']).tolist())     #2
local_point = []
local_point.extend(pd.unique(data['Local Point Groups']).tolist())     #3
new_list = []
for i in range(len(local_point)):
    if ',' in local_point[i]:
        new_list.extend(local_point[i].replace(' ', '').split(','))
    else:
        new_list.extend(local_point[i])
col_list.extend(pd.unique(new_list))
col_list.extend(pd.unique(data['Lattice Type']).tolist())           #5
col_list.extend(pd.unique(data['Centering']).tolist())              #6

df_new = pd.DataFrame(columns = col_list)

for i in range(len(data.index)):
    data_anal = data.iloc[i]
    row_list = []

    df = pd.DataFrame(pd.unique(data['Space Group']), columns = ['Space Group'])
    space = [data_anal['Space Group']]
    row_list.extend(df['Space Group'].isin(space).astype(int).tolist())

    df = pd.DataFrame(pd.unique(data['Global Point Group']), columns = ['Global Point Group'])
    glob = [data_anal['Global Point Group']]
    row_list.extend(df['Global Point Group'].isin(glob).astype(int).tolist())

    df = pd.DataFrame(pd.unique(new_list), columns = ['Local'])
    local = data_anal['Local Point Groups'].replace(' ','').split(',')
    row_list.extend(df['Local'].isin(local).astype(int).tolist())

    df = pd.DataFrame(pd.unique(data['Lattice Type']), columns = ['Lattice Type'])
    lattice = [data_anal['Lattice Type']]
    row_list.extend(df['Lattice Type'].isin(lattice).astype(int).tolist())

    df = pd.DataFrame(pd.unique(data['Centering']), columns = ['Centering'])
    cent = [data_anal['Centering']]
    row_list.extend(df['Centering'].isin(cent).astype(int).tolist())

    df_new.loc[i] = row_list

df_new.to_csv('crystal_info_no_inherited.csv', index=False)
