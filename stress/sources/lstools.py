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

##################################################################################################
#############             Post-treatment of an input LS function                     #############
#############             inputs:  mesh   (string): mesh of the shape                #############
#############                      phi    (string): level set function               #############
#############             output: phiout (string): regularized level set function    #############
##################################################################################################

def postls(mesh,phi,phiout) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=phi)
  inout.setAtt(file=path.EXCHFILE,attname="SolName",attval=phiout)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {postls} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,regls=path.FFPOSTLS)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in regularization of level set function; abort.")
    exit()
    
##################################################################################################
##################################################################################################
