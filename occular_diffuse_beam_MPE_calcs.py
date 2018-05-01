#### THIS IS NOT ACTUALLY USED AND IS NOT FINISHED.

import numpy as np
import pdb

def occular_diffuse_beam_MPE_calcs():

# Calculation of Occular Diffuse Beam Exposure MPE
# This is calculated for a given beam diameter

        MPEs_occular_diffuse = {'Zone1_radius': 0.0, 'Zone2_radius' :0.0,
                                'Zone3_radius' :0.0,
                                'MPE_diffuse_zone1_limit' : np.zeros(2600),
                                'MPE_diffuse_zone2_limit' : np.zeros(2600},
                                'MPE_diffuse_zone3_center' : np.zeros(2600}}

#MPEs_scenario1_intrabeam


# Page 326 of the LIA manual states the diffuse beam MPE can be
# calculated from the intra-beam MPE. One need only calculate 
# the correction factor C_E for each of the 3 Zones

# The MPE is dependent upon the angular size of the source.
# alpha_min (which is the angular size of 1.5 mrad which is the diffraction limit 
# of the eye [pg 324 of LIA book]),

        r1_distance_mm = beam_diameter_mm/np.tan(1.5e-3) # [mm] 
        MPEs_occular_diffuse['Zone1_radius']=r1_distance_mm
        # for the Ekspla-242 this is - 1180 mm for 1.77mm Ekspla beam

# so Zone1 is when the viewer is further away than r1_distance_mm
# for this C_E = 1.0, so we treat as intrabeam viewing
        C_E=1.0
        MPEs_occular_diffuse['MPE_diffuse_zone1_limit']=MPEs_scenario1_intrabeam['final']*1.0


# Zone 2 is when the viewer is between r1_distance_mm and 10*beam_diameter_mm
# for the Ekspla nt-242, this is between 1.77m and 17 mm
        MPEs_occular_diffuse['Zone2_radius']=10.0*beam_diameter_mm
        #C_E is alpha/alpha_min --> we calculate only the innermost (maximum) value
        C_E=np.atan(1.0/10)/1e-3 # equal to 100.
        MPEs_occular_diffuse['MPE_diffuse_zone2_limit']=MPEs_scenario1_intrabeam['final']*C_E
        
# Zone 3 is when the viewer is less than 10*beam_diameter_mm = 17mm
# this is so close that it is practically impossible, we calculate the
# MPE at half of this distance


        return MPEs_occular_diffuse


