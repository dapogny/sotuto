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

# Coefficient for time step (descent direction is scaled with respect to mesh size)
coef = 1.0

# Main loop
# At the beginning of each iteration, are available:
#    - the mesh $\¢alT^n$ of $D$ associated to the current shape $\Omega^n$;
#    - the solution to the linear elasticity equation on $\Omega^n$ (at the nodes of $D$).
#    - The compliance and volume of the shape
for it in range(0,path.MAXIT) :
  curmesh = path.step(it,"mesh")
  newmesh = path.step(it+1,"mesh")
  curphi  = path.step(it,"phi.sol")
  newphi  = path.step(it+1,"phi.sol")
  curu    = path.step(it,"u.sol")
  newu    = path.step(it+1,"u.sol")
  curCpgrad = path.step(it,"CP.grad.sol")
  curtopCpgrad = path.step(it,"CP.gradT.sol")
  curVgrad = path.step(it,"V.grad.sol")
  curtopVgrad = path.step(it,"V.gradT.sol")
  curgrad = path.step(it,"grad.sol")
  curtopgrad = path.step(it,"gradT.sol")
  curCp   = newCp
  curvol  = newvol
  dotopder = 1 if ( it % 5 == 0 and it <= 50 ) else 0 # Equals 1 if topological derivative operation, 0 else
  
  print("***************************************************")
  print("Iteration {}: Compliance {} ; volume {}".format(it,curCp,curvol))
  print("***************************************************")
  
  # Print values in the path.HISTO file
  inout.printHisto(it,curCp,curvol)

  # Change value of tolerance after a certain number of iterations
  if ( it == 100 ) :
    path.TOL = 0.005

  # Generation of a level set function for $\Omega^n$ on $D$
  print("  Creation of a level set function")
  lstools.mshdist(curmesh,curphi)
  
  print("  Computation of a descent direction")
# Calculation of the gradients of compliance and volume
  mechtools.gradCp(curmesh,curu,curCpgrad)
  mechtools.gradV(curmesh,curVgrad)
  
  # Calculation of a descent direction
  mechtools.descentSG(curmesh,curphi,curCp,curCpgrad,curvol,curVgrad,curgrad)

  # Evaluation of the merit of $\Omega^n$
  merit = mechtools.merit(curCp,curvol)
    
  # Modification of the shape using topological gradients
  if ( dotopder ) :
    # Calculation of the topological derivatives of the compliance and volume
    print("  Computation of topological derivatives")
    mechtools.topgradCp(curmesh,curu,curtopCpgrad)
    mechtools.topgradV(curmesh,curtopVgrad)
        
    # Calculation of the topological derivative of the merit functional
    mechtools.descentTG(curmesh,curphi,curCp,curtopCpgrad,curvol,curtopVgrad,curtopgrad)
    
    # Update of the level set function of the shape
    lstools.creaHoles(curmesh,curphi,curtopgrad,path.VFRACTG,newphi)

    # Creation of a mesh associated to the new shape
    print("  Local remeshing")
    retmmg = mshtools.mmg2d(curmesh,1,newphi,path.HMIN,path.HMAX,path.HAUSD,path.HGRAD,1,newmesh)
    
    if ( retmmg ) :
      # Resolution of the state equation on the new shape
      print("  Resolution of the linearized elasticity system")
      mechtools.elasticity(newmesh,newu)

      # Calculation of the new values of compliance and volume
      print("  Evaluation of the new merit")
      newCp  = mechtools.compliance(newmesh,newu)
      newvol = mechtools.volume(newmesh)
      newmerit = mechtools.merit(newCp,newvol)
    else :
      exit() 
      
    # Decision
    # Accept iteration
      if ( retmmg and ( newmerit < merit + path.TOLTG*abs(merit) ) ) :
        print("  Iteration {} (topological derivative) accepted\n".format(it))
      # Reject iteration
      else :
        print("  Iteration {} (topological derivative) rejected".format(k))
        proc = subprocess.Popen(["cp {omesh} {nmesh}".format(omesh=curmesh,nmesh=newmesh)],shell=True)
        proc.wait()
  
  # Modification of the shape via the boundary variation strategy
  else :
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
        print("    Iteration {} - subiteration {} accepted\n".format(it,k))
        break
      # Reject iteration: go to start of line search with a decreased "time step"
      else :
        print("    Iteration {} - subiteration {} rejected".format(it,k))
        proc = subprocess.Popen(["rm {nmesh}".format(nmesh=newmesh)],shell=True)
        proc.wait()
        coef = max(path.MINCOEF,0.6*coef)
    
###############################################################
####################       END PROGRAM      ###################
###############################################################

print("*************************************************")
print("****************** End of SO Demo ***************")
print("*************************************************")
