"""miPFinder version 2.0

WIP WIP WIP WIP
"""

import config

import logging
import datetime
import os
import sys
import typing

# Set up logging configuration
logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    filename = 'mipfinder.log',
                    filemode = 'w',
                    format='%(name)s:%(levelname)s:%(message)s')

# TODO: Write a unit test for this
def getKnownMicroproteins(microprotein_list: str) -> typing.List[str]:
  """Extract known microprotein IDs from a file into a list.""" 
  known_microproteins = []
  with open(microprotein_list, 'r') as f:
    for line in f:
      known_microproteins.append(f)
  return known_microproteins 


######################
#   MIPFINDER v2.0   #
######################

if __name__ == "__main__":
  logging.info("Starting MIPFINDER v2.0")
  # TODO (12/05/2019, Valdeko): Format the datetime to get rid of microseconds
  logging.info(f"Starting at {datetime.datetime.now()}")
  logging.debug(f"Working directory is {os.getcwd()}")

  # TODO: Maybe rewrite using ConfigArgParser module rather than configuration file? Not important atm
  configuration = config.Config('config.ini')

  getKnownMicroproteins(configuration.known_microproteins)


