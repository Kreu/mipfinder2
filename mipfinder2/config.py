import configparser
import logging
import os

class Config:
  """Class to read in and verify the configuration file for miPFinder.
  
  Ensures that the configuration file is correctly read and that the required parameters have been
  set correctly. Optional parameters are not checked; it is up to the calling function using
  optional parameters to ensure they point to a valid file.

  Attributes:
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
    self.organism_protein_list: str = config['DATA']['organism_protein_list']  # Required
    self.known_mips: str = config['DATA']['known_mips']  # Required

    # STRING configuration section
    self.string_database: str = config['STRING']['string_database']  # Required
    self.string_protein_aliases: str = config['STRING']['string_protein_aliases']  # Required
    self.string_to_uniprot: str = config['STRING']['string_to_uniprot']

    # TAIR configuration section
    self.tair_protein_aliases: str = config['TAIR']['tair_protein_aliases']  # Required 

    # ARAPORT configuration section
    self.araport_database: str = config['ARAPORT']['araport_database']

    # OTHER configuration section
    self.curated_protein_aliases: str = config['OTHER']['curated_protein_aliases']

  def _verifyConfiguration(self):
    """Verify that user configuration file has the correct parameters."""
    logging.info("Verifying configuration file parameters...")

    ##########################
    #   REQUIRED VARIABLES   #
    ##########################

    _fileExists(self.organism_protein_list)
    _fileExists(self.known_mips)

    _fileExists(self.string_database)
    _fileExists(self.string_protein_aliases)

    _fileExists(self.tair_protein_aliases)

    logging.info("All required dependencies detected.") 

    ##########################
    #   OPTIONAL VARIABLES   #
    ##########################
  
    # As per Config class API, optional variables are not checked. 


# Helper functions for Config class
def _fileExists(filename: str):
  """Check whether file exists.

  Helper function to check whether file exists, with incorporated logging.

  Raises:
    FileNotFoundError: If file cannot be found.

  """
  # TODO: Rewrite using pathlib.
  if os.path.isfile(filename):
    logging.info(f"{filename} found.")

  if not os.path.isfile(filename):
    logging.error(f"{filename} does not refer to a valid file location, aborting...")
    raise FileNotFoundError(f"{filename} does not refer to a valid file location, aborting...")
