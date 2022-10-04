#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import subprocess
import os
import sys
import path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

print("**********************************************")
print("**********       Plot histogram      *********")
print("**********************************************")

# Load histogram
itl    = []
voll   = []
Cpl    = []

fin = open(path.HISTO,'r')

content = fin.read()
lst = content.split()

# Number of columns and rows
nc  = path.NC + 2
nit = len(lst) // nc
Cpl = np.zeros((path.NC,nit))

for n in range(0,nit) :
  it   = int(lst[nc*n])
  vol  = float(lst[nc*n+1])
  itl.append(it)
  voll.append(vol)
  
  for k in range(0,path.NC) :
    Cp         = float(lst[nc*n+2+k])
    Cpl[k,it]  = Cp

fin.close()

#Set integer ticker for the x axis
fig, axs = plt.subplots(1,2,figsize=(12,5),constrained_layout=False)

# Set title and axes
axs[0].set_title("Evolution of volume",fontsize=10)
axs[1].set_title("Evolution of compliance",fontsize=10)
axs[0].set_xlabel("Iterations")
axs[0].set_ylabel("Volume")
axs[1].set_xlabel("Iterations")
axs[1].set_ylabel("Compliance")

# Plot
axs[0].plot(itl,voll)
line = axs[1].plot(itl,np.zeros(nit),label="Constraint threshold")
for k in range(0,path.NC) :
  axs[1].plot(itl,Cpl[k,:])
  
axs[0].axis([0,max(itl),min(voll),max(voll)])
axs[1].axis([0,max(itl),np.amin(Cpl),np.amax(Cpl)])
fig.suptitle("Evolution of the volume and compliance of the structure",fontsize=12,fontweight="bold")
fig.tight_layout()
axs[1].legend()
plt.show()

#################################################
################# END PROGRAM ###################
#################################################

print("**********************************************")
print("**************    End of Plot   **************")
print("**********************************************")
