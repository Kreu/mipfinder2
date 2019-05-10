"""miPFinder version 2.0

WIP WIP WIP WIP
"""

import configparser
import os
import logging

#TODO: Maybe rewrite using ConfigArgParser module rather than configuration file? Not important atm
#Read configuration file (previously ArgParse CLI)

def readConfiguration(config_file):
  """Reads and verifies configuration file for miPFinder
  
  Reads in the user-defined configuration file and then verifies the parameters.

  Parameters:
    config_file: Path to the configuration file.
  
  Return:
    None

  Raises:
    ValueError
  """

  config = configparser.ConfigParser()
  config.read(config_file)

  #MIPFINDER configuration section
  protein_list = config['MIPFINDER']['protein_list']
  species_prefix = config['MIPFINDER']['species_prefix']

  #Integer
  maximum_mip_length = int(config['MIPFINDER']['maximum_mip_length'])

  #Integer
  minimum_ancestor_length = int(config['MIPFINDER']['minimum_ancestor_length'])
  blast_cutoff = float(config['MIPFINDER']['blast_cutoff'])
  overlap_cutoff = float(config['MIPFINDER']['overlap_cutoff'])
  e_value_cutoff = float(config['MIPFINDER']['e_value_cutoff'])
  c_value_cutoff = float(config['MIPFINDER']['c_value_cutoff'])

  #TODO: Rename
  mostSIMILARcutoff = config['MIPFINDER']['mostSIMILARcutoff']
  open_gap_penalty = config['MIPFINDER']['open_gap_penalty']
  maxMIPgroupSIZE = config['MIPFINDER']['maxMIPgroupSIZE']
  dropfile = config['MIPFINDER']['dropfile']

  #DATA configuration section
  hmmscan_database = config['DATA']['hmmscan_database']
  pfam_database = config['DATA']['pfam_database']
  ipfam_database = config['DATA']['ipfam_database']
  protein_gene_list = config['DATA']['protein_gene_list']
  annotation = config['DATA']['annotation']
  known_microproteins = config['DATA']['known_microproteins']

  #STRING configuration section
  STRING_database = config['STRING']['STRING_database']
  STRING_column = config['STRING']['STRING_column']
  STRING_min_score = config['STRING']['STRING_min_score']

  verifyConfiguration()

def verifyConfiguration():
  """Verifies that user configuration file has correct parameters"""

  if maximum_mip_length >= minimum_ancestor_length:
    raise ValueError(f'In {config_file}, maximum_mip_length must be smaller than the minimum_ancestor_length')
  
  # fastadbPATH = args['fastadb']
  # species = args['species']

  # ProteinGeneListName = args['ProteinGeneList']
  # if ProteinGeneListName == None:
  #   print '\nWARNING: Will not consider gene-protein relations\nRecommended: specify -p ProteinGeneList.tsv'

  # annotationdb = args['annotationdb']
  # if annotationdb == None:
  #   print '\nWARNING: Will not add protein annotations\nRecommended: specify -a AnnotationFile.tsv'

  # PfamAdbPATH = args['PfamAdb']
  # hmmscandb = args['hmmscandb']
  # if hmmscandb == None and PfamAdbPATH != None:
  #   hmmscandb = species+'_hmmscandb.txt'
  #   print '\nWARNING: Going to do a hmmscan on all proteins, that may take some time!'
  # if hmmscandb == None and PfamAdbPATH == None:
  #   print '\nWARNING: Will not add domain information\nRecommended: specify -d Pfam-database.hmm'
      
  # iPfamdbPATH = args['iPfamdb']
  # if iPfamdbPATH == None:
  #   print '\nWARNING: iPfam database not specified, will not add domain interaction information\nRecommended: specify -i iPfam-database.tsv'	
    
  # if args['STRINGdb'] == None:
  #   print '\nWARNING: STRING database not specified, will not add interaction information\nRecommended: specify -S STRING-database.txt'	





#TODO: Change back to 'config.ini' in the final version. Can't get VS Code to run the script from the subdir
readConfiguration('./mipfinder/config.ini')
