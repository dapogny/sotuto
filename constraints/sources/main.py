#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import os
import sys
import numpy as np
import subprocess
import path
import inout
import mshtools
import lstools
import inigeom
import mechtools
from nullspace_optimizer import *

###############################################################
##################      START PROGRAM    ######################
###############################################################

print("*************************************************")
print("********************* SO Demo *******************")
print("*************************************************")

# Initialize folders and exchange files
inout.iniWF()

# Test the links with external C libraries
inout.testLib()

# Creation of the initial mesh
inigeom.iniGeom(path.step(0,"mesh"))

# Resolution of the NC elasticity systems associated to all individual loads
print("Resolution of the linear elasticity systems.")
for i in range(0,path.NC) :
  refneu = path.REFNEU + i
  gx     = path.GX[i]
  gy     = path.GY[i]
  ui     = path.step(0,"u."+str(i)+".sol")
  mechtools.elasticity(path.step(0,"mesh"),refneu,gx,gy,ui)

# Calculation of the upper bound for compliance, and print to the path.EXCH file
print("Calculation of upper bound for compliance.")
Cptab = []
for i in range(0,path.NC) :
  Cp = mechtools.compliance(path.step(0,"mesh"),path.step(0,"u."+str(i)+".sol"))
  Cptab.append(Cp)

path.CTARG = path.CTARGPC * max(Cptab)

# Initial values of the objective and constraint functions
J  = mechtools.volume(path.step(0,"mesh"))
H  = [Cp - path.CTARG for Cp in Cptab]

#################### Definition of Optimizable class Bridge ###################
class Bridge(Optimizable) :

  # Constructor
  def __init__(self) :
    super().__init__()
    self.ucomputed = True                    # When initializing algorithm, the states have been computed
    self.sensitivity_computed = False        # When initializing algorithm, the sensitivities have not been computed
    self.obj = (J,H)                         # When initializing algorithm, the objective has been computed
    self.nconstraints = 0                    # Number of equality constraints
    self.nineqconstraints = path.NC          # Number of inequality constraints
    
  # Initialization
  def x0(self) :
    return path.step(0,"mesh")
  
  # Calculation of the objective and constraint functions
  def evalObjective(self,x) :
    nam = x.rpartition('.')[0] # Radical in the name of the mesh
    if not self.ucomputed :
      print("  Resolution of the linear elasticity systems")

      # Calculate u
      for i in range(0,path.NC) :
        refneu = path.REFNEU + i
        gx     = path.GX[i]
        gy     = path.GY[i]
        ui     = nam + ".u."+str(i)+".sol"
        mechtools.elasticity(x,refneu,gx,gy,ui)
      self.ucomputed = True
      
      # Calculate J and H
      J = mechtools.volume(x)
      Cptab = []
      for i in range(0,path.NC) :
        Cp = mechtools.compliance(x,nam+".u."+str(i)+".sol")
        Cptab.append(Cp)
      H = [Cp - path.CTARG for Cp in Cptab]
      self.obj = (J,H)
      
    return self.obj
  
  # Calculate objective function
  def J(self,x) :
    (J,H) = self.evalObjective(x)
    return J

  # Calculate all inequality constraint functions and return the list of them
  def H(self,x) :
    (J,H) = self.evalObjective(x)
    return H
  
  # Shape derivatives, sensitivity of objective and constraint
  def evalSensitivities(self,x) :
    nam = x.rpartition('.')[0]
    if not self.sensitivity_computed :
      
      # Calculate dJ and gradJ
      mechtools.gradV(x,nam+".diffV.sol",nam+".gradV.sol")

      # Calculate dH and gradH
      for i in range(0,path.NC) :
        mechtools.gradCp(x,nam+".u."+str(i)+".sol",nam+".diffCp."+str(i)+".sol",nam+".gradCp."+str(i)+".sol")

      self.sensitivity_computed = True
      
      # Read all tables
      # dJ = list of np values ; dH = NC lines, np columns ; gradJ = list of np values ; gradH = path.NC * ndof list
      dJ    = inout.loadSol(nam+".diffV.sol")
      gradJ = inout.loadSol(nam+".gradV.sol")
      dH = []
      gradH = []
      for i in range(0,path.NC) :
        dHi = inout.loadSol(nam+".diffCp."+str(i)+".sol")
        dH.append(dHi)
        gradHi = inout.loadSol(nam+".gradCp."+str(i)+".sol")
        gradH.append(gradHi)
      
      self.sensitivities = (dJ,dH,gradJ,gradH)
    
    return self.sensitivities
  
  # List with ndof elements
  def dJ(self,x) :
    (dJ,dH,gradJ,gradH) = self.evalSensitivities(x)
    return dJ
  
  # dH = array with path.NC lines, and ndof columns
  def dH(self,x) :
    (dJ,dH,gradJ,gradH) = self.evalSensitivities(x)
    return dH
        
  # Gradient and transpose
  def dJT(self,x) :
    (dJ,dH,gradJ,gradH) = self.evalSensitivities(x)
    return gradJ
    
  def dHT(self,x) :
    (dJ,dH,gradJ,gradH) = self.evalSensitivities(x)
    return np.asarray(gradH).T
    
  # Retraction : shape update
  # dx = array of np values containing values of the scalar velocity field
  def retract(self, x, dx) :
    nam = x.rpartition('.')[0]
    it = int(nam.rpartition('.')[2])
    curmesh = x
    curphi  = nam + ".phi.sol"
    curgrad = nam + ".grad.sol"
    newmesh = path.step(it+1,"mesh")
    newphi  = path.step(it+1,"phi.sol")

    # Assume that the next computations will be performed on a new mesh
    self.sensitivity_computed = False
    self.ucomputed = False
    
    # Generation of a level set function for $\Omega^n$ on $D$
    print("  Creation of a level set function")
    lstools.mshdist(curmesh,curphi)

    # Put scalar velocity defined on D into the normal direction
    inout.saveSol(dx,path.TMPSOL)
    lstools.norvec(curmesh,curphi,path.TMPSOL,curgrad)
    
    # Advection of the level set function
    print("  Level Set advection")
    lstools.advect(curmesh,curphi,curgrad,1.0,newphi) # time step taken into account in calculation of descent
    
    # Creation of a mesh associated to the new shape
    print("  Local remeshing")
    retmmg = mshtools.mmg2d(curmesh,1,newphi,path.HMIN,path.HMAX,path.HAUSD,path.HGRAD,1,newmesh)
    return newmesh
    
  # Accept step
  def accept(self,results) :
    it    = len(results['J'])-1
    print("\n***************************************************")
    print("********            Iteration {}            ********".format(it))
    print("***************************************************")
    (J,H) = self.obj
    inout.printHisto(it,J,H)
    pass
    
################ End of definition of Optimizable class Bridge() ###############

# Run optimization solver
optSettings = {"dt" : path.MESHSIZ,
               "alphaJ" : 1.0,
               "alphaC" : 2.0,
               "maxit" : 300,
               "provide_gradient" : True,
               "maxtrials" : 3,
               "itnormalisation" : 3
              }
results=nlspace_solve(Bridge(), optSettings)

    
###############################################################
####################       END PROGRAM      ###################
###############################################################

print("*************************************************")
print("****************** End of SO Demo ***************")
print("*************************************************")
