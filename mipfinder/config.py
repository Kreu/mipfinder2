import configparser
import logging
import os
import apt

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
    self.protein_list : str = config['DATA']['protein_list']
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
    self.hmmbuild_path : str = config['PATHS']['hmmbuild_path']
    self.hmmscan_path : str = config['PATHS']['hmmscan_path']

    # STRING configuration section
    self.string_database : str = config['STRING']['STRING_database']
    self.string_column : str = config['STRING']['STRING_column']
    self.string_min_score : str = config['STRING']['STRING_min_score']

  def _verifyConfiguration(self):
    """Verify that user configuration file has correct parameters.
    hmmer
    Raises:
      ValueError: If, in configuration file `maximum_mip_length` is larger or equal to 
                  `minimum_ancestor_length`.

    """
    logging.info("Verifying configuration file...")



    # TODO (11/05/2018, Valdeko): See which variables are optional and which are absolutely and do
    # checking based on that
    # ######ARGUMENT PARSER & VERIFICATION
    # os.environ["CYGWIN"] = "nodosfilewarning" #avoid hmmer warnings
    # currentPATH = os.getcwd().replace('\\','/')

    ##########################
    #   REQUIRED VARIABLES   #
    ##########################

    # Check whether all programs (clustalw2, hmmscan etc) are present on the system
    # TODO: REENABLE CHECKS ONCE THEY ARE INSTALLED
    # _fileExists(self.hmmbuild_path)
    # _fileExists(self.hmmscan_path)
    # _fileExists(self.hmmsearch_path)
    # _fileExists(self.clustal_path)

    # # TODO (12/05/2019, Valdeko): blast_path should point to an executable, not a folder...
    # if not os.path.exists(self.blast_path):
    #   logging.error(f"{self.blast_path} does not refer to a valid file location, aborting...")
    #   raise FileNotFoundError(f"{self.blast_path} does not refer to a valid file location, aborting...")

    # logging.info("All dependencdies detected.") 
    
    ##########################
    #   OPTIONAL VARIABLES   #
    ##########################

    if self.maximum_mip_length >= self.minimum_ancestor_length:
      logging.error(f"In {self.config_file}, maximum_mip_length must be smaller than the minimum_ancestor_length.")
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


# Helper functions for Config class

def _fileExists(filename: str):
  """Check whether file exists.

  Helper function to check whether file exists, with incorporated logging.

  Raises:
    FileNotFoundError: If file cannot be found.

  """
  if not os.path.isfile(filename):
    logging.error(f"{filename} does not refer to a valid file location, aborting...")
    raise FileNotFoundError(f"{filename} does not refer to a valid file location, aborting...")

def _packageInstalled(package_name: str):
  """Check whether a package is installed on the system.

  Raises:
    FileNotFoundError: If a given package is not installed.

  """
  cache = apt.Cache()
  if cache[package_name].is_installed:
    logging.info(f"{package_name} installation detected")
  else:
    logging.error(f"{package_name} installation not detected, aborting...")
    raise FileNotFoundError(f"{package_name} installation not detected, aborting...")