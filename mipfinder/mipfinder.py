"""miPFinder version 2.0

WIP WIP WIP WIP
"""

from config import Config
import logging
import datetime
import os

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
  # TODO: Change back to 'config.ini' in the final version. Can't get VS Code to run the script from the subdir
  # Read configuration file (previously ArgParse CLI)
  config = Config('./mipfinder/config.ini')

  config.protein_list = int(5)

# (Valdeko, 10/05/2019) TODO: Potentially move them into a configuration file and have three different variables? I don't know if
# there variables are used for more than this or if this is it. 
# blastPATH = '\"'+args['blastPATH']+'\"'
# hmmsearchPATH = '\"'+args['hmmPATH']+'hmmsearch.exe\"'
# hmmbuildPATH = '\"'+args['hmmPATH']+'hmmbuild.exe\"'
# hmmscanPATH = '\"'+args['hmmPATH']+'hmmscan.exe\"'
# clustalwPATH = '\"'+args['ClustalPATH']+'clustalw2.exe\"'


# IDlist = args['IDlist'].split(';')

# print '\nArguments:\n'+str(args).replace(',','\n')+'\nParsed arguments successfully, all tested dependencies are available'
