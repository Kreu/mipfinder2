"""miPFinder version 2.0

WIP WIP WIP WIP
"""

import os
import logging

from Config import Config
# TODO: Maybe rewrite using ConfigArgParser module rather than configuration file? Not important atm
# Read configuration file (previously ArgParse CLI)

# TODO: Change back to 'config.ini' in the final version. Can't get VS Code to run the script from the subdir

config = Config('./mipfinder/config.ini')
