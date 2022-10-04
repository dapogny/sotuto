#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import os
import sys

# Global parameters
REFDIR        = 1       # Reference for Dirichlet B.C
REFNEU        = 2       # Reference for Neumann B.C.
REFISO        = 10      # Reference for the boundary edges of the shape
REFINT        = 3       # Reference of the interior domain
REFEXT        = 2       # Reference of the exterior domain

# Parameters of the mesh
MESHSIZ       = 0.05
HMIN          = 0.04
HMAX          = 0.07
HAUSD         = 0.005
HGRAD         = 1.4

# Other parameters
EPS           = 1e-10 # Precision parameter
EPSP          = 1e-20 # Precision parameter for packing
ALPHA         = 0.07 # Parameter for velocity extension - regularization
ALPHALS       = 0.01 # Parameter for regularization of LS function
MAXIT         = 200   # Maximum number of iterations in the shape optimization process
MAXITLS       = 3   # Maximum number of iterations in the line search procedure
MAXCOEF       = 1.0  # Maximum allowed move between two iterations (in # * MESHSIZ)
MINCOEF       = 0.02 # Minimum allowed move between two iterations (in # * MESHSIZ)
TOL           = 0.01  # Tolerance for a slight increase in the merit
AJ            = 1.0   # Weight of objective in null-space optimization algorithm
AG            = 0.4  #  Weight of constraint in null-space optimization algorithm
ITMAXNORMXIJ  = 200
VTARG         = 0.45    # Volume target

# Paths to folders
RES     = "./res/"       # Directory for results
VID     = "./vid/"       # Directory for outputting truncated meshes
TESTDIR = RES + "test/"  # Directory for test of libraries
SCRIPT  = "./sources/"   # Directory for sources

# Call for the executables of external codes
FREEFEM = "FreeFem++ -nw"
MSHDIST = "mshdist"
ADVECT  = "/Users/dapogny/Advection/build/advect"
MMG3D   = "/Users/dapogny/mmg/build/bin/mmg3d_O3"

# Path to FreeFem scripts
FFTEST         = SCRIPT + "testFF.edp"
FFREGLS        = SCRIPT + "regls.edp"
FFDESCENT      = SCRIPT + "descent.edp"
FFINIMSH       = SCRIPT + "inimsh.edp"
FFINILS        = SCRIPT + "inils.edp"
FFELAS         = SCRIPT + "elasticity.edp"
FFCPLY         = SCRIPT + "compliance.edp"
FFGRADCP       = SCRIPT + "gradCp.edp"
FFVOL          = SCRIPT + "volume.edp"
FFGRADV        = SCRIPT + "gradV.edp"
FFTRUNC        = SCRIPT + "truncvid.edp"


# Names of output and exchange files
DEFMMG       = "./DEFAULT.mmg3d"
EXCHFILE     = RES + "exch.data"
EXCHFILEVID  = VID + "exch.data"
LOGFILE      = RES + "log.data"
HISTO        = RES + "histo.data"
STEP         = RES + "step"
TMPSOL       = "./res/temp.sol"
TESTMESH     = TESTDIR + "test.mesh"
TESTPHI      = TESTDIR + "test.phi.sol"
TESTSOL      = TESTDIR + "test.grad.sol"

# Shortcut for various file types
def step(n,typ) :
  return STEP + "." + str(n) + "." + typ
