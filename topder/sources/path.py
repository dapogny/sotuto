#!/usr/bin/pythonw
# -*-coding:Utf-8 -*

import os
import sys

# Global parameters
REFDIR        = 1       # Reference for Dirichlet B.C
REFDIRG       = 4       # Reference for Dirichlet B.C on the normal component only
REFNEU        = 2       # Reference for Neumann B.C.
REFISO        = 10      # Reference for the boundary edges of the shape
REFINT        = 3       # Reference of the interior domain
REFEXT        = 2       # Reference of the exterior domain

# Parameters of the mesh
MESHSIZ       = 0.02
HMIN          = 0.001
HMAX          = 0.02
HAUSD         = 0.001
HGRAD         = 1.3

# Other parameters
EPS           = 1e-10 # Precision parameter
EPSP          = 1e-20 # Precision parameter for packing
ALPHA         = 0.02 # Parameter for velocity extension - regularization
MAXIT         = 150   # Maximum number of iterations in the shape optimization process
MAXITLS       = 3   # Maximum number of iterations in the line search procedure
MAXCOEF       = 2.0  # Maximum allowed move between two iterations (in # * MESHSIZ)
MINCOEF       = 0.02 # Minimum allowed move between two iterations (in # * MESHSIZ)
TOL           = 0.02  # Tolerance for a slight increase in the merit
TOLTG         = 0.05  # Tolerance for a slight increase in the merit in the use of topological derivatives
AJ            = 1.0   # Weight of objective in null-space optimization algorithm
AG            = 0.1   #  Weight of constraint in null-space optimization algorithm
ITMAXNORMXIJ  = 200
VTARG         = 0.7    # Volume target
VFRACTG       = 0.01   # Fraction of volume removed during one topological derivative iteration

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
FFDESCENTSG    = SCRIPT + "descentSG.edp"
FFDESCENTTG    = SCRIPT + "descentTG.edp"
FFINIMSH       = SCRIPT + "inimsh.edp"
FFINILS        = SCRIPT + "inils.edp"
FFELAS         = SCRIPT + "elasticity.edp"
FFCPLY         = SCRIPT + "compliance.edp"
FFGRADCP       = SCRIPT + "gradCp.edp"
FFTOPGRADCP    = SCRIPT + "topgradCp.edp"
FFVOL          = SCRIPT + "volume.edp"
FFGRADV        = SCRIPT + "gradV.edp"
FFTOPGRADV     = SCRIPT + "topgradV.edp"
FFUPTG         = SCRIPT + "upTG.edp"

# Names of output and exchange files
EXCHFILE = RES + "exch.data"
DEFMMG2D = "DEFAULT.mmg2d"
LOGFILE  = RES + "log.data"
HISTO    = RES + "histo.data"
STEP     = RES + "step"
TMPSOL   = "./res/temp.sol"
TESTMESH = TESTDIR + "test.mesh"
TESTPHI  = TESTDIR + "test.phi.sol"
TESTSOL  = TESTDIR + "test.grad.sol"

# Shortcut for various file types
def step(n,typ) :
  return STEP + "." + str(n) + "." + typ
