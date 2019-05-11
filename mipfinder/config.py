import configparser
import logging
import os

logging.getLogger(__name__)

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
    """Read the configuration file for miPFinder.
    
    Raises:
      FileNotFoundError: If configuration file cannot be found.
    
    """
    if not os.path.exists(self.config_file):
      raise FileNotFoundError(f"{config_file} could not be found, aborting...")
    
    logging.info(f"Reading configuration file {self.config_file}...")
    config = configparser.ConfigParser()
    config.read(self.config_file)
    
    # MIPFINDER configuration section
    self.protein_list : str = config['MIPFINDER']['protein_list']
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
    self.hmmscan_database : str = config['DATA']['hmmscan_database']
    self.pfam_database : str = config['DATA']['pfam_database']
    self.ipfam_database : str = config['DATA']['ipfam_database']
    self.protein_gene_list : str = config['DATA']['protein_gene_list']
    self.annotation : str = config['DATA']['annotation']
    self.known_microproteins : str = config['DATA']['known_microproteins']

    # PATHS configuration section
    self.blast_path : str = config['PATHS']['blast_path']
    self.clustal_path : str = config['PATHS']['clustal_path']
    self.hmmsearch_path : str = config['PATHS']['hmmsearch_path']

    # STRING configuration section
    self.string_database : str = config['STRING']['STRING_database']
    self.string_column : str = config['STRING']['STRING_column']
    self.string_min_score : str = config['STRING']['STRING_min_score']

  def _verifyConfiguration(self):
    """Verify that user configuration file has correct parameters.
    
    Raises:
      ValueError: If, in configuration file `maximum_mip_length` is larger or equal to `minimum_ancestor_length`.

    """
    logging.info("Verifying configuration file...")
    if self.maximum_mip_length >= self.minimum_ancestor_length:
      logging.info(f"In {self.config_file}, maximum_mip_length must be smaller than the minimum_ancestor_length.")
      raise ValueError(f"In {self.config_file}, maximum_mip_length must be smaller than the minimum_ancestor_length.")

    if not self.protein_gene_list:
      logging.info(f"Warning: protein_gene_list parameter is not set in {self.config_file}. Will not consider gene-protein relations.")

    if not self.annotation:
      logging.info(f"Warning: annotation parameter is not set in {self.config_file}. Will not add protein annotations.")

    if not self.ipfam_database:
      logging.info(f"Warning: ipfam_database parameter is not set in {self.config_file}. Will not add domain interaction information.")

    if not self.string_database:
      logging.info(f"Warning: string_database parameter is not set in {self.config_file}. Will not add interaction information.")

    # TODO: Check whether these two logical conditions can be simplified
    if not self.hmmscan_database and self.pfam_database:
      self.hmmscan_database = self.species_prefix + "_hmmscan_database.txt"
      logging.info("Warning: hmmscan is being performed on all proteins. This can take a long time.")

    if not self.hmmscan_database and not self.pfam_database:
      logging.info(f"Warning: pfam_database parameter is not set in {self.config_file}. Will not add domain information.")
