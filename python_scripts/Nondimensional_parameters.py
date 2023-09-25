# Nondimensional_parameters.py
# This script converts the relevant dimensional values into the corresponding
# nondimensional parameters used by CO2GraVISim


## Dimensional parameters ####################################################

#Injection flux scale [m^3 s^-1]
Q_scale = 4.9e-3

#Porosity scale [-]
poro_scale = 0.25

#Permeability scale [m^2]
perm_scale = 2.5e-12

#CO_2 density [kg m^-3]
rho_current = 348.

#Unsaturated ambient density [kg m^-3]
rho_ambient_unsat = 997.

#Saturated ambient density [kg m^-3]
rho_ambient_sat = 1007.5

#CO_2 viscosity [Pa s]
mu_c = 3e-5

#Ambient viscosity [Pa s]
mu_a = 8.9e-4

#Reservoir width scale [m]
H_scale = 34.

#residual saturation of the CO_2 [-]
s_c_r = 0.2

#irreducible saturation of the ambient [-]
s_a_i = 0.1

#Molecular diffusivity of the CO_2 [m^2 s^-1]
Dmol = 2e-9

#Volume fraction of CO_2 dissolved in saturated ambient
C_sat = 0.04

#Gravitational acceleration [m s^-2]
g = 9.81




#Density difference between the CO_2 and the unsaturated ambient
delta_rho = rho_ambient_unsat - rho_current

#Density difference between the saturated and unsaturated ambient
delta_rho_amb = rho_ambient_sat - rho_ambient_unsat


#buoyancy velocity scale [m s^-1]
u_b = (delta_rho * g * perm_scale) / mu_c

#Flux velocity scale [m s^-1]
u_Q = Q_scale / (H_scale**2)


#Dimensional convective flux [m s^-1]
b_qd = 0.12
n_qd = 0.84
q_d_dim = b_qd * ( poro_scale * C_sat * Dmol / H_scale ) *\
      ( (delta_rho_amb * g * perm_scale * H_scale)/(poro_scale*mu_a*Dmol) )**(n_qd)


## Dimensional scales not specified by the user #####################################

#Flux timescale [s]
T_scale = (poro_scale * H_scale) / u_Q

#Flux pressure scale [Pa]
P_scale = (mu_c / perm_scale) * (Q_scale / H_scale)


## Nondimensional parameters #########################################################

#Viscosity ratio
M_val = mu_c / mu_a

#Buoyancy-Flux ratio
Gamma_val = u_b / u_Q

#Nondimensional convective flux
q_d_nondim = q_d_dim / u_Q


## Print relevant values ############################################################

print('\n')
print('The dimensional flux-based timescale is')
print(f'T_scale = {T_scale:.5f} [s]')
print(f'        = {T_scale / 3600:.5f} [hrs]')
print(f'        = {T_scale / (3600*24):.5f} [days]')
print(f'        = {T_scale / (3600*24*365.25):.5f} [yrs]')

print('\n')
print('The dimensional flux-based pressure scale is')
print(f'P_scale = {P_scale:.5f} [Pa]')
print(f'        = {P_scale/1e3:.5f} [kPa]')
print(f'        = {P_scale/1e6:.5f} [MPa]')

print('\n')
print('The buoyancy velocity scale is')
print(f'u_b = {u_b} [m s^-1]')

print('\n')
print('The flux velocity scale is')
print(f'u_Q = {u_Q} [m s^-1]')

print('\n')
print('The viscosity ratio is')
print(f'M = {M_val}')

print('\n')
print('The buoyancy-flux ratio is ')
print(f'Gamma = u_b/u_Q = {Gamma_val}')

print('\n')
print('The nondimensional convective dissolution flux is')
print(f'q_d = {q_d_nondim}')

print('\n')
print('---------------------------------------------------')
print('The values required for flow_parameters.txt are:')
print('(M, Gamma_val, s_c_r, s_a_i, C_sat, q_dissolve)')
print(f'{M_val:.8f}')
print(f'{Gamma_val:.8f}')
print(f'{s_c_r:.8f}')
print(f'{s_a_i:.8f}')
print(f'{C_sat:.8f}')
print(f'{q_d_nondim:.8f}')



