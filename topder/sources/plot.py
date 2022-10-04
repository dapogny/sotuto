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
Cpl    = []
voll   = []

fin = open(path.HISTO,'r')
content = fin.read()
lst = content.split()

# Number of rows
nit = len(lst) // 3

for n in range(0,nit) :
  it   = int(lst[3*n])
  Cp   = float(lst[3*n+1])
  vol  = float(lst[3*n+2])
  itl.append(it)
  Cpl.append(Cp)
  voll.append(vol)

fin.close()

#Set integer ticker for the x axis
fig, axs = plt.subplots(1,2,figsize=(12,5),constrained_layout=False)

# Set title and axes
axs[0].set_title("Evolution of compliance",fontsize=10)
axs[1].set_title("Evolution of volume",fontsize=10)
axs[0].set_xlabel("iterations")
axs[0].set_ylabel("Compliance")
axs[1].set_xlabel("iterations")
axs[1].set_ylabel("Volume")

# Plot
axs[0].plot(itl,Cpl)
axs[1].plot(itl,voll)
axs[0].axis([0,max(itl),min(Cpl),max(Cpl)])
axs[1].axis([0,max(itl),min(voll),max(voll)])
fig.suptitle("Evolution of the compliance and volume of the structure",fontsize=12,fontweight="bold")
fig.tight_layout()
plt.show()


#################################################
################# END PROGRAM ###################
#################################################

print("**********************************************")
print("**************    End of Plot   **************")
print("**********************************************")
