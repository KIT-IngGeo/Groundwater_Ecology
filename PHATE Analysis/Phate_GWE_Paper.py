# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 11:50:45 2021

@author: Fabien Koch
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 15:37:59 2020

@author: Fabien Koch
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import MDS
from sklearn.metrics import euclidean_distances
from sklearn.preprocessing import StandardScaler
import phate

# read data file and define names of columns 

data = pd.read_csv ('Data PHATE.txt', sep='\t', index_col=None, header=0, 
                    names=[ 'name', 'depth', 'oxygen', 'GWT', 'GWT_SD', 'elec_cond', 'pH', 'iron',
                           'phosphate', 'nitrate', 'detritus', 'sediment', 'num_taxa', 'num_ind', 'shannon',
                           'geology', 'per_crust', 'per_oligos', 'GFI', 'amphipods', 'cyclops', 'parast', 'land use', 'bathy', 'nematoda'])

# --------  Data preparation -----------

target = 'land use'  #define target value: divides data and  colours points in the diagram 
n_comp = 2


data_x = data[['depth', 'GWT', 'nitrate', 'phosphate', 'detritus', 'geology', 
               'num_taxa', 'num_ind', 'shannon', 'per_crust', 'per_oligos', 'amphipods', 'cyclops', 'parast', 'bathy']]  # choise of used parameters


print (data_x)

data_x = StandardScaler().fit_transform(data_x) # standardize parameters 

data_y = data[target] # define target parameter


# --------  Performance PHATE -----------

phate_op = phate.PHATE()
data_phate = phate_op.fit_transform(data_x)


principalDf = pd.DataFrame(data = data_phate   # create dataframe for presenting the data
             , columns = ['PHATE 1', 'PHATE 2'])
finalDf = pd.concat([principalDf, data_y, data['name'], data['GWT']], axis = 1)

# %%-------- Result presentation ---------
fig2 = plt.figure(2, figsize=(8, 6))

ax = fig2.add_axes([0.08, 0.08, 0.88, 0.88])

targets = [1, 2]
colors = ['r', 'b']

for target, color in zip(targets,colors):
    indicesToKeep = finalDf['land use'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'PHATE 1']
                , finalDf.loc[indicesToKeep, 'PHATE 2']
                , c = color
                , s = 50)

for label, x, y in zip(finalDf['name'], principalDf['PHATE 1'], principalDf['PHATE 2']):
    plt.annotate(
        label,
        xy=(x, y), xytext=(-5, 5),
        textcoords='offset points', ha='right', va='bottom')


ax.set_xlabel("PHATE 1")
ax.set_ylabel("PHATE 2")
ax.legend(['urban area', 'forest'])

plt.savefig('PHATE Analysist.png') #Diagramm speichern
plt.savefig('PHATE Analysist.eps') #Diagramm speichern
plt.savefig('PHATE Analysist.pdf') #Diagramm speichern

