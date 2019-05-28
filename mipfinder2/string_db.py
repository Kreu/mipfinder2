import logging
from typing import Dict, List, Type
import pathlib
import re

import config

class StringDB(object):

  def __init__(self, conf: Type[config.Config]):
    """StringDB class provides a set of functions to extract and process data from STRING databases.
    
    Attributes:
      _conf = Copy of the configuration file object
      _id_table (Dict[str, List[str]]): A dictionary that maps genomic locus tags to UniProt 
          accession names.
    
    """
    self._conf = conf
    self._id_table: Dict[str, List[str]]  = {}

    if pathlib.Path(self._conf.string_to_uniprot).exists():
      answer = input("STRING to UniProt alias file already exists, do you "
                    "want to reprocess STRING protein aliases file (This may "
                    "take some time)? Y/N ")
      if answer == 'Y' or answer == 'y':
        logging.info(f"Reprocessing STRING to UniProt alias file.")
        string_to_uniprot_ids: dict = self._extractStringAliases()
        self._writeStringAliases(string_to_uniprot_ids)

    if not pathlib.Path(self._conf.string_to_uniprot).exists():
      # If the file does not exist, either the variable has not been set or the variable points to
      # an invalid path. Either way the a default file needs to be created and the variable needs to
      # be updated
      default = "data/string_to_uniprot.txt"
      logging.info(f"{self._conf.string_to_uniprot} does not point to a valid file, setting"
                   f"string_to_uniprot variable in {self._conf.config_file} to {default}.")
      self._conf.string_to_uniprot = default

      string_to_uniprot_ids: dict = self._extractStringAliases()
      # Write the contents to a table so there is no need to parse >1 million lines every time the
      # script is run
      self._writeStringAliases(string_to_uniprot_ids)

    # Regardless of whether the STRING aliases were extracted again or for the first time, 
    # _createIdTable() needs to be run for StringDB class to function properly.
    self._createIdTable()

  def toUniprot(self, genomic_locus_tag: str) -> str:
    """Takes a STRING database genomic locus tag and returns the UniProt equivalent.
    
    Raises:
      KeyError: If the STRING genomic locus tag cannot be mapped to a unique Uniprot ID
      
    """
    return self._id_table[genomic_locus_tag]

  def extractInteractions(self, score_cutoff: int=700, delimiter: str=' ', format="UNIPROT") -> Dict[str, List[str]]:
    """Extracts protein-protein interaction information from the STRING database.

    Args:
      score_cutoff: Exclude all protein-protein interactions below this threshold.
      delimiter: Character by which to split values into separate tokens. Defaults to space (' ')
      format: Output format of protein accession codes. Defauls to `UNIPROT`.
          Other possible format is `STRING`.

    Returns:
      If `format=UNIPROT`, returns a dictionary containing UniProt accession numbers as keys and
      list of UniProt accession numbers as values. This list contains the accession numbers of all
      proteins that interact with the given domain, according to SRING database.

      If `format=STRING`, returns the same dictionary but instead of UniProt accession numbers the
      keys and values contain genomic locus tag.

      Interactions are duplicated, i.e. if protein 1 interacts with protein 2 and protein 3;
      and protein 2 interacts with protein 1 but not 3, it is
      represented as a {"1": ["2", "3"]} and as {"2": ["1"]} key-value pairs.

    """
    # An example of STRING database format is below:
    # protein1 protein2 neighborhood fusion cooccurence coexpression experimental database textmining combined_score
    # 3702.AT1G01010.1 3702.AT1G10570.1 0 0 0 165 0 0 0 165
    # 3702.AT1G01010.1 3702.AT1G06149.1 0 0 0 0 0 0 865 86

    # The score in the database is the same as on the STRING website but multiplied by a 1000, e.g. a
    # score of 0.954 on the STRING website is 954 in the database file. The scores range from 0 to 1000. 
    # The score indicates the probability of an interaction, e.g. a score of 500 means that every second 
    # interaction is possibly erroneous.
    logging.info(f"Extracting STRING database protein interaction data from {self._conf.string_database}.")
    protein_interactions: dict = {}

    with open(self._conf.string_database, 'r') as f:
      next(f) # Ignore the header line
      for line in f:
        line = line.strip('\n') # Interferes with processing
        tokens: list = line.split(delimiter)
        interaction_score: int = int(tokens[9])
        if interaction_score < score_cutoff:
          continue

        # All STRING aliases in an organism database are suffixed with the
        # NCBI taxonomic identifier in the following format:
        # xxxx.GENE_IDENTIFIER.ISOFORM	
        # We are only interested in the protein ID so we need to split the 
        # organism identifier.
        first_protein: str = tokens[0]
        second_protein: str = tokens[1]

        #Split xxxx.GENE_IDENTIFIER.ISOFORM into tokens and retain the GENE_IDENTIFIER
        first_protein = (first_protein.split('.'))[1]  # These will be STRING database IDs
        second_protein = (second_protein.split('.'))[1]  # These will be STRING database IDs

        if format == "STRING":
          if first_protein in protein_interactions:
            protein_interactions[first_protein].append(second_protein)
          else:
            protein_interactions[first_protein] = [second_protein]

        if format == "UNIPROT":
          try:
            if first_protein in protein_interactions:
              protein_interactions[first_protein].append(self.toUniprot(second_protein))
            else:
              protein_interactions[first_protein] = [self.toUniprot(second_protein)]
          except KeyError:
            logging.warning(f"Could not find a UniProt accession code equivalent to STRING ID {second_protein}")

    logging.info(f"Extracted {len(protein_interactions)} protein-protein interactions from {self._conf.string_database}.") 

  def _createIdTable(self):
    """Creates a table that maps genomic locus tags to UniProt IDs.
    
    It incorporates the STRING, TAIR, and manually curated databases because the STRING protein
    alias file is incomplete and results in a lot of missing values. The necessary files for this
    function are set in config.ini as `string_to_uniprot`, `tair_protein_aliases` and
    `curate_protein_aliases`.
    
    Requires that all the STRING IDs have been extracted from the STRING protein alias list before
    running this function.

    See readme for more details. 

    Returns:
      A dictionary containing the genomic locus tag as the keys and all the corresponding UniProt
      accession names as a list of values. One genomic locus tag can have multiple accession names
      associated with it due to some names being deprecated etc in the UniProt database.

    """
    logging.info(f"Creating a table that maps genomics locus tags to UniProt accession codes.")
    database_files = [self._conf.string_to_uniprot,  # STRING protein aliases
                      self._conf.tair_protein_aliases, 
                      self._conf.curated_protein_aliases]

    id_table: dict = {}

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
          id_table[genomic_locus_tag] = [uniprot_id]
        else:
          if uniprot_id in id_table[genomic_locus_tag]:  # Don't append same ID twice to the list
            continue
          else:
            id_table[genomic_locus_tag].append(uniprot_id)

    logging.info(f"Finished mapping genomic locus tags to UniProt accession names.")
    return id_table

  def _extractStringAliases(self) -> Dict[str, List[str]]: 
    """Extracts STRING IDs from STRING alias file and maps them to UniProt IDs. 

    This uses an organism-specific file from STRING database from here:
    https://string-db.org/cgi/download.pl?sessionId=QSuugpq1Ea5l&species_text=Arabidopsis+thaliana

    Specifically, this one:
    3702.protein.info.v11.0.txt.gz (2.4 Mb) - list of STRING proteins incl. their display names and
    descriptions

    Creates a file whose is specified by the string_to_uniprot variable in config.ini. If the
    file exists, it overwrites it.

    Args:
      config: Configuration object that has been initialised from an *.ini file.

    Returns:
      A dictionary containing genomic locus tags (str) as keys and corresponding UniProt accession
      names as a list (str).

    """
    id_table = {}
    with open(self._conf.string_protein_aliases) as f:
      logging.info(f"Extracting STRING genomic locus tags and their corresponding UniProt "
                   f"accession names from {self._conf.string_protein_aliases}")
      # This is the regex from UniProt website to find any accession code in their database
      uniprot_regex_1 = re.compile("[OPQ][0-9][A-Z0-9]{3}[0-9]")
      uniprot_regex_2 = re.compile("[A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9]")
      uniprot_regex_3 = re.compile("[A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9][A-Z][A-Z0-9]{2}[0-9]")

      # We only want accession codes from lines with UniProt_AC annotation 
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
          # # xxxx.GENE_LOCUS_TAG.ISOFORM
          string_alias = tokens[0]
          #Split xxxx.GENE_LOCUS_TAG.ISOFORM into tokens and extract the GENE_LOCUS_TAG
          string_alias = (string_alias.split('.'))[1]

          uniprot_alias = tokens[1]

          if string_alias not in id_table:
            id_table[string_alias] = [uniprot_alias]
          else:
            id_table[string_alias].append(uniprot_alias)

    logging.info(f"Finished extracting STRING genomic locus tags from {self._conf.string_protein_aliases}")
    return id_table

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
