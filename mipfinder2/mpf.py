"""miPFinder version 2.0

WIP WIP WIP WIP
"""
import logging
import datetime
import pathlib
import shutil
import typing
import subprocess

# TODO (Valdeko, 13/05/2019): This is here to get relative imports to work. This will have to change
# though. 
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# from scripts import alignments_v13

import config

# from ..scripts import alignments_v13
# from ..scripts import splicevariants_v13
# from ..scripts import splitdb_v13
from scripts import read_v13
# from ..scripts import delta_v13
# from ..scripts import domains_v13

# from alignments_v13 import ALIGNMENTRATING
# from splicevariants_v13 import splicevariantsSEQ
# from splitdb_v13 import splitdb
# from read_v13 import readAnnotation, readFasta, readBlastTAB, readProteinGeneList, readiPfam, readDOMTBL, readSTRING
# from delta_v13 import percentsmall, percentZones
# from domains_v13 import domains, domainOverlap

# Set up logging configuration
logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    filename = 'mipfinder.log',
                    filemode = 'w',
                    format='%(asctime)s %(module)s.%(funcName)s %(levelname)-8s %(message)s',
                    datefmt = "%Y-%m-%d %H:%M:%S")
                #     format='%(asctime)s %(module)s %(name)s.%(funcName)s %(levelname)-8s %(message)s')

# TODO: Write a unit test for this
def getKnownMicroproteins(microprotein_list: str) -> typing.List[str]:
  """Extract known microprotein IDs from a file into a list.
  
  Returns:
    list: A list containing all microprotein UniProt IDs""" 
  known_microproteins = []
  with open(microprotein_list, 'r+') as f:
    for line in f:
      known_microproteins.append(line.strip('\n'))
  return known_microproteins 

def createTempDirs():
  """Create temporary directories to hold processing files."""
  pathlib.Path('temp').mkdir(parents = True, exist_ok = True)
  pathlib.Path('temp/blast').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/clustalo').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/hmmer').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/aligment').mkdir(parents=True, exist_ok = True)

def removeTempDirs():
  """Remove temporary directories that hold processing files.
  
  If temporary directories do not exist, the function does nothing
  
  """
  try:
    shutil.rmtree('temp')
  except FileNotFoundError:
    pass


def extractFastaRecords(fasta_file: str) -> typing.Dict[str, str]:
  """Extract all FASTA records from a file into individual entries.

.

  Args:
    fasta_file (str): Path to a file containing all the proteins of the target
                      organism in FASTA format.
  Returns:
    dict: Dictionary containing protein FASTA identifier as the key and protein sequence
          as the value.

  """

  with open(fasta_file, 'r') as f:
    fasta_identifier = ""
    fasta_sequence = ""
    fasta_records = {}
    fasta_record_found = False

    for line in f:
      #Strip newlines because they interfere with processing
      line = line.strip('\n')
      
      # A FASTA format contains a line always starting with '>' character. This line contains 
      # information about the sequence such as its ID, source organism, gene code or the like

      # If we find a line that starts with a '>' without encountering one before, that signifies 
      # the start of the first FASTA record
      if line.startswith('>') and not fasta_record_found:
        fasta_record_found = True
        fasta_identifier = line
        continue

      # If a record has been found and the line does not denote another record, it contains 
      # a sequence that corresponds to the record found.
      elif not line.startswith('>') and fasta_record_found:
        fasta_sequence += line
        continue

      # If we have been reading in a FASTA record and find another one, we need to save
      # the old record and start reading in the new one.
      elif line.startswith('>') and fasta_record_found:
        fasta_records[fasta_identifier] = fasta_sequence
        # Reset the contents of the sequence and set the new identifier
        fasta_sequence = ""
        fasta_identifier = line
        continue

      # If FASTA record has not been found, the line contains bad data as far as we are concerned
      elif not fasta_record_found:
        continue

    # Finally, if we hit the last line of the file, we need to write the last entry.
    fasta_records[fasta_identifier] = fasta_sequence

    return fasta_records



###################################################################################
#   __  __   _____   _____    ______   _____   _   _   _____    ______   _____    #
#  |  \/  | |_   _| |  __ \  |  ____| |_   _| | \ | | |  __ \  |  ____| |  __ \   #
#  | \  / |   | |   | |__) | | |__      | |   |  \| | | |  | | | |__    | |__) |  #
#  | |\/| |   | |   |  ___/  |  __|     | |   | . ` | | |  | | |  __|   |  _  /   #
#  | |  | |  _| |_  | |      | |       _| |_  | |\  | | |__| | | |____  | | \ \   #
#  |_|  |_| |_____| |_|      |_|      |_____| |_| \_| |_____/  |______| |_|  \_\  #
#                                                                                 #
#                                 ___         ___                                 #
#                                |__ \       / _ \                                #
#                        __   __    ) |     | | | |                               #
#                        \ \ / /   / /      | | | |                               #
#                         \ V /   / /_   _  | |_| |                               #
#                          \_/   |____| (_)  \___/                                #
#                                                                                 #
###################################################################################

if __name__ == "__main__":
  logging.info("Starting MIPFINDER v2.0")
  logging.debug(f"Working directory is {os.getcwd()}")
  start_time = datetime.datetime.now() 

  # TODO: Maybe rewrite using ConfigArgParser module rather than configuration file? Would allow to 
  # quickly override paramteres from the command line. Howveer it is not currently important.
  conf = config.Config('config.ini')

  extractFastaRecords(conf.organism_protein_list)
  print