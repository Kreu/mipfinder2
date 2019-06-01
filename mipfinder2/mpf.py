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



  #####################
  #   LOGGING SETUP   #
  #####################

  logging.getLogger(__name__)
  logging.basicConfig(level=logging.DEBUG,
                      filename = 'mipfinder.log',
                      filemode = 'w',
                      format='%(asctime)s %(module)s.%(funcName)s %(levelname)-8s %(message)s',
                      datefmt = "%Y%m-%d %H:%M:%S")
  conf = config.Config('config.ini')

  ###############
  #   STARTUP   #
  ###############
  currentdir = os.path.dirname(os.path.realpath(__file__))
  sys.path.append(os.path.dirname(currentdir))
  logging.info("Starting MIPFINDER v2.0")
  logging.debug(f"Working directory is {os.getcwd()}")
  start_time = datetime.datetime.now()


  ###########################
  #   KNOWN MICROPROTEINS   #
  ###########################

  logging.info(f"Extracting all known microproteins from {conf.known_mips}")
  known_mips: dict = fasta.extractRecords(conf.known_mips)


  ########################
  #   ARAPORT DATABASE   #
  ########################

  # Read in Araport database protein records and construct Protein objects from them.
  # Araport database contains all known Arabidopsis thaliana proteins in FASTA format.
  araport_fasta_records: dict = fasta.extractRecords(conf.araport_database)

  logging.info(f"Extracting protein information from Araport FASTA headers")
  for header, sequence in araport_fasta_records.items():
    header_content: list = fasta.extractAraportHeader(header)
    protein_sequence: str = sequence
    protein_araport_tag: str = header_content[0]
    protein_sequence_version: int = int(header_content[1])
    protein_description: str = header_content[2]

    Protein(protein_sequence, protein_araport_tag, protein_sequence_version, protein_description)

  total_entries: int = sum([1 for v in Protein.proteins.values()])
  logging.info(f"Created {total_entries} unique protein entries.")



  #######################
  #   STRING DATABASE   #
  #######################

  string_database = string_db.StringDB(conf)

  # potential_mips: dict = protein.filterBySize(organism_protein_list, 1, 150)
  # potential_ancestors: dict = protein.filterBySize(organism_protein_list, 240)
  # potential_intermediaries: dict = protein.filterBySize(organism_protein_list, 151, 239)

  # Find potential interactors using the STRING database
  logging.info(f"Mapping proteins to their interaction partners using STRING database.")
  for protein_id, protein_obj in Protein.proteins.items():
    # print(f"Finding interactors for {protein_id}")
    string_database.findInteractors(protein_obj)

  #############################
  #   INTERPROSCAN DATABASE   #
  #############################




  ##########################
  #   FIND MICROPROTEINS   #
  ##########################

  # Hypothetical next steps:

  # USE INTERPROSCAN DATABASE TO ANNOTATE ALL DOMAINS IN A PROTEIN
  # THEN... 
  # single_domain_proteins = {}
  # two_domain_proteins = {}
  # all_other_proteins = {}
  # for protein_id, protein_obj in Protein.proteins.items():
  #   if protein_obj.domains == 1:
  #     single_domain_proteins[protein_id] = protein_obj
  #   else if protein_obj.domains == 2:
  #     two_domain_proteins[protein_id] = protein_obj
  #   else if protein_obj.domains > 2:
  #     all_other_proteins[protein_id] = protein_obj

  # TODO: Do this step after sorting proteins according to their domain numbers
  # small_proteins: Dict[Protein] = Protein.filterByLength(1, 150)
  # medium_proteins: Dict[Protein] = Protein.filterByLength(151, 300)
  # large_proteins: Dict[Protein] = Protein.filterByLength(301)

  # print(len(small_proteins))
  # print(len(medium_proteins))
  # print(len(large_proteins))



  # As a positive control, finally we have to make sure that we have actually found all the known
  # microproteins
  # for protein in known_microproteins:

  # Wrap up
  end_time = datetime.datetime.now()
  time_elapsed = end_time - start_time
  logging.info(f"Finished processing all the files in {time_elapsed} seconds.")


if __name__ == "__main__":
  main()
