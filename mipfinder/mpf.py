"""miPFinder version 2.0

WIP WIP WIP WIP
"""

import config
import logging
import datetime
import os
import typing

# Set up logging configuration
logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    filename = 'mipfinder.log',
                    filemode = 'w',
                    format='%(name)s:%(levelname)s:%(message)s')

if __name__ == "__main__":
  logging.info("Starting miPFinder v2.0")
  logging.info(f"Starting at {datetime.datetime.now()}")
  logging.debug(f"Working directory is {os.getcwd()}")

  # TODO: Maybe rewrite using ConfigArgParser module rather than configuration file? Not important atm
  # Read configuration file (previously ArgParse CLI)
  configuration = config.Config('config.ini')

  # TODO: Write a unit test for this
  def getKnownMicroproteins(microprotein_list: str) -> typing.List[str]:
    """Extract known microprotein IDs from a file into a list.""" 
    known_microproteins = []
    with open(microprotein_list, 'r') as f:
      for line in f:
        known_microproteins.append(f)
    return known_microproteins 

  # (Valdeko, 10/05/2019) TODO: Potentially move them into a configuration file and have three different variables? I don't know if
  # there variables are used for more than this or if this is it. 
  # blastPATH = '\"'+args['blastPATH']+'\"'
  # hmmsearchPATH = '\"'+args['hmmPATH']+'hmmsearch.exe\"'
  # hmmbuildPATH = '\"'+args['hmmPATH']+'hmmbuild.exe\"'
  # hmmscanPATH = '\"'+args['hmmPATH']+'hmmscan.exe\"'
  # clustalwPATH = '\"'+args['ClustalPATH']+'clustalw2.exe\"'

# print '\nArguments:\n'+str(args).replace(',','\n')+'\nParsed arguments successfully, all tested dependencies are available'
