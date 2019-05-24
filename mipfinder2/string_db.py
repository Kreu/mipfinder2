import typing
import logging

def stringToUniprot(string_protein_info: str):
  """Match STRING IDs to UniProt IDs.

  This uses an organism-specific file from STRING database from here:
  https://string-db.org/cgi/download.pl?sessionId=QSuugpq1Ea5l&species_text=Arabidopsis+thaliana

  Specifically, this one:
  3702.protein.info.v11.0.txt.gz (2.4 Mb) - list of STRING proteins incl. their display names and descriptions

  This file maps all of STRING protein IDs to different database IDs. Because
  mipfinder is written to work with UniProt IDs, we only extract those.

  The column contents differ for different databases but for the UniProt lines
  the first column is the STRING identifier and the second column is the UniProt
  identifier.

  Args:
    string_protein_info (str): File containing organism-specific list of STRING IDs and
                                descrpitions of how they relate to other databases. See
                                above where to download this file.

  Returns:
    A dictionary with STRING IDs as keys and UniProt IDs as string values.
    Each key maps to exactly one UniProt ID.
      
  """
  id_map = {}
  with open(string_protein_info) as f:
    line_count = 1
    for line in f:
      # The line count numbers are where the UniProt IDs are. Could be done
      # with regex but this way is easier (or this is way easier ;))
      # Might break if the format changes though.
      if (line_count >= 712094) and (line_count <= 765105):
        tokens = line.split('\t')
        print(tokens)

        # All STRING aliases in an organism database are suffixed with the
        # NCBI taxonomic identifier in the following format:
        # xxxx.GENE_IDENTIFIER.ISOFORM	Q9FZ30
        # We are only interested in the protein ID so we need to split the 
        # organism identifier.
        string_alias = tokens[0]
        #Split xxxx.GENE_IDENTIFIER.ISOFORM into tokens and retain the second
        string_alias = (string_alias.split('.'))[1]

        uniprot_alias = tokens[1]

        # Some of the UniProt IDs have suffixes even though they map to
        # the same STRING database alias, so we filter them out to
        # remove the redundancy.
        # TODO: Use if '_' in uniprot_alias as it is faster
        if (uniprot_alias.find('_') == -1): # -1 indicates substring not found
            id_map[string_alias] = uniprot_alias
      line_count += 1

  return id_map

def writeProteinAliases(aliases: dict, output: str):
  """Writes the STRING to UniProt ID mappings into a file.

  Args:
    alises: A dictionary with STRING IDs as keys and UniProt IDs as string values.
            Each key maps to exactly one UniProt ID.

  """
  with open(output, 'w') as x:
    for string_alias, uniprot_alias in aliases.items():
      x.write(f"{string_alias}\t{uniprot_alias}\n")


def extractLinks(string_database: str, score_cutoff: int=700, delimiter: str='\t', format="UNIPROT") -> typing.Dict[str, typing.List[str]]:
  """Extracts protein-protein interaction information from STRING database.

  An example of STRING database format is below:
  protein1 protein2 neighborhood fusion cooccurence coexpression experimental database textmining combined_score
  3702.AT1G01010.1 3702.AT1G10570.1 0 0 0 165 0 0 0 165
  3702.AT1G01010.1 3702.AT1G06149.1 0 0 0 0 0 0 865 86

  The score in the database is the same as on the STRING website but multiplied by a 1000, e.g. a
  score of 0.954 on the STRING website is 954 in the database file. The scores range from 0 to 1000. 
  The score indicates the likelihood of an interaction, e.g. a score of 500 means that every second 
  interaction is possibly erroneous.

  Args:
    string_database (str): File containing protein-protein interaction network data for a specific
        organism. This can be downloaded from http://www.string-db.org.
    score_cutoff (int): Exclude all protein-protein interactions with a reported value of lower than cutoff.
    delimiter (str): Character by which to split values into separate tokens.
    format (str): Output format of protein IDs. Defauls to `UNIPROT`.
        Other possible format is `STRING`

  Returns:
    A dictionary containing STRING IDs as as keys and a list of STRING IDs as values. 
    Interactions are duplicated, i.e. if protein 1 interacts with protein 2 and protein 3;
    and protein 2 interacts with protein 1 but not 3, it is
    represented as a {"1": ["2", "3"]} and as {"2": ["1"]} key-value pairs.

  """

  logging.info(f"Extracting STRING protein links from {string_database}.")
  protein_links: dict = {}
  with open(string_database, 'r') as f:
    next(f) # Ignore the header
    for line in f:
      line = line.strip('\n') # Interferes with processing
      tokens: list = line.split(delimiter)

      interaction_score: int = int(tokens[9])
      if interaction_score < score_cutoff:
        continue

      # All STRING aliases in an organism database are suffixed with the
      # NCBI taxonomic identifier in the following format:
      # xxxx.GENE_IDENTIFIER.ISOFORM	Q9FZ30
      # We are only interested in the protein ID so we need to split the 
      # organism identifier.
      first_protein: str = tokens[0]
      second_protein: str = tokens[1]
      #Split xxxx.GENE_IDENTIFIER.ISOFORM into tokens and retain the GENE_IDENTIFIER
      first_protein = (first_protein.split('.'))[1]
      second_protein = (second_protein.split('.'))[1]

      # print(f"{first_protein}, {second_protein}, {interaction_score}")

      if first_protein in protein_links:
        # print(protein_links[first_protein])
        protein_links[first_protein].append(second_protein)
      else:
        protein_links[first_protein] = [second_protein]
        # print(protein_links[first_protein])
  logging.info(f"Extracted {len(protein_links)} protein-protein interactions from {string_database}.") 
