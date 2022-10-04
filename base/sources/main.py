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

# Resolution of the state equation
mechtools.elasticity(path.step(0,"mesh"),path.step(0,"u.sol"))

# Calculation of the compliance and the volume of the shape
newCp  = mechtools.compliance(path.step(0,"mesh"),path.step(0,"u.sol"))
newvol = mechtools.volume(path.step(0,"mesh"))

print("*** Initialization: Compliance {} ; volume {}".format(newCp,newvol))

# Coefficient for time step ( descent direction is scaled with respect to mesh size)
coef = 1.0

# Main loop
# At the beginning of each iteration, are available:
#    - the mesh $\¢alT^n$ of $D$ associated to the current shape $\Omega^n$;
#    - the solution to the linear elasticity equation on $\Omega^n$ (at the nodes of $D$).
#    - The compliance and volume of the shape
for n in range(0,path.MAXIT) :
  curmesh = path.step(n,"mesh")
  newmesh = path.step(n+1,"mesh")
  curphi  = path.step(n,"phi.sol")
  newphi  = path.step(n+1,"phi.sol")
  curu    = path.step(n,"u.sol")
  newu    = path.step(n+1,"u.sol")
  curCpgrad = path.step(n,"CP.grad.sol")
  curVgrad = path.step(n,"V.grad.sol")
  curgrad = path.step(n,"grad.sol")
  curCp   = newCp
  curvol  = newvol
  
  print("***************************************************")
  print("Iteration {}: Compliance {} ; volume {}".format(n,curCp,curvol))
  print("***************************************************")
  
  # Print values in the path.HISTO file
  inout.printHisto(n,curCp,curvol)

  # Stop normalization of the null space direction after a certain number of iterations
  if ( n == 50 ) :
    [normXiJ] = inout.getrAtt(file=path.EXCHFILE,attname="NormXiJ")
    inout.setAtt(file=path.EXCHFILE,attname="MaxNormXiJ",attval=normXiJ)

  # Change value of tolerance after a certain number of iterations
  if ( n == 100 ) :
    path.TOL = 0.005

  # Generation of a level set function for $\Omega^n$ on $D$
  print("  Creation of a level set function")
  lstools.mshdist(curmesh,curphi)
  
  print("  Computation of a descent direction")
# Calculation of the gradients of compliance and volume
  mechtools.gradCp(curmesh,curu,curCpgrad)
  mechtools.gradV(curmesh,curVgrad)
  
  # Calculation of a descent direction
  mechtools.descent(curmesh,curphi,curCp,curCpgrad,curvol,curVgrad,curgrad)

  # Evaluation of the merit of $\Omega^n$
  merit = mechtools.merit(curCp,curvol)

  # Line search
  for k in range(0,path.MAXITLS) :
    print("  Line search k = {}".format(k))

    # Advection of the level set function
    print("    Level Set advection")
    lstools.advect(curmesh,curphi,curgrad,coef,newphi)
   
    # Creation of a mesh associated to the new shape
    print("    Local remeshing")
    retmmg = mshtools.mmg2d(curmesh,1,newphi,path.HMIN,path.HMAX,path.HAUSD,path.HGRAD,1,newmesh)

    if ( retmmg ) :
      # Resolution of the state equation on the new shape
      print("    Resolution of the linearized elasticity system")
      mechtools.elasticity(newmesh,newu)

      # Calculation of the new values of compliance and volume
      print("    Evaluation of the new merit")
      newCp  = mechtools.compliance(newmesh,newu)
      newvol = mechtools.volume(newmesh)
      newmerit = mechtools.merit(newCp,newvol)
    
    # Decision
    # Accept iteration: break and increase slightly the "time step"
    if ( retmmg and ( newmerit < merit + path.TOL*abs(merit) ) or ( k == 2 ) or ( coef < path.MINCOEF ) ) :
      coef = min(path.MAXCOEF,1.1*coef)
      print("    Iteration {} - subiteration {} accepted\n".format(n,k))
      break
    # Reject iteration: go to start of line search with a decreased "time step"
    else :
      print("    Iteration {} - subiteration {} rejected".format(n,k))
      proc = subprocess.Popen(["rm {nmesh}".format(nmesh=newmesh)],shell=True)
      proc.wait()
      coef = max(path.MINCOEF,0.6*coef)
    
###############################################################
####################       END PROGRAM      ###################
###############################################################

print("*************************************************")
print("****************** End of SO Demo ***************")
print("*************************************************")
