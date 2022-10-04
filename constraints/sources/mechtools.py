#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import subprocess
import inout
import os
import path
import sys
import numpy as np

#####################################################################################
#######   Numerical solver for elasticity                                     #######
#######       inputs: mesh   (string): mesh of the shape                      #######
#######               refneu (int): ref of the loaded region                  #######
#######               gx (real): horizontal component of load                 #######
#######               gy (real): vertical component of load                   #######
#######               u (string): output elastic displacement                 #######
#####################################################################################

def elasticity(mesh,refneu,gx,gy,u) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="Neumann",attval=refneu)
  inout.setAtt(file=path.EXCHFILE,attname="GX",attval=gx)
  inout.setAtt(file=path.EXCHFILE,attname="GY",attval=gy)
  inout.setAtt(file=path.EXCHFILE,attname="DispName",attval=u)
  
  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {elasticity} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,elasticity=path.FFELAS)],shell=True)
  proc.wait()

  if ( proc.returncode != 0 ) :
    print("Error in numerical solver; abort.")
    exit()
    
#####################################################################################
#####################################################################################

#####################################################################################
#######   Calculate elastic compliance                                        #######
#######       inputs: mesh (string): mesh of the shape                        #######
#######               u (string): output elastic displacement                 #######
#####################################################################################

def compliance(mesh,u) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="DispName",attval=u)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {compliance} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,compliance=path.FFCPLY)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in compliance calculation; abort.")
    exit()
  
  [cply] = inout.getrAtt(file=path.EXCHFILE,attname="Compliance")
  
  return cply

#####################################################################################
#####################################################################################

#####################################################################################
#######   Calculate volume                                                    #######
#######       input: mesh (string): mesh of the shape                         #######
#####################################################################################

def volume(mesh) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {volume} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,volume=path.FFVOL)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in compliance calculation; abort.")
    exit()
  
  [vol] = inout.getrAtt(file=path.EXCHFILE,attname="Volume")
  
  return vol

#####################################################################################
#####################################################################################

########################################################################################################
#######          Calculate shape sensitivity and gradient of the compliance functional           #######
#######       input:  mesh (string): mesh of the shape                                           #######
#######               disp (string): solution of the elasticity system                           #######
#######      outpus: diff (string): integrand of shape derivative of compliance                  #######
#######              grad (string): shape gradient of compliance                                 #######
########################################################################################################

def gradCp(mesh,disp,diff,grad) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="DispName",attval=disp)
  inout.setAtt(file=path.EXCHFILE,attname="DiffName",attval=diff)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=grad)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {gradCp} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,gradCp=path.FFGRADCP)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in calculation of gradient of compliance; abort.")
    exit()
    
########################################################################################################
########################################################################################################

#################################################################################################
#######   Calculate shape sensitivity and gradient of the volume function                 #######
#######       input:  mesh (string): mesh of the shape                                    #######
#######      outputs: diff (string): integrand of shape derivative of volume              #######
#######               grad (string): shape gradient of volume                             #######
#################################################################################################

def gradV(mesh,diff,grad) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="DiffName",attval=diff)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=grad)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {gradV} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,gradV=path.FFGRADV)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in calculation of gradient of volume; abort.")
    exit()

#####################################################################################
#####################################################################################
