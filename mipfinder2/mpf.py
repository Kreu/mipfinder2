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
import interpro

# Set up logging configuration
logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    filename = 'mipfinder.log',
                    filemode = 'w',
                    format='%(asctime)s %(module)s.%(funcName)s %(levelname)-8s %(message)s',
                    datefmt = "%Y-%m-%d %H:%M:%S")
                #     format='%(asctime)s %(module)s %(name)s.%(funcName)s %(levelname)-8s %(message)s')

def createDir(dir_name: str):
  """Creates a directory in the current folder.
  
  If the parent directories in the path are missing, they are created. If the directory exists,
  it will be recreated. 
  
  """
  pathlib.Path(dir_name).mkdir(parents = True, exist_ok = True)

def removeDir(dir_name: str):
  """Removes a directory from the current folder.
  
  If the directory does not exist, the function does nothing.
  
  """
  try:
    shutil.rmtree('temp')
  except FileNotFoundError:
    pass


########################################Sølvgade ##########################################
#   __  __   _____   _____    ______   _Sølvgade ___   _   _   _____    ______   _____    #
#  |  \/  | |_   _| |  __ \  |  ____| |_Sølvgade   _| | \ | | |  __ \  |  ____| |  __ \   #
#  | \  / |   | |   | |__) | | |__      Sølvgade  |   |  \| | | |  | | | |__    | |__) |  #
#  | |\/| |   | |   |  ___/  |  __|     Sølvgade  |   | . ` | | |  | | |  __|   |  _  /   #
#  | |  | |  _| |_  | |      | |       _Sølvgade  |_  | |\  | | |__| | | |____  | | \ \   #
#  |_|  |_| |_____| |_|      |_|      |_Sølvgade ___| |_| \_| |_____/  |______| |_|  \_\  #
#                                                                                 #
#                                 ___         ___                                 #
#                                |__ \       / _ \                                #
#                        __   __    ) |     | | | |                               #
#                        \ \ / /   / /      | | | |                               #
#                         \ V /   / /_   _  | |_| |                               #
#                          \_/   |____| (_)  \___/                                #
#                                                                                 #
###################################################################################

"""
mipfinder v2.0

This script looks for microproteins within genomes. Microproteins are small regulatory
proteins which are thought to derive from ancestral genes.

"""
if __name__ == "__main__":
  # Setup
  logging.info("Starting MIPFINDER v2.0")
  logging.debug(f"Working directory is {os.getcwd()}")
  start_time = datetime.datetime.now() 
  conf = config.Config('config.ini')

  # Create directories to hold files for data processing


  # Main part
  logging.info(f"Extracting all protein IDs and sequences from {conf.organism_protein_list}...")
  organism_protein_list = fasta.extractRecords(conf.organism_protein_list)

  # Extract th

  # Create two groups of proteins, one with those of sequence length shorter than that of 
  # conf.maximum_mip_length and the other with sequence longer than the conf.minimum_ancestor_length
  potential_mips = {}
  potential_ancestors = {}

  # for fasta_header, protein_sequence in all_proteins.items():
  #   if protein.isLengthBetween(protein_sequence, 0, conf.maximum_mip_length):
  #     uniprot_id = fasta.extractUniprotID(fasta_header, 6)
  #     if uniprot_id:
  #       potential_mips[uniprot_id] = protein_sequence

  #   if protein.isLengthBetween(protein_sequence, conf.minimum_ancestor_length):
  #     uniprot_id = fasta.extractUniprotID(fasta_header, 6)
  #     if uniprot_id:
  #       potential_ancestors[uniprot_id] = protein_sequence

  # fasta.createFile(potential_mips, "mip_proteins.fasta")
  # fasta.createFile(potential_ancestors, "ancestor_proteins.fasta")

  # blast.createDatabase("ancestor_proteins.fasta", "ancestor_db")
  blast.run("blastp -query mip_proteins.fasta -db ancestor_db -outfmt 7 -out mip_blast.txt")

  # interpro.processTSV()
  print(len(organism_protein_list))
  print(len(potential_mips))
  print(len(potential_ancestors))
  # print(potential_ancestors)

  # Wrap up
  end_time = datetime.datetime.now()
  time_elapsed = end_time - start_time
  logging.info(f"Finished processing all the files in {time_elapsed} seconds.")



