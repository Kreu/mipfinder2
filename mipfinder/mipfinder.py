"""miPFinder version 2.0

WIP WIP WIP WIP
"""

from config import Config
import logging

# Set up logging configuration
logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    filename = 'mipfinder.log',
                    filemode = 'w',
                    format='%(name)s:%(levelname)s:%(message)s')

# TODO: Maybe rewrite using ConfigArgParser module rather than configuration file? Not important atm
# Read configuration file (previously ArgParse CLI)
# TODO: Change back to 'config.ini' in the final version. Can't get VS Code to run the script from the subdir

logging.info("Starting miPFinder v2.0")
config = Config('./mipfinder/config.ini')
