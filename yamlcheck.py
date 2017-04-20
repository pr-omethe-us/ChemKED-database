# -*- coding: utf-8 -*-
"""
This script will check yaml files individually. 

"""
import os

from pyked.chemked import ChemKED

validate_file= ChemKED(yaml_file=os.path.join("t-butanol", "Bec_t-b_20atm.yaml"))

#validate_file= ChemKED(yaml_file="2-butanol/2-butanol_Moss_phi_1_2-b_0_0025.yaml")