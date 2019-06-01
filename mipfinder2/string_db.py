from __future__ import annotations

import logging
from typing import Dict, List, Type
import pathlib
import re

import config
import fasta

class StringDB(object):

  def __init__(self, conf: Config):
    """StringDB class provides a set of functions to extract and process data from STRING databases.
    
    Attributes:
      _conf = Copy of the configuration file object
      _id_table (Dict[str, List[str]]): A dictionary that maps genomic locus tags to UniProt 
          accession names.
    
    """
    # Local copy of the configuration object. This is required by many private member functions.
    self._conf = conf

    # Contains all known protein-protein interactions from the STRING database. Both the keys and
    # the list of values contain unique protein IDs in the following format:
    # GENOMICS_LOCUS_TAG.SEQUENCE_VERSION Keys are Araport 
    self._protein_interactions: Dict[str, List[str]] = {}

    # The initialisation logic is as follows:
    #   Read in the database file and extract all genomic locus tags for protein-protein interactions
    #   with a score above a set threshold. This threshold is set in the configuration file as the
    #   `string_cutoff` variable. 
    #   Create an interaction table where the keys are protein genomic locus tags and values are
    #   all the other protein genomic locus tags that the protein interacts with.
    self._protein_interactions = self._extractInteractionsFromDatabase()
    print(_protein_interactions)

  @property
  def conf(self):
    return self._conf

  @property
  def protein_interactions(self):
    return self._protein_interactions

  # def toUniprot(self, genomic_locus_tag: str) -> str:
  #   """Takes a STRING database genomic locus tag and returns the UniProt equivalent.
    
  #   Raises:
  #     KeyError: If the STRING genomic locus tag cannot be mapped to a unique Uniprot ID
      
  #   """
  #   return self._id_table[genomic_locus_tag]

  def _extractInteractionsFromDatabase(self) -> Dict[str, List[str]]:
    """Extracts protein-protein interaction information from the STRING database.

    Extracts the genomic locus tags of all interacting proteins with a cutoff value that is
    specified in config.ini file as the `string_cutoff` variable.

    Interactions are duplicated, i.e. if protein 1 interacts with protein 2 and protein 3;
    and protein 2 interacts with protein 1 but not 3, it is
    represented as a {"1": ["2", "3"]} and as {"2": ["1"]} key-value pairs.

    Returns:
      A dictionary containing the protein's unique ID (consisting of Araport genomic locus tag and 
      sequence version) as keys and a list of unique IDs as values. This list contains all proteins
      that interact with the given domain according to SRING database.

    """
    # An example of STRING database format is below:
    # protein1 protein2 neighborhood fusion cooccurence coexpression experimental database textmining combined_score
    # 3702.AT1G01010.1 3702.AT1G10570.1 0 0 0 165 0 0 0 165
    # 3702.AT1G01010.1 3702.AT1G06149.1 0 0 0 0 0 0 865 86

    # The score in the database is the same as on the STRING website but multiplied by a 1000, e.g. a
    # score of 0.954 on the STRING website is 954 in the database file. The scores range from 0 to 1000. 
    # The score indicates the probability of an interaction, e.g. a score of 500 means that every second 
    # interaction is possibly erroneous.

    logging.info(f"Extracting STRING database protein interaction data from {self._conf.string_database} "
                 f"with a cutoff score of {self._conf.string_cutoff}.")

    string_protein_interactions: Dict[str, List[str]] = {}
    with open(self._conf.string_database, 'r') as f:
      next(f) # Ignore the header line
      for line in f:
        tokens: list = line.strip('\n').split(' ')

        # Check the interaction score before starting to split the time to save CPU cycles.
        interaction_score: int = int(tokens[9])
        if interaction_score < self._conf.string_cutoff:
          continue

        # After the initial split extract the protein 1 and protein 2 information in the following 
        # format:
        # TAXONOMIC_ID.GENOMIC_LOCUS_TAG.VERSION_NUMBER 
        protein_id_data = tokens[0]
        interacting_protein_id_data = tokens[1]

        # We then split that to extract locus tag and version number by splitting it into three
        # tokens (TAXONOMIC_ID, GENOMIC_LOCUS_TAG and VERSION_NUMBER)
        protein_locus_tag: str = (protein_id_data.split('.'))[1]
        protein_version_nr: str = (protein_id_data.split('.'))[2]
        interacting_protein_locus_tag: str = (interacting_protein_id_data.split('.'))[1]
        interacting_protein_version_nr: str = (interacting_protein_id_data.split('.'))[2]

        first_protein_unique_id = protein_locus_tag + "." + protein_version_nr
        interacting_protein_unique_id = interacting_protein_locus_tag + "." + interacting_protein_version_nr

        if first_protein_unique_id not in string_protein_interactions:
          string_protein_interactions[first_protein_unique_id] = [interacting_protein_unique_id]
        else:
          string_protein_interactions[first_protein_unique_id].append(interacting_protein_unique_id)

    logging.info(f"Extracted {len(self._protein_interactions)} protein-protein interactions from {self._conf.string_database}.") 
    return string_protein_interactions

  def findInteractors(self, protein_unique_id: str) -> List[str]:
    """Finds all interactors of a given protein.

    Finds all interactions in the STRING database for the specified protein unique ID.
    
    Returns:
      A list of unique IDs of the interacting proteins.
      
    """
    if protein_unique_id in self._protein_interactions:
      # print(f"Found interactors for {protein_obj.unique_id}")
      # print(f"All known interactors are: {self._protein_interactions[protein_obj.unique_id]}")
      return self._protein_interactions[protein_unique_id]

  def stringToUniprot(string_id: str) -> List[str]:
    """Takes a STRING ID and returns all corresponding UniProt accession numbers.

    Args:
      string_id: STRING ID in the following format: `GENOMIC_LOCUS_TAG.SEQUENCE_VERSION`.

    Returns:
      A list of corresponding UniProt accession names.

    """

    string_to_id_conversion: Dict[str, List[str]] = self._readUniprotConversionTable()


  def _readUniprotConversionTable(self) -> Dict[str, List[str]]:
    # TODO: This uses the raw STRING alias file but internally it should use the conversion file
    # that has been created after the STRING file has been parsed. This will save processing time
    # as we don't have to reparse the million+ lines every time.
    """Read in a STRING ID to Uniprot accession number conversion table
    
    It incorporates the STRING, TAIR, and manually curated databases because the STRING protein
    alias file is incomplete and results in a lot of missing values. The necessary files for this
    function are set in config.ini as `string_protein_aliases`, tair_protein_aliases` and
    `curated_protein_aliases`.
    
    This function is similar to _extractStringAliases() except that it incorporates three different
    databases to map all STRING IDs to 

    See readme for more details. 

    Returns:
      A dictionary containing the unique protein IDs as the keys and all the corresponding UniProt
      accession names as a list of values. One unique protein ID can have multiple accession names
      associated with it due to some names being deprecated etc in the UniProt database.

    """
    logging.info(f"Creating a table that maps unique protein IDs to UniProt accession codes.")

    # Before we call the costly operation of extracting the Uniprot accession numbers from the
    # STRING alias database and create a conversion file, check whether the conversion file 
    # (`string_id_to_uniprot`) already exists.
    self._ensureConversionTableExists()

    database_files = [self._conf.string_id_to_uniprot,
                      self._conf.tair_protein_aliases, 
                      self._conf.curated_protein_aliases]

    conversion_table: Dict[str, List[str]] = {}
    # All three files (STRING, TAIR and manually curated databases) come in a tsv format where the
    # first column is the UniProt accession name and the second column is the genomic locus tag.
    for filename in database_files:
      with open(filename, 'r') as f:
        logging.info(f"Processing {filename}...")
        for line in f:
          tokens: list = line.strip('\n').split('\t')
          uniprot_id: str = tokens[0]
          genomic_locus_tag: str = tokens[1]

        if genomic_locus_tag not in id_table:
          id_table[genomic_locus_tag] = [u.niprot_id]
        else:
          if uniprot_id in id_table[genomic_locus_tag]:  # Don't append same ID twice to the list
            continue
          else:
            id_table[genomic_locus_tag].append(uniprot_id)

    logging.info(f"Finished mapping genomic locus tags to UniProt accession names.")
    return id_table

  def _ensureConversionTableExists(self):
    """Makes sure a STRING ID to UniProt ID conversion table exists.

    The conversion table location is set within the `string_id_to_uniprot` variable in the
    configuration file. If the file does not exist, it creates the conversion file. If the file
    already exists, it prompts the user whether they want to recreate it.

    """
    if pathlib.Path(self._conf.string_id_to_uniprot).exists():
      answer = input("STRING to UniProt conversion file already exists, do you "
                    "want to reprocess STRING protein aliases file (This may "
                    "take some time)? Y/N ")
      if answer == 'Y' or answer == 'y':
        logging.info(f"Reprocessing STRING to UniProt alias file.")
        string_aliases: dict = self._extractStringAliases()
        self._writeStringAliases(string_aliases)

    if not pathlib.Path(self._conf.string_id_to_uniprot).exists():
      # If the file does not exist, either the variable has not been set or the variable points to
      # an invalid path. Either way the a default file needs to be created and the variable needs to
      # be updated
      default = "data/string_id_to_uniprot.txt"
      logging.info(f"{self._conf.string_id_to_uniprot} does not point to a valid file, setting"
                   f"string_id_to_uniprot variable in {self._conf.config_file} to {default}.")
      self._conf.string_id_to_uniprot = default

      string_aliases: dict = self._extractStringAliases()
      self._writeStringAliases(string_aliases)

  def _extractStringAliases(self) -> Dict[str, List[str]]: 
    """Extracts STRING IDs from STRING alias file and maps them to UniProt IDs. 

    This uses an organism-specific file from STRING database from here:
    https://string-db.org/cgi/download.pl?sessionId=QSuugpq1Ea5l&species_text=Arabidopsis+thaliana

    Specifically, this one:
    3702.protein.info.v11.0.txt.gz (2.4 Mb) - list of STRING proteins incl. their display names and
    descriptions

    Returns:
      A dictionary containg unique protein IDs as keys and corresponding UniProt accession
      names as a list.

    """
    string_to_uniprot_conversion = {}
    with open(self._conf.string_protein_aliases) as f:
      logging.info(f"Extracting STRING genomic locus tags and their corresponding UniProt "
                   f"accession names from {self._conf.string_protein_aliases}")
      # This is the regex from UniProt website to find any accession code in their database
      uniprot_regex_1 = re.compile("[OPQ][0-9][A-Z0-9]{3}[0-9]")
      uniprot_regex_2 = re.compile("[A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9]")
      uniprot_regex_3 = re.compile("[A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9][A-Z][A-Z0-9]{2}[0-9]")

      # We only want accession codes from lines with UniProt_AC annotation as these contain the
      # IDs that correspond to BLAST and UniProt databases. 
      uniprot_database_name = re.compile("BLAST_UniProt_AC", re.IGNORECASE)
      for line in f:
        # Matching the regex isn't enough because it will also pick up other codes from different databases.
        # We need to explicitly check whether the identifier is from UniProt_AC database.
        if (uniprot_regex_1.search(line) != None or 
            uniprot_regex_2.search(line) != None or 
            uniprot_regex_3.search(line) != None) \
            and uniprot_database_name.search(line) != None:
          tokens = line.split('\t')

          # The first column in the protein aliases file is always the STRING ID in the following
          # format:
          # # xxxx.GENOMIC_LOCUS_TAG.SEQUENCE_VERSION
          string_alias = tokens[0]
          #Split xxxx.GENOMIC_LOCUS_TAG.SEQUENCE_VERSION into tokens and extract the unique ID made up 
          # of GENOMIC_LOCUS_TAG and SEQUENCE_VERSION.
          string_alias_tokens = string_alias.split('.')
          unique_id = string_alias_tokens[1] + '.' + string_alias_tokens[2] 

          uniprot_alias = tokens[1]

          if unique_id not in string_to_uniprot_conversion:
            string_to_uniprot_conversion[unique_id] = [uniprot_alias]
          else:
            string_to_uniprot_conversion[unique_id].append(uniprot_alias)

    logging.info(f"Finished extracting STRING genomic locus tags from {self._conf.string_protein_aliases}")
    return string_to_uniprot_conversion

  def _writeStringAliases(self, string_aliases):
    # ID mapping data comes from _extractStringAliases where keys are STRING IDs and values are a list of
    # UniProt IDs
    # TODO: What happens if the variable is not set?
    logging.info(f"Writing STRING to UniProt ID conversion file into {self._conf.string_to_uniprot}")
    with open(self._conf.string_to_uniprot, 'w') as f:
      for string_id, uniprot_id_list in string_aliases.items():
        for uniprot_id in uniprot_id_list:
          # To comply with the external databases, UniProt accession names must come first
          f.write(f"{uniprot_id}\t{string_id}\n")
