# -*- coding: utf-8 -*-
"""
This script will check chemked yaml files individually. 
Morgan Mayer 3-29-2017

"""

from pyked.chemked import ChemKED

validate_file= ChemKED(yaml_file="n-butanol\Stranic2012_nbutanol_xO2=0.04_phi=0.5.yaml")