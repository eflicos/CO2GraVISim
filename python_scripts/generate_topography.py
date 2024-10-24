# Written by ejf61
# Generates topography for poro_current.py

# Packages 
import numpy as np

def gen_top(top_type,nx,ny,dx,dy,Q_x,Q_y,theta,top_ampl_x,top_wl_x,top_ampl_y,top_wl_y):
    # Q_x,Q_y are injection location
    top_type = top_type.lower()
    
    if top_type=='flat':
        h_top = np.zeros((nx,ny))
        h_base = np.ones((nx,ny))
    
    if top_type=='slope_x':
        h_top, h_base = slope_x(nx,ny,dx,dy,Q_x,Q_y,theta)
        
    if top_type=='cos':
        h_top, h_base = sinusoidal(nx,ny,dx,dy,Q_x,Q_y,theta,top_ampl_x,top_wl_x,top_ampl_y,top_wl_y)
    
    return h_top, h_base

def sinusoidal(nx,ny,dx,dy,Q_x,Q_y,theta,top_ampl_x,top_wl_x,top_ampl_y,top_wl_y):
    """
    (x,y,ampl_x,wl_x,ampl_y,wl_y,theta)
    Creates topography with slope theta in x in RADIANS
    For now just single mode!
    Works with theta=0
    """
    # arrays zeroed at injection
    x_array = (np.arange(nx) - Q_x) * dx
    y_array = (np.arange(ny) - Q_y) * dy
    
    # Contribution from overall slop
    h_slope = - np.tan(theta) * x_array
    h_slope_array = np.transpose(np.tile(h_slope, (ny,1)))
    
    # # Number of modes in x and y
    # Nx = len(top_wl_x)
    # Ny = len(top_wl_y)
    
    h_top = np.zeros((nx,ny))
    h_top += h_slope_array
    
    if top_wl_x!=0:
        h_tmp = top_ampl_x * np.cos(2*np.pi/top_wl_x * x_array - np.pi)
        h_tmp_array = np.transpose(np.tile(h_tmp, (ny,1)))
        h_top += h_tmp_array
    
    if top_wl_y!=0:
        h_top[:] += top_ampl_y * np.cos(2*np.pi/top_wl_y * y_array - np.pi)
        
    h_base = h_top + 1
    # for i in range(Nx):
        # h_tmp = top_ampl_x[i] * np.cos(2*np.pi/top_wl_x[i] * x_array - np.pi)
        # h_tmp_array = np.transpose(np.tile(h_tmp, (ny,1)))
        # h_top += h_tmp_array

    # for i in range(Ny):
        # h_top[:] += top_ampl_y[i] * np.cos(2*np.pi/top_wl_y[i] * y_array - np.pi)
    
    # Needed this for line inj, don't think it matters when we aren't reaching the edge
    # h_top[0] = h_top[1]
    # h_top[-1] = h_top[-2]
    # h_top[:,0] = h_top[:,1]
    # h_top[:,-1] = h_top[:,-2]
    return h_top, h_base

def slope_x(nx,ny,dx,dy,Q_x,Q_y,theta):
    x_array = (np.arange(nx) - Q_x) * dx
    y_array = (np.arange(ny) - Q_y) * dy
    
    h_top_line = np.tan(theta) * x_array
    h_top = np.transpose(np.tile(h_top_line, (ny,1)))
    
    h_base = h_top + 1
    return h_top, h_top
