import configparser
import os
import ddss_display

# ====================================================================================================================
# Author: Robert Jiang
# Name: DDSS v1.5.0.0
# File Name: ddss_config.py
# Description: Stores functions used by DDSS regarding the config file
# Version: 1.5.0.0
# ====================================================================================================================

# Creates a default ddss config.ini file if one does not exist already
def create_config():
    cp = configparser.ConfigParser()
    rs_curr, rr_curr, br_curr = ddss_display.get_current_settings()
    rs_supported, rr_supported, br_supported, rr_min, rr_max = ddss_display.get_supported_settings()

    # Sets the default AC settings to the current settings used by the display
    cp['AC'] = {
        'resolutionX': rs_curr[0],
        'resolutionY': rs_curr[1],
        'refreshRate': rr_curr,
        'brightness': br_curr
    }

    # Sets the default Battery settings to the most commonly used resolution, the lowest supported refresh rate, and a brightness of 0
    cp['Battery'] = {
        'resolutionX': '1366',
        'resolutionY': '768',
        'refreshRate': rr_min,
        'brightness': '0'
    }

    # Creates the config.ini file with the default settings
    with open('config.ini', 'w') as f:
        cp.write(f)

# Returns the display settings on AC and Battery given by the config file
def read_config():
    cp = configparser.ConfigParser()

    cp.read('config.ini')
    config_ac_rs = tuple([int(cp.get('AC', 'resolutionx')),
                          int(cp.get('AC', 'resolutiony'))])  # get desired resolution on AC from config
    config_ac_rr = int(cp.get('AC', 'refreshrate'))  # get desired refresh rate on AC from config
    config_ac_br = int(cp.get('AC', 'brightness'))  # get desired brightness on AC from config
    config_by_rs = tuple([int(cp.get('Battery', 'resolutionx')),
                          int(cp.get('Battery', 'resolutiony'))])  # get desired resolution on Battery from config
    config_by_rr = int(cp.get('Battery', 'refreshrate'))  # get desired refresh rate on Battery from config
    config_by_br = int(cp.get('Battery', 'brightness'))  # get desired brightness on Battery from config

    return config_ac_rs, config_ac_rr, config_ac_br, config_by_rs, config_by_rr, config_by_br

# Returns the config file path
def get_config_path():
    return os.getcwd() + "\config.ini"