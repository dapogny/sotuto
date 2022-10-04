#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import path
import subprocess
import os
import inout
import sys
import mshtools
import lstools

###########################################################################
#######           Create initial mesh and Ls Function               #######
#######             Input: mesh (string) path to mesh               #######
###########################################################################
def iniGeom(mesh) :
  
  # Fill in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=path.TMPSOL)

  # Call to FreeFem for creating the background mesh
  log = open(path.LOGFILE,'a')
  proc = subprocess.Popen(["{FreeFem} {file} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,file=path.FFINIMSH)],shell=True,stdout=log)
  proc.wait()
  log.close()
  
  if ( proc.returncode != 0 ) :
    print("Error in creation of initial mesh; abort.")
    exit()

  # Call to mmg2d for remeshing the background mesh
  mshtools.mmg2d(mesh,0,None,path.HMIN,path.HMAX,path.HAUSD,path.HGRAD,0,mesh)
  
  # Call to FreeFem for creating the initial level set function
  log = open(path.LOGFILE,'a')
  proc = subprocess.Popen(["{FreeFem} {file} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,file=path.FFINILS)],shell=True,stdout=log)
  proc.wait()
  log.close()
  
  if ( proc.returncode != 0 ) :
    print("Error in creation of initial level set function; abort.")
    exit()
  
  # Call to mmg2d for discretizing the level set function into the mesh
  mshtools.mmg2d(mesh,1,path.TMPSOL,path.HMIN,path.HMAX,path.HAUSD,path.HGRAD,1,mesh)
