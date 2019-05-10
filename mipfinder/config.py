import configparser
import logging

logging.getLogger(__name__)


class Config:
  """Test for doc"""

  def __init__(self, config_file):
    self.config_file = config_file
    self.readConfiguration(config_file)
    self.verifyConfiguration()

  def readConfiguration(self, config_file):
    """Reads and verifies configuration file for miPFinder

    Reads in the user-defined configuration file and then verifies the parameters.

    Parameters:
      config_file: Path to the configuration file.

    Return:
      None

    Raises:
    """

    logging.info("Reading configuration file...")
    config = configparser.ConfigParser()
    config.read(config_file)

    # MIPFINDER configuration section
    self.protein_list = config['MIPFINDER']['protein_list']
    self.species_prefix = config['MIPFINDER']['species_prefix']
    self.maximum_mip_length = int(config['MIPFINDER']['maximum_mip_length'])
    self.minimum_ancestor_length = int(config['MIPFINDER']['minimum_ancestor_length'])
    self.blast_cutoff = float(config['MIPFINDER']['blast_cutoff'])
    self.overlap_cutoff = float(config['MIPFINDER']['overlap_cutoff'])
    self.e_value_cutoff = float(config['MIPFINDER']['e_value_cutoff'])
    self.c_value_cutoff = float(config['MIPFINDER']['c_value_cutoff'])

    # TODO: Rename
    self.mostSIMILARcutoff = config['MIPFINDER']['mostSIMILARcutoff']
    self.open_gap_penalty = config['MIPFINDER']['open_gap_penalty']
    self.maxMIPgroupSIZE = config['MIPFINDER']['maxMIPgroupSIZE']
    self.dropfile = config['MIPFINDER']['dropfile']

    # DATA configuration section
    self.hmmscan_database = config['DATA']['hmmscan_database']
    self.pfam_database = config['DATA']['pfam_database']
    self.ipfam_database = config['DATA']['ipfam_database']
    self.protein_gene_list = config['DATA']['protein_gene_list']
    self.annotation = config['DATA']['annotation']
    self.known_microproteins = config['DATA']['known_microproteins']

    # STRING configuration section
    self.string_database = config['STRING']['STRING_database']
    self.string_column = config['STRING']['STRING_column']
    self.string_min_score = config['STRING']['STRING_min_score']

  def verifyConfiguration(self):
    """Verifies that user configuration file has correct parameters"""

    logging.info("Verifying configuration file...")
    if self.maximum_mip_length >= self.minimum_ancestor_length:
      logging.info(f'In {self.config_file}, maximum_mip_length must be smaller than the minimum_ancestor_length.')
      raise ValueError(f'In {self.config_file}, maximum_mip_length must be smaller than the minimum_ancestor_length.')

    if not self.protein_gene_list:
      logging.info(f'Warning: protein_gene_list parameter is not set in {self.config_file}. Will not consider gene-protein relations.')

    if not self.annotation:
      logging.info(f'Warning: annotation parameter is not set in {self.config_file}. Will not add protein annotations.')

    if not self.ipfam_database:
      logging.info(f'warning: ipfam_database parameter is not set in {self.config_file}. Will not add domain interaction information.')

    if not self.string_database:
      logging.info(f'Warning: string_database parameter is not set in {self.config_file}. Will not add interaction information.')

    # TODO: Check whether these two logical conditions can be simplified
    if not self.hmmscan_database and self.pfam_database:
      self.hmmscan_database = self.species_prefix + "_hmmscan_database.txt"
      logging.info("Warning: hmmscan is being performed on all proteins. This can take a long time.")
    if not self.hmmscan_database and not self.pfam_database:
      logging.info(f'Warning: pfam_database parameter is not set in {self.config_file}. Will not add domain information.')
