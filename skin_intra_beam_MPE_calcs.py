import numpy as np
import pdb

def skin_intra_beam_MPE_calcs():

# Calculation of intra-beam Beam Exposure MPE in Zone 1
# Possible damage is Ocular and Skin

# Ocular calculations
# the dictionary below declares limits 1 and 2, which are often thermal and photochemical,
# or retina/cornea. Note that although all values are calculated, only the
# lower value is used as the MPE (this is done below).
        MPEs_skin_intra_beam = {'wavelength': np.arange(0.0,2600,1.0), 
        'MPE_pulse_limit1' : np.zeros(2600),
        'MPE_pulse_limit2' : np.zeros(2600),
        'MPE_avg_limit1': np.zeros(2600), 
        'MPE_avg_limit2' : np.zeros(2600),
        'MPE_final' : np.zeros(2600)}
#
# Ocular damage MPE - Table 7a
# Table 2 states the intra_beam exposure durations for 180-400 nm is 100 seconds
# Pulsed lasers must consider the damage from a single pulse (rule 1 in section 8.2.3)
# and the average power (rule 2 in section 8.2.3) 
# So the considered exposure times in this section are 3e-9 and 100 seconds.
# When photochemical and thermal limits are given, the MPE is always the lower of the two values (table 5a note 2)

# MPEs for 300 to 303nm
        t=3e-9 # [s]
        lmin, lmax = 300, 303
        MPEs_skin_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 0.56 * t**(0.25) # doesn't set index 303, only 300,301,302
        MPEs_skin_intra_beam['MPE_pulse_limit2'][lmin:lmax] = 3e-3 # J/cm2
        t=100e0 # [s]
        MPEs_skin_intra_beam['MPE_avg_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_skin_intra_beam['MPE_avg_limit2'][lmin:lmax] = 3e-3 # J/cm2

# MPEs for 303-315nm
        t=3e-9 # [s]
        lmin, lmax = 303, 315
        MPEs_skin_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_skin_intra_beam['MPE_pulse_limit2'][lmin:lmax] = 10**(0.2*( (MPEs_skin_intra_beam['wavelength'][lmin:lmax])-295)) *10**(-4.0) # J/cm2
        t=100e0 # [s]
        MPEs_skin_intra_beam['MPE_avg_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_skin_intra_beam['MPE_avg_limit2'][lmin:lmax] = 10**(0.2*( (MPEs_skin_intra_beam['wavelength'][lmin:lmax])-295)) *10**(-4.0) # J/cm2

# MPEs for 315 to 400 nm
        t=3e-9 # [s]
        lmin, lmax = 315, 400
        MPEs_skin_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_skin_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=100e0 # [s]
        MPEs_skin_intra_beam['MPE_avg_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_skin_intra_beam['MPE_avg_limit2'][lmin:lmax] = 1.0 # J/cm2


# Skin damage MPE at visible wavelengths - Table 7b
# Table 2 states the intra_beam exposure duration is 0.25s between 400 and 700 nm
# then 10s for 700nm to 1400 nm
# Pulsed lasers must consider the damage from a single pulse (rule 1 in section 8.2.3)
# and the average power (rule 2 in section 8.2.3) 
# So the considered exposure times in this section are 3e-9, 0.25 and 10s seconds.
# When photochemical and thermal limits are given, the MPE is always the lower of the two values (table 5b note 3)

#MPEs for 400-700
        lmin, lmax = 400, 700
        t=3e-9 # [s]
        C_A_400_700 = 1.0
        MPEs_skin_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 2e-2 * C_A_400_700 # J/cm2
        MPEs_skin_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=0.25 # [s]
        MPEs_skin_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.1 * C_A_400_700 * t**(0.25) # J/cm2
        MPEs_skin_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates

#MPEs for 700-1050
        lmin, lmax = 700, 1050
        t=3e-9 # [s]
        C_A_700_1050 = 10**(0.002*(MPEs_skin_intra_beam['wavelength'][lmin:lmax]-700))
        MPEs_skin_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 2e-2 * C_A_700_1050 # J/cm2
        MPEs_skin_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=10.0 # [s]
        MPEs_skin_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.1 * C_A_700_1050 * t**(0.25) # J/cm2
        MPEs_skin_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates

        #MPEs for 1050-1400
        lmin, lmax = 1050, 1400
        t=3e-9 # [s]
        C_A_1050_1400 = 5.0 
        MPEs_skin_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 2e-2 * C_A_1050_1400 # J/cm2
        MPEs_skin_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=10.0 # [s]
        MPEs_skin_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.1 * C_A_1050_1400 * t**(0.25) # J/cm2
        MPEs_skin_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates

# Skin intra-beam damage MPE - Table 7c
# Table 2 states the intra_beam exposure duration is 10s between 1400 nm and 2600nm (actually  1000um)
# Pulsed lasers must consider the damage from a single pulse (rule 1 in section 8.2.3)
# and the average power (rule 2 in section 8.2.3) 
# So the considered exposure times in this section are 3e-9 and 10 seconds.
# No dual limits are present in this table for our exposures, so photochemical is just marked as nan

#MPEs for 1400-1500
        lmin, lmax = 1400, 1500 
        t=3e-9 # [s]
        MPEs_skin_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 0.3 # J/cm2
        MPEs_skin_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=10.0 # [s]
        MPEs_skin_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.0 # J/cm2
        MPEs_skin_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan  # no value in the table, thermal damage dominates

#MPEs for 1500-1800
        lmin, lmax = 1500, 1800 
        t=3e-9 # [s]
        MPEs_skin_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 1.0 # J/cm2
        MPEs_skin_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=10.0 # [s]
        MPEs_skin_intra_beam['MPE_avg_limit1'][lmin:lmax] = 1.0 # J/cm2
        MPEs_skin_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan  # no value in the table, thermal damage dominates

#MPEs for 1800-2600
        lmin, lmax = 1800, 2600 
        t=3e-9 # [s]
        MPEs_skin_intra_beam['MPE_pulse_limit1'][lmin:lmax] = 0.1 # J/cm2
        MPEs_skin_intra_beam['MPE_pulse_limit2'][lmin:lmax] = np.nan # no value in the table, thermal damage dominates
        t=10.0 # [s]
        MPEs_skin_intra_beam['MPE_avg_limit1'][lmin:lmax] = 0.56 * t**(0.25) # J/cm2
        MPEs_skin_intra_beam['MPE_avg_limit2'][lmin:lmax] = np.nan  # no value in the table, thermal damage dominates

# Now return the minimum of all calculations
        MPEs_skin_intra_beam['MPE_final'] = np.nanmin([MPEs_skin_intra_beam['MPE_pulse_limit1'], MPEs_skin_intra_beam['MPE_pulse_limit2'], MPEs_skin_intra_beam['MPE_avg_limit1'],MPEs_skin_intra_beam['MPE_avg_limit2']],axis=0)

        return MPEs_skin_intra_beam


