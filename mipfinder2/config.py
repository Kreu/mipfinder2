import configparser
import logging
import os
import apt

class Config:
  """Class to read in and verify the configuration file for miPFinder.
  
  Ensures that the configuration file is correctly read and that the parameters
  have been set appropriately.

  Args:
    config_file (str): Path to the mipfinder configuration file 

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
    
    # DATA configuration section
    self.organism_protein_fasta : str = config['DATA']['organism_protein_fasta']

    # STRING configuration section
    self.string_database: str = config['STRING']['string_database']
    self.string_protein_info: str = config['STRING']['string_protein_info']


  def _verifyConfiguration(self):
    """Verify that user configuration file has correct parameter."""
    logging.info("Verifying configuration file...")

    ##########################
    #   REQUIRED VARIABLES   #
    ##########################

    _fileExists(self.organism_protein_fasta)
    _fileExists(self.string_database)
    _fileExists(self.string_protein_info)
    logging.info("All required dependencies detected.") 

    ##########################
    #   OPTIONAL VARIABLES   #
    ##########################



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
