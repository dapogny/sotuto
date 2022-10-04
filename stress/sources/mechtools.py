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
#######   Computation of the adjoint state for the stress functional          #######
#######       inputs: mesh (string): mesh of the shape                        #######
#######               u (string): input elastic displacement                 #######
#######               p (string): output adjoint state                       #######
#####################################################################################

def adjoint(mesh,u,p) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="DispName",attval=u)
  inout.setAtt(file=path.EXCHFILE,attname="AdjName",attval=p)
  
  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {adjoint} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,adjoint=path.FFADJ)],shell=True)
  proc.wait()

  if ( proc.returncode != 0 ) :
    print("Error in numerical solver for adjoint equation; abort.")
    exit()
    
#####################################################################################
#####################################################################################

#####################################################################################
#######   Calculate elastic stress                                            #######
#######       inputs: mesh (string): mesh of the shape                        #######
#######               u (string): output elastic displacement                 #######
#####################################################################################

def stress(mesh,u) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="DispName",attval=u)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {stress} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,stress=path.FFSTRESS)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in compliance calculation; abort.")
    exit()
  
  [S] = inout.getrAtt(file=path.EXCHFILE,attname="Stress")
  
  return S

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
#######   Calculate gradient of the stress functional                         #######
#######       input:  mesh (string): mesh of the shape                        #######
#######               disp (string): solution of the elasticity system        #######
#######               adj (string):  solution of the adjoint system           #######
#######       output: grad (string): shape gradient of stress                 #######
#####################################################################################

def gradS(mesh,disp,adj,grad) :
  
  # Set information in exchange file
  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="DispName",attval=disp)
  inout.setAtt(file=path.EXCHFILE,attname="AdjName",attval=adj)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=grad)

  # Call to FreeFem
  proc = subprocess.Popen(["{FreeFem} {gradS} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,gradS=path.FFGRADS)],shell=True)
  proc.wait()
  
  if ( proc.returncode != 0 ) :
    print("Error in calculation of gradient of stress; abort.")
    exit()
    
#####################################################################################
#####################################################################################

#####################################################################################
#######   Calculate gradient of the volume function                           #######
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

#######################################################################################
#####             Calculation of the (normalized) descent direction               #####
#####      inputs :   mesh: (string for) mesh ;                                   #####
#####                 phi: (string for) ls function                               #####
#####                 gS: (string for) gradient of stress                         #####
#####                 S: (real) value of stress                               #####
#####                 gV: (string for) gradient of Volume                         #####
#####                 vol: (real) value of volume                                 #####
#####      Output:    g: (string for) total gradient                              #####
#######################################################################################

def descent(mesh,phi,S,gS,vol,gV,g) :

  inout.setAtt(file=path.EXCHFILE,attname="MeshName",attval=mesh)
  inout.setAtt(file=path.EXCHFILE,attname="PhiName",attval=phi)
  inout.setAtt(file=path.EXCHFILE,attname="GradSName",attval=gS)
  inout.setAtt(file=path.EXCHFILE,attname="Stress",attval=S)
  inout.setAtt(file=path.EXCHFILE,attname="GradVolName",attval=gV)
  inout.setAtt(file=path.EXCHFILE,attname="Volume",attval=vol)
  inout.setAtt(file=path.EXCHFILE,attname="GradName",attval=g)
      
  # Velocity extension - regularization via FreeFem
  proc = subprocess.Popen(["{FreeFem} {ffdescent} > /dev/null 2>&1".format(FreeFem=path.FREEFEM,ffdescent=path.FFDESCENT)],shell=True)
  proc.wait()
    
  if ( proc.returncode != 0 ) :
    print("Error in calculation of descent direction; abort.")
    exit()

#######################################################################################
#######################################################################################

#######################################################################################
#####                         Evaluation of the merit function                    #####
#####                     in the Null Space optimization algorithm                #####
#####      inputs : S: (real) value of stress                                     #####
#####               vol: (real) value of the volume                               #####
#####      output : merit: (real) value of the merit of shape                     #####
#######################################################################################

def merit(S,vol) :

  # Read parameters in the exchange file
  [alphaJ] = inout.getrAtt(file=path.EXCHFILE,attname="alphaJ")
  [alphaG] = inout.getrAtt(file=path.EXCHFILE,attname="alphaG")
  [ell] = inout.getrAtt(file=path.EXCHFILE,attname="Lagrange")
  [m] = inout.getrAtt(file=path.EXCHFILE,attname="Penalty")
  [vtarg] = inout.getrAtt(file=path.EXCHFILE,attname="VolumeTarget")

  merit = alphaJ*(S - ell*(vol-vtarg)) + 0.5*alphaG/m*(vol-vtarg)**2

  return merit

#######################################################################################
#######################################################################################
