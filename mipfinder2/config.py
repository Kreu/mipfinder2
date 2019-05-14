import configparser
import logging
import os
import apt

class Config:
  """Class to read in and verify the configuration file for miPFinder.
  
  Ensures that the configuration file is correctly read and that the parameters
  have been set appropriately.

  Args:
    config_file (str): Path to the miPFinder configuration file 

  Raises:
    ValueError: If, in configuration file `maximum_mip_length` is larger or equal to `minimum_ancestor_length`.

  """

  def __init__(self, config_file: str):
    self.config_file = config_file
    self._readConfiguration()
    self._verifyConfiguration()

  def _readConfiguration(self):
    """Read the configuration file for miPFinder."""
    _fileExists(self.config_file)
    logging.info(f"Reading configuration file ({self.config_file})...")
    config = configparser.ConfigParser()
    config.read(self.config_file)
    
    # MIPFINDER configuration section
    self.species_prefix : str = config['MIPFINDER']['species_prefix']
    self.maximum_mip_length : int = int(config['MIPFINDER']['maximum_mip_length'])
    self.minimum_ancestor_length : int = int(config['MIPFINDER']['minimum_ancestor_length'])
    self.blast_cutoff : float = float(config['MIPFINDER']['blast_cutoff'])
    self.overlap_cutoff : float = float(config['MIPFINDER']['overlap_cutoff'])
    self.e_value_cutoff : float = float(config['MIPFINDER']['e_value_cutoff'])
    self.c_value_cutoff : float = float(config['MIPFINDER']['c_value_cutoff'])

    # TODO: Rename these files
    self.mostSIMILARcutoff : str = config['MIPFINDER']['mostSIMILARcutoff']
    self.open_gap_penalty : str = config['MIPFINDER']['open_gap_penalty']
    self.maxMIPgroupSIZE : int  = int(config['MIPFINDER']['maxMIPgroupSIZE'])
    self.dropfile : str = config['MIPFINDER']['dropfile']

    # DATA configuration section
    self.organism_protein_list : str = config['DATA']['organism_protein_list']
    self.hmmscan_database : str = config['DATA']['hmmscan_database']
    self.pfam_database : str = config['DATA']['pfam_database']
    self.ipfam_database : str = config['DATA']['ipfam_database']
    self.protein_gene_list : str = config['DATA']['protein_gene_list']
    self.annotation_file : str = config['DATA']['annotation_file']
    self.known_microproteins : str = config['DATA']['known_microproteins']

    # PATH configuration section
    self.blast_path : str = config['PATH']['blast_path']
    self.clustalo_path : str = config['PATH']['clustalo_path']
    self.hmmsearch_path : str = config['PATH']['hmmsearch_path']
    self.hmmbuild_path : str = config['PATH']['hmmbuild_path']
    self.hmmscan_path : str = config['PATH']['hmmscan_path']

    # STRING configuration section
    self.STRING_database : str = config['STRING']['STRING_database']
    self.STRING_column : str = config['STRING']['STRING_column']
    self.STRING_min_score : str = config['STRING']['STRING_min_score']

  def _verifyConfiguration(self):
    """Verify that user configuration file has correct parameters.
    
    Raises:
      ValueError: If, in configuration file `maximum_mip_length` is larger or equal to 
                  `minimum_ancestor_length`.

    """
    logging.info("Verifying configuration file...")

    ##########################
    #   REQUIRED VARIABLES   #
    ##########################

    _fileExists(self.hmmbuild_path)
    _fileExists(self.hmmscan_path)
    _fileExists(self.hmmsearch_path)
    _fileExists(self.clustalo_path)
    _fileExists(self.organism_protein_list)
    logging.info("All required dependencies detected.") 

    ##########################
    #   OPTIONAL VARIABLES   #
    ##########################

    # TODO (14/05/2019): Verify that set optional variables actually point to valid files!
    if self.maximum_mip_length >= self.minimum_ancestor_length:
      logging.error(f"In {self.config_file}, maximum_mip_length must be smaller than the minimum_ancestor_length.")
      raise ValueError(f"In {self.config_file}, maximum_mip_length must be smaller than the minimum_ancestor_length.")

    if self.protein_gene_list:
      _fileExists(self.protein_gene_list)
    else:
      logging.info(f"Warning: protein_gene_list parameter is not set in {self.config_file}. Will not consider gene-protein relations.")

    if self.annotation_file:
      _fileExists(self.annotation_file)
    else:
      logging.info(f"Warning: annotation_file parameter is not set in {self.config_file}. Will not add protein annotations.")

    if self.ipfam_database:
      _fileExists(self.ipfam_database)
    else:
      logging.info(f"Warning: ipfam_database parameter is not set in {self.config_file}. Will not add domain interaction information.")

    if self.STRING_database:
      _fileExists(self.STRING_database)
    else:
      logging.info(f"Warning: string_database parameter is not set in {self.config_file}. Will not add interaction information.")

    # TODO: Check whether these two logical conditions can be simplified
    if not self.hmmscan_database and self.pfam_database:
      self.hmmscan_database = self.species_prefix + "_hmmscan_database.txt"
      logging.info("Warning: hmmscan is being performed on all proteins. This can take a long time.")

    if not self.hmmscan_database and not self.pfam_database:
      logging.info(f"Warning: pfam_database parameter is not set in {self.config_file}. Will not add domain information.")


# Helper functions for Config class

def _fileExists(filename: str):
  """Check whether file exists.

  Helper function to check whether file exists, with incorporated logging.

  Raises:
    FileNotFoundError: If file cannot be found.

  """
  if os.path.isfile(filename):
    logging.info(f"{filename} found.")

  if not os.path.isfile(filename):
    logging.error(f"{filename} does not refer to a valid file location, aborting...")
    raise FileNotFoundError(f"{filename} does not refer to a valid file location, aborting...")
