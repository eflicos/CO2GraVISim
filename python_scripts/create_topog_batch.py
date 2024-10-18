
# Import packages
import numpy as np
import sys
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path 

#Import functions from batch_run_generation to archive old batch and create folders
sys.path.append("./python_scripts")
import generate_topography as gtop

# Edit these as appropriate for different runs
topdir = './batch_run_test/' # top level directory for batch runs
commonfiles = 'Common_files/' # location of common files shared across batches - this has all param defaults, then copied into all dirs
theta_range_deg = 0.1 # in degrees - translated to radians below
ampl_range = [0.01,0.02]

# Do not edit these
theta_range = np.array(theta_range_deg) * np.pi/180
parameterloc = topdir+commonfiles+"grid_parameters.txt" #location of file containing grid parameters
topographyloc = topdir+commonfiles+"ceil_topo.txt" #location of file containing ceiling topography
baseloc = topdir+commonfiles+"base_topo.txt" #file containing base topography to ensure gap
injectionloc = topdir+commonfiles+"injection_locations.txt" #file containing injection locations

#load in data about grid point locations
parameters = np.loadtxt(parameterloc,skiprows=1)
nx = int(parameters[0])
ny = int(parameters[1])
dx = parameters[2]
dy = parameters[3]
# assumes only one injection location
injection = np.loadtxt(injectionloc,skiprows=3) # rows 1,2 are text. row 3 says how many injection locations
Q_x = int(injection[0])
Q_y = int(injection[1])

# Create array with all combos of theta and amplitude
theta_ampl_range = np.stack(np.meshgrid(theta_range,ampl_range)).T.reshape(-1,2)
nvar = len(theta_ampl_range)

top_wl_x = 1
top_ampl_y = 0
top_wl_y = 0

# #x and y axis values
# x = np.arange(-(nx-1)/2.0,(nx-1)/2.0+1.0)*dx
# y = np.arange(-(ny-1)/2.0,(ny-1)/2.0+1.0)*dy

#plot variants on topography
# xplot, yplot = np.meshgrid(x,y)
# create_folders(topdir,nvar)

for i in range(nvar):
    theta = theta_ampl_range[i,0]
    top_ampl_x = theta_ampl_range[i,1]
    
    # Generate topography
    top = gtop.sinusoidal(nx,ny,dx,dy,Q_x,Q_y,theta,top_ampl_x,top_wl_x,top_ampl_y,top_wl_y)
    
    # Create input and output directories
    this_dir = topdir+'run_'+str(i+1)+'/'
    Path(this_dir+'Input/').mkdir(parents=True, exist_ok=True)
    Path(this_dir+'Output/').mkdir(parents=True, exist_ok=True)
    
    # Copy everything from commonfiles into this_dir
    copy_tree(topdir+commonfiles,this_dir+'Input/')
    # Save topog
    np.savetxt(this_dir+'/Input/ceil_topo.txt',top)
    # Save theta, ampl pair
    np.savetxt(this_dir+'/Input/theta_ampl_x.txt',theta_ampl_range[i])
    
    # #No longer copying across common files
    # shutil.copy(topdir+commonfiles+'base_topo.txt',topdir+'run_'+str(i+1)+'/Input/')
    # shutil.copy(topdir+commonfiles+'boundary_conditions.txt',topdir+'run_'+str(i+1)+'/Input/')
    # shutil.copy(topdir+commonfiles+'flow_parameters.txt',topdir+'run_'+str(i+1)+'/Input/')
    # shutil.copy(topdir+commonfiles+'grid_parameters.txt',topdir+'run_'+str(i+1)+'/Input/')
    # shutil.copy(topdir+commonfiles+'injection_locations.txt',topdir+'run_'+str(i+1)+'/Input/')
    # shutil.copy(topdir+commonfiles+'injection_profile.txt',topdir+'run_'+str(i+1)+'/Input/')
    # shutil.copy(topdir+commonfiles+'perm_h.txt',topdir+'run_'+str(i+1)+'/Input/')
    # shutil.copy(topdir+commonfiles+'Permeability.txt',topdir+'run_'+str(i+1)+'/Input/')
    # shutil.copy(topdir+commonfiles+'poro_h.txt',topdir+'run_'+str(i+1)+'/Input/')
    # shutil.copy(topdir+commonfiles+'Porosity.txt',topdir+'run_'+str(i+1)+'/Input/')
    # shutil.copy(topdir+commonfiles+'target_plot_times.txt',topdir+'run_'+str(i+1)+'/Input/')
