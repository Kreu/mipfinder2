"""miPFinder version 2.0

WIP WIP WIP WIP
"""
import datetime
import logging
import os
import pathlib
import shutil
import sys
import typing

import blast
import config
import fasta
import interpro
from protein import Protein
import string_db


# TODO(Valdeko): Move these into a separate file, they don't really belong here.
def createDir(dir_name: str):
  """Creates a directory in the current folder.
  
  If the parent directories in the path are missing, they are created. If the directory exists,
  it will be recreated. 
 rotein.Protein 
  Args:
    dir_name: Name of the directory to be created.
  
  """
  pathlib.Path(dir_name).mkdir(parents = True, exist_ok = True)

def removeDir(dir_name: str):
  """Removes a directory from the current folder.
  
  If the directory does not exist, the function does nothing.
 
  Args:
    dir_name: Name of the directory to be created.
    
  """
  try:
    shutil.rmtree('temp')
  except FileNotFoundError:
    pass


##################################################################################
#   __  __   _____   _____    ______   ____   _   _   _____    ______   _____    #
#  |  \/  | |_   _| |  __ \  |  ____| |_  _| | \ | | |  __ \  |  ____| |  __ \   #
#  | \  / |   | |   | |__) | | |__      | |  |  \| | | |  | | | |__    | |__) |  #
#  | |\/| |   | |   |  ___/  |  __|     | |  | . ` | | |  | | |  __|   |  _  /   #
#  | |  | |  _| |_  | |      | |       _| |_ | |\  | | |__| | | |____  | | \ \   #
#  |_|  |_| |_____| |_|      |_|      |____| |_| \_| |_____/  |______| |_|  \_\  #
#                                                                                #
#                                 ___        ___                                 #
#                                |__ \      / _ \                                #
#                        __   __    ) |     || | |                               #
#                        \ \ / /   / /      || | |                               #
#                         \ V /   / /_   _  ||_| |                               #
#                          \_/   |____| (_) \___/                                #
#                                                                                #
###################################################################################

def main():

  # Setup
  currentdir = os.path.dirname(os.path.realpath(__file__))
  sys.path.append(os.path.dirname(currentdir))

  # Set up logging configuration
  logging.getLogger(__name__)
  logging.basicConfig(level=logging.DEBUG,
                      filename = 'mipfinder.log',
                      filemode = 'w',
                      format='%(asctime)s %(module)s.%(funcName)s %(levelname)-8s %(message)s',
                      datefmt = "%Y%m-%d %H:%M:%S")
  # format='%(asctime)s %(module)s %(name)s.%(funcName)s %(levelname)-8s %(message)s')
    
  logging.info("Starting MIPFINDER v2.0")
  logging.debug(f"Working directory is {os.getcwd()}")
  start_time = datetime.datetime.now() 
  conf = config.Config('config.ini')

  # Create directories to hold files for data processing
  createDir('blast')
  # Main part
  # logging.info(f"Extracting all protein IDs and sequences from {conf.organism_protein_list}...")
  # organism_protein_list: dict = fasta.extractRecords(conf.organism_protein_list)

  # logging.info(f"Extracting all known microproteins from {conf.known_mips}")
  # known_mips: dict = fasta.extractRecords(conf.known_mips)

  ########################
  #   ARAPORT DATABASE   #
  ########################

  # Read in Araport database protein records and construct Protein objects from them
  araport_fasta_records: dict = fasta.extractRecords(conf.araport_database)

  logging.info(f"Extracting protein information from Araport FASTA headers")
  for header, sequence in araport_fasta_records.items():
    header_content: list = fasta.extractAraportHeader(header)
    protein_sequence: str = sequence
    protein_araport_tag: str = header_content[0]
    protein_sequence_version: int = int(header_content[1])
    protein_description: str = header_content[2]

    Protein(protein_sequence, protein_araport_tag, protein_sequence_version, protein_description)
  logging.info(f"Created {len(Protein.proteins)} protein entries with a unique genomic locus tag.")

  #######################
  #   STRING DATABASE   #
  #######################

  string_database = string_db.StringDB(conf)

  # Extract protein-protein interactions with a certain confidence level:
  # string_database.extractInteractions()

  # potential_mips: dict = protein.filterBySize(organism_protein_list, 1, 150)
  # potential_ancestors: dict = protein.filterBySize(organism_protein_list, 240)
  # potential_intermediaries: dict = protein.filterBySize(organism_protein_list, 151, 239)


  # Create two groups of proteins, one with those of sequence length shorter than that of 
  # conf.maximum_mip_length and the other with sequence longer than the conf.minimum_ancestor_length
  potential_mips = {}
  potential_ancestors = {}


  # fasta.createFile(potential_mips, "blast/mip_proteins.fasta")
  # fasta.createFile(potential_ancestors, "blast/ancestor_proteins.fasta")

  # blast.createDatabase("blast/ancestor_proteins.fasta", "ancestor_db")
  # blast.run("blastp -query blast/mip_proteins.fasta -db blast/ancestor_db -outfmt 7 -out mip_blast.txt")

  # interpro.processTSV()

  # print(potential_ancestors)

  # Wrap up
  end_time = datetime.datetime.now()
  time_elapsed = end_time - start_time
  logging.info(f"Finished processing all the files in {time_elapsed} seconds.")


if __name__ == "__main__":
  main()
