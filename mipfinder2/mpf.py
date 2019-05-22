"""miPFinder version 2.0

WIP WIP WIP WIP
"""
import logging
import datetime
import pathlib
import shutil
import typing

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import config
import blast
import fasta
import protein

# Set up logging configuration
logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    filename = 'mipfinder.log',
                    filemode = 'w',
                    format='%(asctime)s %(module)s.%(funcName)s %(levelname)-8s %(message)s',
                    datefmt = "%Y-%m-%d %H:%M:%S")
                #     format='%(asctime)s %(module)s %(name)s.%(funcName)s %(levelname)-8s %(message)s')

def getKnownMicroproteins(microprotein_list: str) -> typing.List[str]:
  """Extracts known microprotein IDs from a file into a list.
  
  Returns:
    A list containing all microprotein UniProt IDs""" 
  known_microproteins = []
  with open(microprotein_list, 'r+') as f:
    for line in f:
      known_microproteins.append(line.strip('\n'))
  return known_microproteins 

def createTempDirs():
  """Creates temporary directories to hold processing files."""
  pathlib.Path('temp').mkdir(parents = True, exist_ok = True)
  pathlib.Path('temp/blast').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/clustalo').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/hmmer').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/aligment').mkdir(parents=True, exist_ok = True)

def removeTempDirs():
  """Removes temporary directories that hold processing files.
  
  If temporary directories do not exist, the function does nothing
  
  """
  try:
    shutil.rmtree('temp')
  except FileNotFoundError:
    pass


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

  all_proteins = fasta.extractFastaRecords(conf.organism_protein_list)
  # Create two groups of proteins, one with those of sequence length shorter than that of 
  # conf.maximum_mip_length and the other with sequence longer than the conf.minimum_ancestor_length
  potential_mips = {}
  potential_ancestors = {}

  for fasta_header, protein_sequence in all_proteins.items():
    if protein.isLengthBetween(protein_sequence, 0, conf.maximum_mip_length):
      uniprot_id = fasta.extractUniprotID(fasta_header, 5)
      if uniprot_id:
        potential_mips[uniprot_id] = protein_sequence

    if protein.isLengthBetween(protein_sequence, conf.minimum_ancestor_length):
      uniprot_id = fasta.extractUniprotID(fasta_header, 5)
      if uniprot_id:
        potential_ancestors[uniprot_id] = protein_sequence

  fasta.createFastaFile(potential_mips, "mip_proteins.fasta")
  fasta.createFastaFile(potential_ancestors, "ancestor_proteins.fasta")

  blast.createBlastDatabase("ancestor_proteins.fasta", "ancestor_db")
  blast.runBlast("blastp -query mip_proteins.fasta -db ancestor_db -outfmt 7 -out mip_blast.txt")

  print(len(all_proteins))
  print(len(potential_mips))
  print(len(potential_ancestors))
  # print(potential_ancestors)

  



