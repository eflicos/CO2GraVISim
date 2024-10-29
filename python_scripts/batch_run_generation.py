# batch_run_generation.py (17/03/24)
# This python script can be used to generate the various folders and
# input files used for a batch run of CO2GraVISim

# Built with help from ChatGPT 3.5

import os
import shutil
from datetime import datetime
import numpy as np
from itertools import product

# from brg.brg_grid_parameters import nx, ny, dx, dy
# from brg.brg_flow_parameters import flow_params, N_flow
# from brg.brg_BC_parameters import h_BCs, P_BCs
# from brg.brg_plot_times import pt_waypoints, pt_intervals
# from brg.brg_topography_parameters import topo_params, N_topo
# from brg.brg_poro_and_perm_parameters import poro_perm_params, N_poro_perm
# from brg.brg_injection_parameters import (
    # n_inj_locs,
    # inj_loc_idxs,
    # n_flux_vals,
    # flux_times,
    # flux_vals,
    # N_flux,
# )

# from input_generation import input_gen
# from Generate_Plot_times import pt_generate


def archive_existing_runs(target_directory):
    # Generate a unique name for the archive directory based on the current datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_directory = os.path.join(target_directory, f"Archived/old_runs_{timestamp}")

    # Create the archive directory if there are any run_N folders to move
    created_archive = False

    for item in os.listdir(target_directory):
        item_path = os.path.join(target_directory, item)
        # If the item is a directory and its name starts with 'run_'
        if os.path.isdir(item_path) and item.startswith("run_"):
            if not created_archive:
                os.makedirs(archive_directory, exist_ok=True)
                created_archive = True
            # Move the run_N directory to the archive directory
            shutil.move(item_path, os.path.join(archive_directory, item))
            print(f"Moved {item} to {archive_directory}")


def copy_common_files(input_directory, common_files_dir):
    for filename in os.listdir(common_files_dir):
        file_path = os.path.join(common_files_dir, filename)
        if os.path.isfile(file_path):
            shutil.copy(file_path, input_directory)


def create_folders(target_directory, num_runs, archive_boo):

    # Make sure the target directory exists, if not, create it
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    elif archive_boo:
        # Archive any existing run_N directories
        archive_existing_runs(target_directory)

    for i in range(1, num_runs + 1):
        # Create the run_N directory
        run_directory = os.path.join(target_directory, f"run_{i}")
        os.makedirs(run_directory, exist_ok=True)

        # Inside each run_N directory, create Input and Output directories
        input_directory = os.path.join(run_directory, "Input")
        output_directory = os.path.join(run_directory, "Output")
        os.makedirs(input_directory, exist_ok=True)
        os.makedirs(output_directory, exist_ok=True)
        # Create folders within Output directories
        os.makedirs(os.path.join(output_directory, "Current_Pressure"), exist_ok=True)
        os.makedirs(os.path.join(output_directory, "Current_Thickness"), exist_ok=True)
        os.makedirs(os.path.join(output_directory, "Current_Volume"), exist_ok=True)
        os.makedirs(os.path.join(output_directory, "Other"), exist_ok=True)

        # # Copy common files to the Input directory
        # # copy_common_files(input_directory, common_files_dir)

        print(f"Created: {run_directory}\n\tWith subdirectories: Input, Output")


def create_grid_parameters(run_directory, parameters):

    file_path = os.path.join(run_directory, f"Input/grid_parameters.txt")
    with open(file_path, "w") as file:
        file.write("-- grid parameters: nx, ny, nz, dx, dy --\n")
        for k, p in enumerate(parameters):
            file.write(f"{p}".lstrip() + "\n")


def create_flow_parameters(run_directory, parameters):

    file_path = os.path.join(run_directory, f"Input/flow_parameters.txt")
    with open(file_path, "w") as file:
        file.write(
            "-- flow parameters: M, Gamma_val, s_c_r, s_a_i, C_sat, q_dissolve --\n"
        )
        for k, p in enumerate(parameters):
            file.write(f"{p}".lstrip() + "\n")


def create_boundary_conditions(run_directory, h_BC_vals, P_BC_vals):

    file_path = os.path.join(run_directory, f"Input/boundary_conditions.txt")

    # Convert list to a suitably spaced string
    h_BC_line = " ".join(map(str, h_BC_vals))
    h_BC_line += "\n"

    P_BC_line = " ".join(map(str, P_BC_vals))
    P_BC_line += "\n"

    with open(file_path, "w") as file:
        file.writelines(
            [
                "-- Set the parameter values for the BCs, first --\n",
                "-- for the current thickness h, then for the   --\n",
                "-- ambient pressure P. Specify for the North,  --\n",
                "-- East, South, and West sides of the domain.  --\n",
                "-- Dirichlet BCs (f=0) are labelled by 1,      --\n",
                "-- Neumann BCs (df/dn = 0) by 2.               --\n",
            ]
        )
        file.write(h_BC_line)
        file.write(P_BC_line)


# def create_plot_times(run_directory, times, intervals):


def create_injection_locations(run_directory, n, idxs):

    file_path = os.path.join(run_directory, f"Input/injection_locations.txt")
    with open(file_path, "w") as file:
        file.writelines(
            [
                "-- n_inj_locs - number of injection points in use, followed by --\n",
                "-- x_idx, y_idx for each injection point, on separate rows     --\n",
            ]
        )
        file.write(f"{n}\n")
        
        # I get an error if n=1 in for loop, so separating out into own case
        if n==1:
            file.write(
                f"{idxs[0]:d}".lstrip() + " " + f"{idxs[1]:d}".lstrip() + "\n"
            )
        else:
            for k in range(0, n):
                file.write(
                    f"{idxs[k][0]:d}".lstrip() + " " + f"{idxs[k][1]:d}".lstrip() + "\n"
                )


def create_injection_profile(run_directory, n, times, vals):

    file_path = os.path.join(run_directory, f"Input/injection_profile.txt")
    with open(file_path, "w") as file:
        file.writelines(
            [
                "-- n_flux_vals - no. of times the injection flux is adjusted, --\n",
                "-- followed by t, Q_1(t), ..., Q_n(t), where n is the no. of  --\n",
                "-- injection points specified in Injection_points.txt         --\n",
            ]
        )
        file.write(f"{n}\n")
        for k in range(0, n):
            file.write(f"{times[k]}".lstrip() + " " + f"{vals[k]:5.4g}".lstrip() + "\n")


if __name__ == "__main__":

    # Generate batch run folders

    target_dir = "./batch_run_test/"  # Update this path as needed
    common_files_dir = "./batch_run_test/Common_files"  # Specify the path to the Common_files directory

    # print('nx, ny, dx, dy: ', nx, ny, dx, dy)

    print("flux_times: ", flux_times)
    print("flux_vals:  ", flux_vals)

    # Total number of runs
    N_runs = N_flow * N_topo * N_poro_perm * N_flux

    # Combinations of indices to access Topography parameters and Porosity and Permeability parameters
    index_array = list(
        product(
            range(0, N_flow), range(0, N_topo), range(0, N_poro_perm), range(0, N_flux)
        )
    )

    create_folders(target_dir, N_runs)

    for i in range(0, N_runs):

        print(f"\n [ -- n = {i+1} -- ] \n")

        flow_idx = index_array[i][0]  # Flow parameters
        topo_idx = index_array[i][1]  # Topography parameters
        poro_idx = index_array[i][2]  # Porosity and Permeability parameters
        flux_idx = index_array[i][3]  # Injection flux parameters

        run_directory = os.path.join(target_dir, f"run_{i+1}")
        run_Input_directory = os.path.join(run_directory, "Input")

        # print("-- grid parameters")
        # create_grid_parameters(run_directory, [nx, ny, nz, dx, dy])

        print("-- flow parameters")
        create_flow_parameters(run_directory, flow_params[flow_idx])

        # print("-- boundary conditions")
        # create_boundary_conditions(run_directory, h_BCs, P_BCs)

        # print("-- injection locations")
        # create_injection_locations(run_directory, n_inj_locs, inj_loc_idxs)

        # print("-- injection profile")
        # create_injection_profile(
        #     run_directory, n_flux_vals, flux_times[flux_idx], flux_vals[flux_idx]
        # )

        # print("-- topography, porosity, and permeability")
        # input_gen(
        #     run_Input_directory,
        #     nx,
        #     ny,
        #     dx,
        #     dy,
        #     n_inj_locs,
        #     inj_loc_idxs[0],
        #     False,  # Plot_Flag
        #     poro_perm_params[poro_idx][0],
        #     poro_perm_params[poro_idx][1:],
        #     topo_params[topo_idx][0:4],
        #     topo_params[topo_idx][4:],
        # )

        # print("-- plot times \n")
        # pt_generate(
        #     run_Input_directory,
        #     pt_waypoints,
        #     pt_intervals,
        #     False,  # Print_Flag
        # )

        # # # # #!! For Otway !!
        # # # # print("--! Copying Otway Topography !--")
        # # # # shutil.copy("./batch_run_test/Common_files/ceil_topo.txt", run_Input_directory)
        # # # # shutil.copy("./batch_run_test/Common_files/base_topo.txt", run_Input_directory)
