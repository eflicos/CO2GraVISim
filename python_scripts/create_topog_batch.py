
# Import packages
import numpy as np
import sys
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path 

#Import functions from batch_run_generation to archive old batch and create folders
sys.path.append("./python_scripts")
import generate_topography as gtop
import batch_run_generation as brg

# Edit these as appropriate for different runs
top_dir = './test/' # top level directory for batch runs
common_files_dir = 'Input/' # location of common files shared across batches - this has all param defaults, then copied into all dirs
archive_boo = False
# Variables to span
theta_range_deg = 2 # in degrees - translated to radians below
ampl_range = [0.01,0.02]
wavelength_x_range = [1]
wavelength_ratio_range = [0.1,1,10] # l = wl_x/wl_y

# Grid size
pts_per_wl = 16
nx = 500
ny = 500
# Lx_min = 200 # if wl_ratio > 1
# Lx_max = 500 # if wl_ratio < 1
# Ly_min = 100 # if wl_ratio < 1
# Ly_max = 500 # if wl_ratio > 1
inj_dist_x = 5 # how far inj is from edge of domain in x

# Do not edit these
theta_range = np.array(theta_range_deg) * np.pi/180
# parameterloc = topdir+common_files_dir+"grid_parameters.txt" #location of file containing grid parameters
# topographyloc = topdir+common_files_dir+"ceil_topo.txt" #location of file containing ceiling topography
# baseloc = topdir+common_files_dir+"base_topo.txt" #file containing base topography to ensure gap
# injectionloc = topdir+common_files_dir+"injection_locations.txt" #file containing injection locations

# #load in data about grid point locations
# parameters = np.loadtxt(parameterloc,skiprows=1)
# nx = int(parameters[0])
# ny = int(parameters[1])
# dx = parameters[2]
# dy = parameters[3]
# # assumes only one injection location
# injection = np.loadtxt(injectionloc,skiprows=3) # rows 1,2 are text. row 3 says how many injection locations
# Q_x = int(injection[0])
# Q_y = int(injection[1])

# Create array with all combos of theta and amplitude
# theta, amp, wl_x, wl_ratio
param_range = np.stack(np.meshgrid(theta_range,ampl_range,wavelength_x_range,wavelength_ratio_range)).T.reshape(-1,4)
num_runs = len(param_range)

# Create all the folders
brg.create_folders(top_dir,num_runs,archive_boo)

for i in range(num_runs):
    # Set dirs
    this_dir = top_dir+'run_'+str(i+1)+'/'
    input_dir = this_dir + 'Input/'
    # Copy across common files
    brg.copy_common_files(input_dir, common_files_dir)
    
    # Read in from param_range
    theta = param_range[i,0]
    top_ampl_x = param_range[i,1]
    top_ampl_y = top_ampl_x
    top_wl_x = param_range[i,2]
    top_wl_ratio = param_range[i,3]
    top_wl_y = top_wl_x/top_wl_ratio
    
    # Use wl to set grid spacing
    dx = top_wl_x/pts_per_wl
    dy = top_wl_y/pts_per_wl
    
    # # Choose grid size based on wl_ratio
    # if top_wl_ratio>=1:
        # # Then flow cross-slope more than upslope
        # Lx = Lx_min
        # Ly = Ly_max
    # else:
        # # Then flow upslope more than cross-slope
        # Lx = Lx_max
        # Ly = Ly_min
    
    # nx = int(Lx//dx)
    # ny = int(Ly//dy)
    
    # Set inj location accordingly
    Q_x = int(inj_dist_x//dx)
    Q_y = ny//2 # Central in y
        
    # Generate topography, permeability and porosity
    top,base = gtop.sinusoidal(nx,ny,dx,dy,Q_x,Q_y,theta,top_ampl_x,top_wl_x,top_ampl_y,top_wl_y)
    perm = np.ones((nx,ny))
    poro = np.ones((nx,ny))
        
    # Create input and output directories
    # this_dir = top_dir+'run_'+str(i+1)+'/'
    # Path(this_dir+'Input/').mkdir(parents=True, exist_ok=True)
    # Path(this_dir+'Output/Current_Pressure/').mkdir(parents=True, exist_ok=True)
    # Path(this_dir+'Output/Current_Thickness/').mkdir(parents=True, exist_ok=True)
    # Path(this_dir+'Output/Other/').mkdir(parents=True, exist_ok=True)
    
    # Save grid params and inj loc
    brg.create_grid_parameters(this_dir, [nx, ny, dx, dy])
    brg.create_injection_locations(this_dir, 1, [Q_x, Q_y])
        
    # Save topography, permeability and porosity
    np.savetxt(input_dir + 'ceil_topo.txt',top.T)
    np.savetxt(input_dir + 'base_topo.txt',base.T)
    np.savetxt(input_dir + 'permeability.txt',perm.T)
    np.savetxt(input_dir + 'porosity.txt',poro.T)
    
    # Save topography params
    file_path = input_dir + 'topography_params.txt'
    with open(file_path, "w") as file:
        file.write(
            "-- topography parameters: theta, amplitude, wl_x, wl_ratio=wl_x/wl_y --\n"
        )
        for k, p in enumerate(param_range[i]):
            file.write(f"{p}".lstrip() + "\n")
    
    print(f'Generated and saved inputs for run {i+1}')