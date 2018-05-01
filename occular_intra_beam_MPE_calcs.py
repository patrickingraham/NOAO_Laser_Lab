import numpy as np
import pdb

def occular_intra_beam_MPE_calcs():

# Calculation of Direct Beam Exposure MPE in Zone 1
# Possible damage is Ocular and Skin

# Ocular calculations
# the dictionary below declares limits 1 and 2, which are often thermal and photochemical,
# or retina/cornea. Note that although all values are calculated, only the
# lower value is used as the MPE (this is done below).
        MPEs_intra_beam = {'wavelength': np.arange(0.0,2600,1.0), 
        'MPE_pulse_limit1' : np.zeros(2600),
        'MPE_pulse_limit2' : np.zeros(2600),
        'MPE_avg_limit1': np.zeros(2600), 
        'MPE_avg_limit2' : np.zeros(2600),
        'MPE_final' : np.zeros(2600)}
#
# Ocular damage MPE - Table 5a
# Table 2 states the intrabeam exposure durations for 180-400 nm is 100 seconds
# Pulsed lasers must consider the damage from a single pulse (rule 1 in section 8.2.3)
# and the average power (rule 2 in section 8.2.3) 
# So the considered exposure times in this section are 3e-9 and 100 seconds.
# When photochemical and thermal limits are given, the MPE is always the lower of the two values (table 5a note 2)

# MPEs for 300 to 303nm
        t=3e-9 # [s]
        lmin, lmax = 300, 303
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 0.56 * t**(0.25) # doesn't set index 303, only 300,301,302
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = 3e-3 # J/cm2
        t=100e0 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = 3e-3 # J/cm2

# MPEs for 303-315nm
        t=3e-9 # [s]
        lmin, lmax = 303, 315
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = 10**(0.2*( (MPEs_intra_beam['wavelength'][lmin:lmax])-295)) *10**(-4.0) # J/cm2
        t=100e0 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = 10**(0.2*( (MPEs_intra_beam['wavelength'][lmin:lmax])-295)) *10**(-4.0) # J/cm2

# MPEs for 315 to 400 nm
        t=3e-9 # [s]
        lmin, lmax = 315, 400
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=100e0 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = 1.0 # J/cm2


#Ocular damage MPE at visible wavelengths - Table 5b
# Table 2 states the intrabeam exposure duration is 0.25s between 400 and 700 nm
# Pulsed lasers must consider the damage from a single pulse (rule 1 in section 8.2.3)
# and the average power (rule 2 in section 8.2.3) 
# So the considered exposure times in this section are 3e-9 and 0.25 seconds.
# When photochemical and thermal limits are given, the MPE is always the lower of the two values (table 5b note 3)

#MPEs for 400-450
        lmin, lmax = 400, 450
        t=3e-9 # [s]
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 2e-7 # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=0.25 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.8e-3 * t**(0.75) # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates

#MPEs for 450-500
        lmin, lmax = 450, 500
        t=3e-9 # [s]
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 2e-7 # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=0.25 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.8e-3 * t**(0.75) # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates

#MPEs for 500-700
        lmin, lmax = 500, 700
        t=3e-9 # [s]
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 2e-7 # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=0.25 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.8e-3 * t**(0.75) # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates

# Ocular damage MPE - Table 5c
# Table 2 states the intrabeam exposure duration is 10s between 700 nm and 1400nm
#################################################################################
# This program calculates the INTRA-BEAM OCCULAR MPEs for the Ekspla nt-242 laser
#################################################################################

# Pulsed lasers must consider the damage from a single pulse (rule 1 in section 8.2.3)
# and the average power (rule 2 in section 8.2.3) 
# So the considered exposure times in this section are 3e-9 and 10 seconds.
# When photochemical and thermal limits are given, the MPE is always the lower of the two values (table 5b note 3)

# Note that in this table, retinal and corean affects are shown, we consider the retina to be thermal
# and the cornea photochemical just for book keeping reasons.
# This is moot since we always take the highest value (later on).
#MPEs for 700-1050
        lmin, lmax = 700, 1050 
        t=3e-9 # [s]
        C_A_700_1050 = 10**(0.002*(MPEs_intra_beam['wavelength'][lmin:lmax]-700))
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 2e-7 * C_A_700_1050 # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=10.0 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.8e-3 * t**(0.75) # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan  # no value in the table, thermal damage dominates
        
#MPEs for 1050-1200
        lmin, lmax = 1050, 1200
        t=3e-9 # [s]
        C_C_1050_1200 =  np.ones(lmax-lmin)
        C_C_1050_1200[0:100] = 1.0 # from 1050 to 1150 nm
        C_C_1050_1200[100:150] = 10.0**(0.018*(MPEs_intra_beam['wavelength'][lmin+100:lmax]-1150)) # from 1150 to 1200 nm

        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 2e-6 * C_C_1050_1200 # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=10.0 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.8e-3 * t**(0.75) # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        
        #MPEs for 1200-1400
        lmin, lmax = 1200, 1400
        t=3e-9 # [s]
        C_C_1200_1400 = 8.0 + 10.0**(0.04*(MPEs_intra_beam['wavelength'][1200:1400]-1250))
        K_lambda_1200_1400 = 10.0**(0.01*(1400-MPEs_intra_beam['wavelength'][1200:1400]))
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 2e-6 * C_C_1200_1400 # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = 0.3 * K_lambda_1200_1400 # J/cm2
        t=10.0 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 9.0e-3* C_C_1200_1400 * t**(0.75) # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = 0.3 * K_lambda_1200_1400 + 0.7# J/cm2

# Ocular damage MPE - Table 5d
# Table 2 states the intrabeam exposure duration is 10s between 1400 nm and 2600nm (actually 1000um)
# Pulsed lasers must consider the damage from a single pulse (rule 1 in section 8.2.3)
# and the average power (rule 2 in section 8.2.3) 
# So the considered exposure times in this section are 3e-9 and 10 seconds.
# No dual limits are present in this table for our exposures, so photochemical is just marked as nan

#MPEs for 1400-1500
        lmin, lmax = 1400, 1500 
        t=3e-9 # [s]
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 0.3 # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=10.0 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.0 # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan  # no value in the table, thermal damage dominates

#MPEs for 1500-1800
        lmin, lmax = 1500, 1800 
        t=3e-9 # [s]
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 1.0 # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=10.0 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.0 # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan  # no value in the table, thermal damage dominates

#MPEs for 1800-2600
        lmin, lmax = 1800, 2600 
        t=3e-9 # [s]
        MPEs_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 0.1 # J/cm2
        MPEs_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=10.0 # [s]
        MPEs_intra_beam['MPE_avg_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan  # no value in the table, thermal damage dominates

# Now return the minimum of all calculations
        MPEs_intra_beam['MPE_final'] = np.nanmin([MPEs_intra_beam['MPE_pulse_limit1'], MPEs_intra_beam['MPE_pulse_limit2'], MPEs_intra_beam['MPE_avg_limit1'],MPEs_intra_beam['MPE_avg_limit2']],axis=0)

        return MPEs_intra_beam


