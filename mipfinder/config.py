import configparser


class Config:
  """Test for doc"""

  def __init__(self, config_file):
    self.config_file = config_file
    self.read_configuration(config_file)

  def read_configuration(self, config_file):
    """Reads and verifies configuration file for miPFinder
    
    Reads in the user-defined configuration file and then verifies the parameters.

    Parameters:
      config_file: Path to the configuration file.
    
    Return:
      None

    Raises:
    """

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

    self.verify_configuration()

  def verify_configuration(self):
    """Verifies that user configuration file has correct parameters"""

    if self.maximum_mip_length >= self.minimum_ancestor_length:
      raise ValueError(f'In {self.config_file}, maximum_mip_length must be smaller than the minimum_ancestor_length')
    
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