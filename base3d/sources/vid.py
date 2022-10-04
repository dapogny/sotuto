#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import subprocess
import os
import sys
import inout
import path

# Create and clear ./vid folder for results depending on the situation
proc = subprocess.Popen(["mkdir -p {folder}".format(folder=path.VID)],shell=True)
proc.wait()
proc = subprocess.Popen(["rm -rf {folder}*".format(folder=path.VID)],shell=True)
proc.wait()

# Create exchange file
ff = open(path.EXCHFILEVID,'w')
ff.close()

# Truncate result meshes
for n in range(0,path.MAXIT+1) :
  mesh  = path.step(n,"mesh")
  mesho = path.VID + "step."+str(n)+".mesh"
  
  inout.setAtt(file=path.EXCHFILEVID,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILEVID,attname="MeshOutName",attval=mesho)

  proc = subprocess.Popen(["{ff} {fftrunc}".format(ff=path.FREEFEM,fftrunc=path.FFTRUNC)],shell=True)
  proc.wait()

