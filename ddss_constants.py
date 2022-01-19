# ====================================================================================================================
# Author: Robert Jiang
# Name: DDSS v1.5.0.0
# File Name: ddss_constants.py
# Description: Stores constants used by DDSS
# Version: 1.5.0.0
# ====================================================================================================================

# priority list of resolutions when on AC in case desired config resolution is unsupported
ac_rs_priority =   [tuple([2560, 1440]),
                    tuple([1920, 1080]),
                    tuple([1600, 900]),
                    tuple([1366, 768]),

                   tuple([2560, 1600]),
                   tuple([1920, 1200]),
                   tuple([1680, 1050]),
                   tuple([1440, 900]),

                   tuple([2048, 1536]),
                   tuple([1920, 1440]),
                   tuple([1600, 1200]),
                   tuple([1440, 1080])]

# priority list of resolutions when on battery in case desired config resolution is unsupported
by_rs_priority =  [tuple([1280, 720]),
                   tuple([1152, 648]),
                   tuple([1024, 576]),

                   tuple([1280, 800]),

                   tuple([1280, 960]),
                   tuple([1024, 768])]