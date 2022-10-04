#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import sys
import subprocess
import math
import inout
import path


#####################################################################################################
#######      Advect the L.S. function in ssol via the velocity svel; result in ssolout       ########
#######        Inputs: mesh: (string for) mesh;  phi: (string for) initial LS function      ########
#######                vel: (string for) velocity field; step: (real) final time;           ########
#######                           newphi: (string for) output L.S. function                 ########
#####################################################################################################

def advect(mesh,phi,vel,step,newphi) :

  log = open(path.LOGFILE,'a')

  # Advection by calling advect
  proc = subprocess.Popen(["{adv} {msh} -s {vit} -c {chi} -dt {dt} -o {out} -nocfl".format(adv=path.ADVECT,msh=mesh,vit=vel,chi=phi,dt=step,out=newphi)],shell=True,stdout=log)
  proc.wait()
  
  log.close()

#####################################################################################################
#####################################################################################################

#####################################################################################################
#######    Create holes inside the level set function phi by removing the fraction volfrac   ########
#######               of material where grad is most negative                                ########
#######        Inputs: mesh: (string for) mesh;                                              ########
#######                phi: (string for) initial LS function                                 ########
#######                grad: (string for) gradient;                                          ########
#######                volfrac: (real) fraction of the volume enclosed by phi to remove      ########
#######        Outputs  newphi: (string for) output L.S. function                            ########
#####################################################################################################

def creaHoles(mesh,phi,grad,volfrac,newphi) :

  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=phi)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=grad)
  inout.setAtt(file=path.EXCHFILE,attname="VolFracTG",attval=volfrac)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=newphi)

  # Velocity extension - regularization via FreeFem
  proc = subprocess.Popen(["{FreeFem} {uptg} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,uptg=path.FFUPTG)],shell=True)
  proc.wait()
    
  if ( proc.returncode != 0 ) :
    print("Error in calculation of topological derivative; abort.")
    exit()

#####################################################################################################
#####################################################################################################

##################################################################################################
###########       Create the signed distance function to the subdomain               #############
###########                  with reference path.REFINT                              #############
###########        mesh = mesh (string) ; phi = output distance (string)             #############
##################################################################################################

def mshdist(mesh,phi) :
  
  log = open(path.LOGFILE,'a')

  # Distancing with mshdist
  proc = subprocess.Popen(["{mshdist} {msh} -dom -fmm".format(mshdist=path.MSHDIST,msh=mesh)],shell=True,stdout=log)
  proc.wait()
  
  # Move output file to the desired location
  oldphi = mesh.replace('.mesh','') + ".sol"
  proc = subprocess.Popen(["mv {old} {new}".format(old=oldphi,new=phi)],shell=True,stdout=log)
  proc.wait()

  log.close()

##################################################################################################
##################################################################################################
