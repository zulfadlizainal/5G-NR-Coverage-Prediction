#Created by github.com/zulfadlizainal

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

#Ignore warning if calculation devide by 'zero' or 'Nan'
np.seterr(divide='ignore', invalid='ignore')

df_antpat = pd.read_excel('Antenna_Pattern.xlsx', encoding='utf-8_sig')
df_cellparam = pd.read_excel('Cell_Parameter.xlsx', encoding='utf-8_sig')

# Create Indicators

split_H = df_antpat['ANTENNA_ELEMENT'].str.split('V', expand=True)
split_V = split_H.iloc[:, 1].str.split('(', expand=True)
HBeam = split_H.iloc[:, 0]
VBeam = 'V' + split_V.iloc[:, 0]
del split_H, split_V

# Create Info Table

cols = list(df_antpat.columns)
df_antpat_info = df_antpat[[cols[0]] + [cols[2]] + [cols[1]] + [cols[5]] + [cols[4]]]
df_antpat_info = pd.concat([df_antpat_info, HBeam, VBeam], axis=1)
del cols, HBeam, VBeam

df_antpat_info.columns = ['Antenna Name', 'Vendor', 'Gain (dBi)', 'Etilt (°)', 'Pattern', 'HBW', 'VBW']
cols = list(df_antpat_info)
df_antpat_info = df_antpat_info[cols[0:4] + cols[5:7] + [cols[4]]]
df_antpat_display = df_antpat_info.loc[:, 'Antenna Name':'VBW']
del cols

# Print List of Antenna Patten

print(' ')
print('### List of Antenna Pattern Database ###')
print(' ')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df_antpat_display)

print(' ')
print('### End of List ###')
print(' ')

#Mapping Cell_Parameter

height_cell_1 = df_cellparam.iloc[1,1] - df_cellparam.iloc[0,1]
height_cell_2 = df_cellparam.iloc[1,2] - df_cellparam.iloc[0,2]
height_cell_3 = df_cellparam.iloc[1,3] - df_cellparam.iloc[0,3]

azi_cell_1 = df_cellparam.iloc[2,1]
azi_cell_2 = df_cellparam.iloc[2,2]
azi_cell_3 = df_cellparam.iloc[2,3]

mtilt_cell_1 = df_cellparam.iloc[3,1]
mtilt_cell_2 = df_cellparam.iloc[3,2]
mtilt_cell_3 = df_cellparam.iloc[3,3]

ssbpower_cell_1 = df_cellparam.iloc[4,1]
ssbpower_cell_2 = df_cellparam.iloc[4,2]
ssbpower_cell_3 = df_cellparam.iloc[4,3]

freq_cell_1 = df_cellparam.iloc[5,1]
freq_cell_2 = df_cellparam.iloc[5,2]
freq_cell_3 = df_cellparam.iloc[5,3]

#Antenna Pattern Selection

pattern_cell_1 = int(input("Cell 1 Antenna Pattern: "))
pattern_cell_2 = int(input("Cell 2 Antenna Pattern: "))
pattern_cell_3 = int(input("Cell 3 Antenna Pattern: "))

####################################Cell 1 Preparation################################

#Prepare dataframe for selected antenna - Cell 1

antpat1 = df_antpat_info.loc[pattern_cell_1,'Pattern']
antpat1 = antpat1.split(' ')
antpat1 = pd.DataFrame(antpat1)
antpat1.drop(antpat1.index[[0,1,2,3,724,725,726,727,1448,1449,1450]], inplace = True)
antpat1 = antpat1.reset_index(drop=True)

#Seperate Horizontal and Vertical DataFrame - Cell 1

antpat_H1 = antpat1.iloc[0:720,:]
antpat_H1 = antpat_H1.reset_index(drop=True)
antpat_V1 = antpat1.iloc[720:1440,:]
antpat_V1 = antpat_V1.reset_index(drop=True)

antpat_H_Deg1 = antpat_H1.iloc[::2] #Extract Odd Row Index DataFrame
antpat_H_Deg1 = antpat_H_Deg1.reset_index(drop=True)
antpat_H_Loss1 = antpat_H1.iloc[1::2] #Extract Even Row Index Dataframe
antpat_H_Loss1 = antpat_H_Loss1.reset_index(drop=True)

antpat_V_Deg1 = antpat_V1.iloc[::2] #Extract Odd Row Index DataFrame
antpat_V_Deg1 = antpat_V_Deg1.reset_index(drop=True)
antpat_V_Loss1 = antpat_V1.iloc[1::2] #Extract Even Row Index Dataframe
antpat_V_Loss1 = antpat_V_Loss1.reset_index(drop=True)

antpat_df1 = pd.concat([antpat_H_Deg1, antpat_H_Loss1, antpat_V_Loss1], axis = 1)
antpat_df1.columns = ['Angle', 'H_Loss', 'V_Loss']
antpat_df1['Angle'] = antpat_df1['Angle'].astype(int)
antpat_df1['H_Loss'] = antpat_df1['H_Loss'].astype(float)
antpat_df1['V_Loss'] = antpat_df1['V_Loss'].astype(float)

cols = list(antpat_df1)
antpat_df_H_Cell_1 = antpat_df1[cols[0:2]]
antpat_df_V_Cell_1 = antpat_df1[cols[0:1] + [cols[2]]]

del cols, antpat1, antpat_H1, antpat_H_Deg1, antpat_H_Loss1, antpat_V1, antpat_V_Deg1, antpat_V_Loss1, antpat_df1

#Shift dataframe based on Azimuth and Tilt - Cell 1

hloss_cell_1 = antpat_df_H_Cell_1['H_Loss'].tolist()
vloss_cell_1 = antpat_df_V_Cell_1['V_Loss'].tolist()

def rotate(l, n):
    return l[-n:] + l[:-n]

hloss_cell_1 = rotate(hloss_cell_1, azi_cell_1)
vloss_cell_1 = rotate(vloss_cell_1, mtilt_cell_1)

del antpat_df_H_Cell_1, antpat_df_V_Cell_1

####################################Cell 2 Preparation################################

#Prepare dataframe for selected antenna - Cell 2

antpat2 = df_antpat_info.loc[pattern_cell_2,'Pattern']
antpat2 = antpat2.split(' ')
antpat2 = pd.DataFrame(antpat2)
antpat2.drop(antpat2.index[[0,1,2,3,724,725,726,727,1448,1449,1450]], inplace = True)
antpat2 = antpat2.reset_index(drop=True)

#Seperate Horizontal and Vertical DataFrame - Cell 2

antpat_H2 = antpat2.iloc[0:720,:]
antpat_H2 = antpat_H2.reset_index(drop=True)
antpat_V2 = antpat2.iloc[720:1440,:]
antpat_V2 = antpat_V2.reset_index(drop=True)

antpat_H_Deg2 = antpat_H2.iloc[::2] #Extract Odd Row Index DataFrame
antpat_H_Deg2 = antpat_H_Deg2.reset_index(drop=True)
antpat_H_Loss2 = antpat_H2.iloc[1::2] #Extract Even Row Index Dataframe
antpat_H_Loss2 = antpat_H_Loss2.reset_index(drop=True)

antpat_V_Deg2 = antpat_V2.iloc[::2] #Extract Odd Row Index DataFrame
antpat_V_Deg2 = antpat_V_Deg2.reset_index(drop=True)
antpat_V_Loss2 = antpat_V2.iloc[1::2] #Extract Even Row Index Dataframe
antpat_V_Loss2 = antpat_V_Loss2.reset_index(drop=True)

antpat_df2 = pd.concat([antpat_H_Deg2, antpat_H_Loss2, antpat_V_Loss2], axis = 1)
antpat_df2.columns = ['Angle', 'H_Loss', 'V_Loss']
antpat_df2['Angle'] = antpat_df2['Angle'].astype(int)
antpat_df2['H_Loss'] = antpat_df2['H_Loss'].astype(float)
antpat_df2['V_Loss'] = antpat_df2['V_Loss'].astype(float)

cols = list(antpat_df2)
antpat_df_H_Cell_2 = antpat_df2[cols[0:2]]
antpat_df_V_Cell_2 = antpat_df2[cols[0:1] + [cols[2]]]

del cols, antpat2, antpat_H2, antpat_H_Deg2, antpat_H_Loss2, antpat_V2, antpat_V_Deg2, antpat_V_Loss2, antpat_df2

#Shift dataframe based on Azimuth and Tilt - Cell 2

hloss_cell_2 = antpat_df_H_Cell_2['H_Loss'].tolist()
vloss_cell_2 = antpat_df_V_Cell_2['V_Loss'].tolist()

def rotate(l, n):
    return l[-n:] + l[:-n]

hloss_cell_2 = rotate(hloss_cell_2, azi_cell_2)
vloss_cell_2 = rotate(vloss_cell_2, mtilt_cell_2)

del antpat_df_H_Cell_2, antpat_df_V_Cell_2


####################################Cell 3 Preparation################################

#Prepare dataframe for selected antenna - Cell 3

antpat3 = df_antpat_info.loc[pattern_cell_3,'Pattern']
antpat3 = antpat3.split(' ')
antpat3 = pd.DataFrame(antpat3)
antpat3.drop(antpat3.index[[0,1,2,3,724,725,726,727,1448,1449,1450]], inplace = True)
antpat3 = antpat3.reset_index(drop=True)

#Seperate Horizontal and Vertical DataFrame - Cell 3

antpat_H3 = antpat3.iloc[0:720,:]
antpat_H3 = antpat_H3.reset_index(drop=True)
antpat_V3 = antpat3.iloc[720:1440,:]
antpat_V3 = antpat_V3.reset_index(drop=True)

antpat_H_Deg3 = antpat_H3.iloc[::2] #Extract Odd Row Index DataFrame
antpat_H_Deg3 = antpat_H_Deg3.reset_index(drop=True)
antpat_H_Loss3 = antpat_H3.iloc[1::2] #Extract Even Row Index Dataframe
antpat_H_Loss3 = antpat_H_Loss3.reset_index(drop=True)

antpat_V_Deg3 = antpat_V3.iloc[::2] #Extract Odd Row Index DataFrame
antpat_V_Deg3 = antpat_V_Deg3.reset_index(drop=True)
antpat_V_Loss3 = antpat_V3.iloc[1::2] #Extract Even Row Index Dataframe
antpat_V_Loss3 = antpat_V_Loss3.reset_index(drop=True)

antpat_df3 = pd.concat([antpat_H_Deg3, antpat_H_Loss3, antpat_V_Loss3], axis = 1)
antpat_df3.columns = ['Angle', 'H_Loss', 'V_Loss']
antpat_df3['Angle'] = antpat_df3['Angle'].astype(int)
antpat_df3['H_Loss'] = antpat_df3['H_Loss'].astype(float)
antpat_df3['V_Loss'] = antpat_df3['V_Loss'].astype(float)

cols = list(antpat_df3)
antpat_df_H_Cell_3 = antpat_df3[cols[0:2]]
antpat_df_V_Cell_3 = antpat_df3[cols[0:1] + [cols[2]]]

del cols, antpat3, antpat_H3, antpat_H_Deg3, antpat_H_Loss3, antpat_V3, antpat_V_Deg3, antpat_V_Loss3, antpat_df3

#Shift dataframe based on Azimuth and Tilt - Cell 3

hloss_cell_3 = antpat_df_H_Cell_3['H_Loss'].tolist()
vloss_cell_3 = antpat_df_V_Cell_3['V_Loss'].tolist()

def rotate(l, n):
    return l[-n:] + l[:-n]

hloss_cell_3 = rotate(hloss_cell_3, azi_cell_3)
vloss_cell_3 = rotate(vloss_cell_3, mtilt_cell_3)

del antpat_df_H_Cell_3, antpat_df_V_Cell_3

#######################################Clear Memory#################################

del df_antpat, df_antpat_display, df_antpat_info, df_cellparam

####################################Mesh Calculation################################

#Define mesh radius in meters
grid = 200
step = 10

#Create Matrix based on Radius
col = np.arange(start = grid, stop = 0 - step, step = -step)
idx = np.arange(start = grid, stop = 0 - step, step = -step)
idx_ones = np.ones(int(grid/step) + 1)

col = col.reshape(int(grid/step)+1,1)                                                   #Change Matrix

#Create 1/4 Mesh Based on Matrix
distance_flat = np.sqrt((np.power(col,2)) + (np.power(idx,2)))                          #Flat Distance from Center Point
col_dis = col*idx_ones                                                                  #Dummy distance towards straight Lines

angle_H = np.rad2deg(np.arcsin(col_dis/distance_flat))                                  #Horizontal Angle from Center Point
angle_H = np.round(angle_H)                                                             #Round the angle

distance_hp_1 = np.sqrt((np.power(distance_flat,2)) + (np.power(height_cell_1,2)))     #Hypotenuse Distance from Cell Height (Cell 1)
distance_hp_2 = np.sqrt((np.power(distance_flat,2)) + (np.power(height_cell_2,2)))     #Hypotenuse Distance from Cell Height (Cell 2)
distance_hp_3 = np.sqrt((np.power(distance_flat,2)) + (np.power(height_cell_2,2)))     #Hypotenuse Distance from Cell Height (Cell 3)

angle_V_1 = 90 - np.rad2deg(np.arcsin(distance_flat/distance_hp_1))                    #Vertical Angle from Center Point (Cell 1)
angle_V_1 = np.round(angle_V_1)                                                        #Round the angle
angle_V_2 = 90 - np.rad2deg(np.arcsin(distance_flat/distance_hp_2))                    #Vertical Angle from Center Point (Cell 2)
angle_V_2 = np.round(angle_V_2)                                                        #Round the angle
angle_V_3 = 90 - np.rad2deg(np.arcsin(distance_flat/distance_hp_3))                    #Vertical Angle from Center Point (Cell 3)
angle_V_3 = np.round(angle_V_3)                                                        #Round the angle

#Calculate Path Loss Model - Free Space Model

fs_pl_1 = 20*np.log10(distance_hp_1) + 20*np.log10(freq_cell_1) - 27.55                #Path Loss for Cell 1
fs_pl_2 = 20*np.log10(distance_hp_2) + 20*np.log10(freq_cell_2) - 27.55                #Path Loss for Cell 2
fs_pl_3 = 20*np.log10(distance_hp_3) + 20*np.log10(freq_cell_3) - 27.55                #Path Loss for Cell 3

del grid, step, col, col_dis, idx, idx_ones
del distance_flat, distance_hp_1, distance_hp_2, distance_hp_3

####################################Create Full Mesh################################

######Path Loss (Cell 1)######

#Flip Path Loss
fs_pl_1_NE = np.flip(fs_pl_1, axis = 1)

#Prepare Dataframe
fs_pl_1 = pd.DataFrame(fs_pl_1)                                                 #Convert array to Dataframe

fs_pl_1_NE = pd.DataFrame(fs_pl_1_NE)                                           #Convert array to Dataframe
fs_pl_1_NE = fs_pl_1_NE.iloc[:,1:]                                              #Remove redundant columns

fs_pl_1 = pd.concat([fs_pl_1, fs_pl_1_NE], axis = 1, sort = False)              #First half of the Mesh
fs_pl_1_S = fs_pl_1.values                                                      #Switch to array because dataframe cannot flip
fs_pl_1_S = np.flip(fs_pl_1_S, axis = 0)                                        #Create 2nd half of the Mesh
fs_pl_1_S = pd.DataFrame(fs_pl_1_S)
fs_pl_1_S = fs_pl_1_S.iloc[1:,:]

fs_pl_1.columns = fs_pl_1_S.columns                                             #Standardize column 1st and 2nd half of the Mesh

fs_pl_1 = pd.concat([fs_pl_1, fs_pl_1_S], axis=0, sort=False)                   #Form a complete mesh grid
fs_pl_1 = fs_pl_1.reset_index(drop=True)

del fs_pl_1_NE, fs_pl_1_S

######Path Loss (Cell 2)######

#Flip Path Loss
fs_pl_2_NE = np.flip(fs_pl_2, axis = 1)

#Prepare Dataframe
fs_pl_2 = pd.DataFrame(fs_pl_2)                                                 #Convert array to Dataframe

fs_pl_2_NE = pd.DataFrame(fs_pl_2_NE)                                           #Convert array to Dataframe
fs_pl_2_NE = fs_pl_2_NE.iloc[:,1:]                                              #Remove redundant columns

fs_pl_2 = pd.concat([fs_pl_2, fs_pl_2_NE], axis = 1, sort = False)              #First half of the Mesh
fs_pl_2_S = fs_pl_2.values                                                      #Switch to array because dataframe cannot flip
fs_pl_2_S = np.flip(fs_pl_2_S, axis = 0)                                        #Create 2nd half of the Mesh
fs_pl_2_S = pd.DataFrame(fs_pl_2_S)
fs_pl_2_S = fs_pl_2_S.iloc[1:,:]

fs_pl_2.columns = fs_pl_2_S.columns                                             #Standardize column 1st and 2nd half of the Mesh

fs_pl_2 = pd.concat([fs_pl_2, fs_pl_2_S], axis=0, sort=False)                   #Form a complete mesh grid
fs_pl_2 = fs_pl_2.reset_index(drop=True)

del fs_pl_2_NE, fs_pl_2_S

######Path Loss (Cell 3)######

#Flip Path Loss
fs_pl_3_NE = np.flip(fs_pl_3, axis = 1)

#Prepare Dataframe
fs_pl_3 = pd.DataFrame(fs_pl_3)                                                 #Convert array to Dataframe

fs_pl_3_NE = pd.DataFrame(fs_pl_3_NE)                                           #Convert array to Dataframe
fs_pl_3_NE = fs_pl_3_NE.iloc[:,1:]                                              #Remove redundant columns

fs_pl_3 = pd.concat([fs_pl_3, fs_pl_3_NE], axis = 1, sort = False)              #First half of the Mesh
fs_pl_3_S = fs_pl_3.values                                                      #Switch to array because dataframe cannot flip
fs_pl_3_S = np.flip(fs_pl_3_S, axis = 0)                                        #Create 2nd half of the Mesh
fs_pl_3_S = pd.DataFrame(fs_pl_3_S)
fs_pl_3_S = fs_pl_3_S.iloc[1:,:]

fs_pl_3.columns = fs_pl_3_S.columns                                             #Standardize column 1st and 2nd half of the Mesh

fs_pl_3 = pd.concat([fs_pl_3, fs_pl_3_S], axis=0, sort=False)                   #Form a complete mesh grid
fs_pl_3 = fs_pl_3.reset_index(drop=True)

del fs_pl_3_NE, fs_pl_3_S


######Horizontal Degree Mesh (All Cell)######

#Rotate and Flip Horizontal Degree
angle_H_NE = np.rot90(angle_H)
angle_H_NE = np.flip(angle_H_NE, axis = 0)
angle_H_NE = np.flip(angle_H_NE, axis = 1)

angle_H_SE = np.rot90(angle_H_NE, 3)
angle_H_SE = angle_H_SE + 90

angle_H_SW = np.rot90(angle_H_SE, 3)
angle_H_SW = angle_H_SW + 90

angle_H_NW = np.rot90(angle_H_SW, 3)
angle_H_NW = angle_H_NW + 90

#Prepare Dataframe
angle_H_NE = pd.DataFrame(angle_H_NE)
angle_H_SE = pd.DataFrame(angle_H_SE)
angle_H_SW = pd.DataFrame(angle_H_SW)
angle_H_NW = pd.DataFrame(angle_H_NW)
angle_H_SE = angle_H_SE.iloc[1:,:]
angle_H_SW = angle_H_SW.iloc[1:,:-1]
angle_H_NW = angle_H_NW.iloc[:,:-1]

#Combine Dataframe to become Mesh
angle_H_N = pd.concat([angle_H_NW, angle_H_NE], axis=1, sort=False)
angle_H_N = angle_H_N.values
angle_H_N = pd.DataFrame(angle_H_N)

angle_H_S = pd.concat([angle_H_SW, angle_H_SE], axis=1, sort=False)
angle_H_S = angle_H_S.values
angle_H_S = pd.DataFrame(angle_H_S)

angle_H = pd.concat([angle_H_N, angle_H_S], axis=0, sort=False)
angle_H = angle_H.values
angle_H = pd.DataFrame(angle_H)
angle_H = angle_H.fillna(0)

del angle_H_N, angle_H_S, angle_H_NE, angle_H_SE, angle_H_SW, angle_H_NW

# TODO:  PerSector HL, VD, VL

######Horizontal Loss Mesh (All Cell)######

#Cell 1 - Horizontal Loss
hloss_mesh_cell_1 = angle_H.copy()
temp = pd.Series([])

i = 0
j = 0

for i in range(len(angle_H)):
    j = 0
    for j in range(len(angle_H)):
        temp = angle_H[i][j]
        temp = temp.astype(np.int64)
        hloss_mesh_cell_1[i][j] = hloss_cell_1[temp]

del temp, i, j

#Cell 2 - Horizontal Loss
hloss_mesh_cell_2 = angle_H.copy()
temp = pd.Series([])

i = 0
j = 0

for i in range(len(angle_H)):
    j = 0
    for j in range(len(angle_H)):
        temp = angle_H[i][j]
        temp = temp.astype(np.int64)
        hloss_mesh_cell_2[i][j] = hloss_cell_2[temp]

del temp, i, j

#Cell 3 - Horizontal Loss
hloss_mesh_cell_3 = angle_H.copy()
temp = pd.Series([])

i = 0
j = 0

for i in range(len(angle_H)):
    j = 0
    for j in range(len(angle_H)):
        temp = angle_H[i][j]
        temp = temp.astype(np.int64)
        hloss_mesh_cell_3[i][j] = hloss_cell_3[temp]

del temp, i, j
