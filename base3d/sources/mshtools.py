#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import path
import subprocess
import os
import inout
import sys
import numpy as np

##############################################################################################################
######   Call to mmg3d                                                                                  ######
######   Inputs:   mesh (string) name of the mesh                                                       ######
######             ls   (int)  0 for standard remeshing mode, 1 for L.S. discretization mode            ######
######             phi  (string) name of the L.S. function                                              ######
######             hmin (real) minimum desired size of an element in the mesh                           ######
######             hmax (real) maximum desired size of an element in the mesh                           ######
######             hausd (real) geometric approximation parameter                                       ######
######             hgrad (real) mesh gradation parameter                                                ######
######             nr (int) 0 if identification of sharp angles, 1 if no identification                 ######
######   Output:   out (string) name of the output mesh                                                 ######
######   Return: 1 if remeshing successful, 0 otherwise
##############################################################################################################

def mmg3d(mesh,ls,phi,hmin,hmax,hausd,hgrad,nr,out) :
  
  log = open(path.LOGFILE,'a')
  
  if  ls :
    if nr :
      proc = subprocess.Popen(["{mmg} {mesh} -ls -sol {sol} -hmin {hmin} -hmax {hmax} -hausd {hausd} -hgrad {hgrad} -nr {res} -rmc".format(mmg=path.MMG3D,mesh=mesh,sol=phi,hmin=hmin,hmax=hmax,hausd=hausd,hgrad=hgrad,res=out)],shell=True,stdout=log)
      proc.wait()
    else :
      proc = subprocess.Popen(["{mmg} {mesh} -ls -sol {sol} -hmin {hmin} -hmax {hmax} -hausd {hausd} -hgrad {hgrad} {res} -rmc".format(mmg=path.MMG3D,mesh=mesh,sol=phi,hmin=hmin,hmax=hmax,hausd=hausd,hgrad=hgrad,res=out)],shell=True,stdout=log)
      proc.wait()
  else :
    if nr :
      proc = subprocess.Popen(["{mmg} {mesh} -hmin {hmin} -hmax {hmax} -hausd {hausd} -hgrad {hgrad} -nr {res} -rmc".format(mmg=path.MMG3D,mesh=mesh,sol=phi,hmin=hmin,hmax=hmax,hausd=hausd,hgrad=hgrad,res=out)],shell=True,stdout=log)
      proc.wait()
    else :
      proc = subprocess.Popen(["{mmg} {mesh} -hmin {hmin} -hmax {hmax} -hausd {hausd} -hgrad {hgrad} {res} -rmc".format(mmg=path.MMG3D,mesh=mesh,sol=phi,hmin=hmin,hmax=hmax,hausd=hausd,hgrad=hgrad,res=out)],shell=True,stdout=log)
      proc.wait()
  
  log.close()
  if ( proc.returncode != 0 ) :
    return 0
  else :
    return 1 

##############################################################################################################
##############################################################################################################
