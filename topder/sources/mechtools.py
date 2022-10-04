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
#######       inputs: mesh (string): mesh of the shape                        #######
#######               u (string): output elastic displacement                 #######
#####################################################################################

def elasticity(mesh,u) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
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

#####################################################################################
#######   Calculate shape gradient of the compliance functional               #######
#######       input:  mesh (string): mesh of the shape                        #######
#######               disp (string): solution of the elasticity system        #######
#######       output: grad (string): shape gradient of compliance             #######
#####################################################################################

def gradCp(mesh,disp,grad) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="DispName",attval=disp)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=grad)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {gradCp} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,gradCp=path.FFGRADCP)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in calculation of gradient of compliance; abort.")
    exit()
    
#####################################################################################
#####################################################################################

#####################################################################################
#######   Calculate topological derivative of the compliance functional       #######
#######       input:  mesh (string): mesh of the shape                        #######
#######               disp (string): solution of the elasticity system        #######
#######       output: grad (string): shape gradient of compliance             #######
#####################################################################################

def topgradCp(mesh,disp,grad) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="DispName",attval=disp)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=grad)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {gradCp} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,gradCp=path.FFTOPGRADCP)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in calculation of topological derivative of compliance; abort.")
    exit()
    
#####################################################################################
#####################################################################################



#####################################################################################
#######   Calculate shape gradient of the volume function                     #######
#######       input:  mesh (string): mesh of the shape                        #######
#######       output: grad (string): shape gradient of volume                 #######
#####################################################################################

def gradV(mesh,grad) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=grad)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {gradV} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,gradV=path.FFGRADV)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in calculation of gradient of volume; abort.")
    exit()

#####################################################################################
#####################################################################################

#####################################################################################
#######   Calculate topological derivative of the volume function             #######
#######       input:  mesh (string): mesh of the shape                        #######
#######       output: grad (string): shape gradient of volume                 #######
#####################################################################################

def topgradV(mesh,grad) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=grad)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {gradV} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,gradV=path.FFTOPGRADV)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in calculation of topological derivative of volume; abort.")
    exit()

#####################################################################################
#####################################################################################

#######################################################################################
#####             Calculation of the (normalized) descent direction               #####
#####                     by the boundary variation method                        #####
#####      inputs :   mesh: (string for) mesh ;                                   #####
#####                 phi: (string for) ls function                               #####
#####                 gCp: (string for) gradient of Compliance                    #####
#####                 Cp: (real) value of Compliance                              #####
#####                 gV: (string for) gradient of Volume                         #####
#####                 vol: (real) value of volume                                 #####
#####      Output:    g: (string for) total gradient                              #####
#######################################################################################

def descentSG(mesh,phi,Cp,gCp,vol,gV,g) :

  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=phi)
  inout.setAtt(file=path.EXCHFILE,attname="GradCpName",attval=gCp)
  inout.setAtt(file=path.EXCHFILE,attname="Compliance",attval=Cp)
  inout.setAtt(file=path.EXCHFILE,attname="GradVolName",attval=gV)
  inout.setAtt(file=path.EXCHFILE,attname="Volume",attval=vol)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=g)
      
  # Velocity extension - regularization via FreeFem
  proc = subprocess.Popen(["{FreeFem} {ffdescent} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,ffdescent=path.FFDESCENTSG)],shell=True)
  proc.wait()
    
  if ( proc.returncode != 0 ) :
    print("Error in calculation of descent direction; abort.")
    exit()

#######################################################################################
#######################################################################################

#######################################################################################
#####      Calculation of the topological derivative of the merit function        #####
#####      inputs :   mesh: (string for) mesh ;                                   #####
#####                 phi: (string for) ls function                               #####
#####                 gCp: (string for) topological derivative of Compliance      #####
#####                 Cp: (real) value of Compliance                              #####
#####                 gV: (string for) topological derivative of Volume           #####
#####                 vol: (real) value of volume                                 #####
#####      Output:    g: (string for) total gradient                              #####
#######################################################################################

def descentTG(mesh,phi,Cp,gCp,vol,gV,g) :

  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=phi)
  inout.setAtt(file=path.EXCHFILE,attname="GradCpName",attval=gCp)
  inout.setAtt(file=path.EXCHFILE,attname="Compliance",attval=Cp)
  inout.setAtt(file=path.EXCHFILE,attname="GradVolName",attval=gV)
  inout.setAtt(file=path.EXCHFILE,attname="Volume",attval=vol)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=g)
      
  # Velocity extension - regularization via FreeFem
  proc = subprocess.Popen(["{FreeFem} {ffdescent} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,ffdescent=path.FFDESCENTTG)],shell=True)
  proc.wait()
    
  if ( proc.returncode != 0 ) :
    print("Error in calculation of topological derivative; abort.")
    exit()

#######################################################################################
#######################################################################################

#######################################################################################
#####                         Evaluation of the merit function                    #####
#####                     in the Null Space optimization algorithm                #####
#####      inputs : Cp: (real) value of compliance                                #####
#####               vol: (real) value of the volume                               #####
#####      output : merit: (real) value of the merit of shape                    #####
#######################################################################################

def merit(Cp,vol) :

  # Read parameters in the exchange file
  [alphaJ] = inout.getrAtt(file=path.EXCHFILE,attname="alphaJ")
  [alphaG] = inout.getrAtt(file=path.EXCHFILE,attname="alphaG")
  [ell] = inout.getrAtt(file=path.EXCHFILE,attname="Lagrange")
  [m] = inout.getrAtt(file=path.EXCHFILE,attname="Penalty")
  [vtarg] = inout.getrAtt(file=path.EXCHFILE,attname="VolumeTarget")

  merit = alphaJ*(Cp - ell*(vol-vtarg)) + 0.5*alphaG/m*(vol-vtarg)**2

  return merit

#######################################################################################
#######################################################################################
