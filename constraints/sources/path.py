#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import os
import sys

# Global parameters
REFDIR        = 1       # Reference for Dirichlet B.C
REFISO        = 10      # Reference for the boundary edges of the shape
REFINT        = 3       # Reference of the interior domain
REFEXT        = 2       # Reference of the exterior domain
NC            = 7                                        # Number of contraints (=load cases)
GX            = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]            # Horizontal components of loads on ref REFNEU + i
GY            = [-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]     # Vertical components of loads
REFNEU        = 11      # Load case i=0,...,NC-1 corresponds to ref REFNEU + i

# Parameters of the mesh
MESHSIZ       = 0.1
HMIN          = 0.02
HMAX          = 0.05
HAUSD         = 0.005
HGRAD         = 1.3

# Other parameters
EPS           = 1e-10 # Precision parameter
EPSP          = 1e-20 # Precision parameter for packing
ALPHA         = 0.1 # Parameter for velocity extension - regularization
MAXIT         = 150   # Maximum number of iterations in the shape optimization process
MAXITLS       = 3   # Maximum number of iterations in the line search procedure
MAXCOEF       = 2.0  # Maximum allowed move between two iterations (in # * MESHSIZ)
MINCOEF       = 0.02 # Minimum allowed move between two iterations (in # * MESHSIZ)
TOL           = 0.02  # Tolerance for a slight increase in the merit
AJ            = 1.0   # Weight of objective in null-space optimization algorithm
AG            = 0.1   #  Weight of constraint in null-space optimization algorithm
CTARGPC       = 0.9  # Compliance threshold = CTARGPC * max(Compliance(\Omega,g_i))
CTARG         = 0.0  # Threshold for compliance, to be calculated

# Paths to folders
RES     = "./res/"       # Directory for results
TESTDIR = RES + "test/"  # Directory for test of libraries
SCRIPT  = "./sources/"   # Directory for sources

# Call for the executables of external codes
FREEFEM = "FreeFem++ -nw"
MSHDIST = "mshdist"
ADVECT  = "/Users/dapogny/Advection/build/advect"
MMG2D   = "/Users/dapogny/mmg/build/bin/mmg2d_O3"

# Path to FreeFem scripts
FFTEST         = SCRIPT + "testFF.edp"
FFINIMSH       = SCRIPT + "inimsh.edp"
FFINILS        = SCRIPT + "inils.edp"
FFELAS         = SCRIPT + "elasticity.edp"
FFCPLY         = SCRIPT + "compliance.edp"
FFGRADCP       = SCRIPT + "gradCp.edp"
FFVOL          = SCRIPT + "volume.edp"
FFGRADV        = SCRIPT + "gradV.edp"
FFNORVEC       = SCRIPT + "norvec.edp"

# Names of output and exchange files
EXCHFILE = RES + "exch.data"
DEFMMG2D = "DEFAULT.mmg2d"
LOGFILE  = RES + "log.data"
HISTO    = RES + "histo.data"
STEP     = RES + "step"
TMPSOL   = RES + "temp.sol"
TESTMESH = TESTDIR + "test.mesh"
TESTPHI  = TESTDIR + "test.phi.sol"
TESTSOL  = TESTDIR + "test.grad.sol"

# Shortcut for various file types
def step(n,typ) :
  return STEP + "." + str(n) + "." + typ
