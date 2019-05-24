import logging
import re
from typing import Dict, List

def createFile(sequences: Dict[str, str], output_file: str):
  """Creates a FASTA file from the supplied protein IDs and sequences.

  Args:
    sequences: A dictionary containing FASTA headers as keys and corresponding sequences as values
    output_file: Name of the output file. Overwrites the file if it already exists, otherwise
        creates a new file. The file will be created in the current directory.
  
  """
  logging.info(f"Writing {output}.fasta")
  with open(output, 'w') as f:
    file_contents: list  = []
    for protein_id, protein_sequence in sequences.items():
      f.write(f">{protein_id}\n{protein_sequence}\n")
  logging.info(f"Finished writing {output}.fasta")

def extractRecords(fasta_file: str) -> Dict[str, str]:
  """Extracts all FASTA records from a file into individual entries.

  Args:
    fasta_file: Path to the FASTA file.

  Returns:
    A dictionary containing a FASTA header as the key and the corresponding sequence as the value.

  Example:
    For example, given a file called proteins.fasta that contains the following FASTA records:
    
    | >header1
    | AAAHGT
    | >header2
    | GYTVS
    
    >>> extractRecords("proteins.fasta")
    {'header1': 'AAAHGT', 'header2': 'GYTVS'}

  """
  with open(fasta_file, 'r') as f:
    fasta_identifier: str = ""
    fasta_sequence: str = ""
    fasta_records: dict = {}
    fasta_record_found: bool = False

    for line in f:
      #Strip newlines because they interfere with processing
      line: str = line.strip('\n')
      
      # A FASTA format contains a line always starting with '>' character. This line contains 
      # information about the sequence such as its ID, source organism, gene code or the like

      if line.startswith('>') and not fasta_record_found:
        fasta_record_found = True
        fasta_identifier = line
        continue

      elif not line.startswith('>') and fasta_record_found:
        fasta_sequence += line
        continue

      #If new record has been found
      elif line.startswith('>') and fasta_record_found:
        fasta_records[fasta_identifier] = fasta_sequence
        
        # Reset the variables for the next entry
        fasta_sequence = ""
        fasta_identifier = line
        continue

      # If FASTA record has not been found, the line contains bad data as far as we are concerned
      elif not fasta_record_found:
        continue

    # Finally, if we hit the last line of the file, we need to write the last entry.
    fasta_records[fasta_identifier] = fasta_sequence
    logging.info(f"Extracted {len(fasta_records)} records from {fasta_file}.")
    return fasta_records

def extractIdentifier(fasta_header: str, identifiers: List[str]) -> List[str]:
  """Extracts one or more identifiers from a UniProtKB FASTA header.

  | The general format of a UniProtKB header is represented as:
  | >db|UniqueIdentifier|EntryName ProteinName OS=OrganismName OX=OrganismIdentifier [GN=GeneName ]PE=ProteinExistence SV=SequenceVersion

  | Using the identifiers described below, this is represented as:
  | >DB|ID|EN PN OS OX GN PE SV

  For a more detailed explanation of the identifiers, see https://www.uniprot.org/help/fasta-headers

  Args:
    fasta_header: FASTA header in UniProtKB format
    identifiers: A list of one or more identifiers to extract from the header. The potential 
        identifiers are as follows: 

        * DB - UniProt database
        * ID - UniProt protein accession identifier
        * EN - UniProt entry name
        * PN - Protein name
        * OS - Organism name
        * OX - Organism NCBI taxonomy identifier
        * GN - Gene Name
        * PE - Protein existence level
        * SV - Sequence version

  Returns:
    A list containing the contents of the identifiers. The order in which the contents are in the
    list is the same order in which they were listed in `identifiers` list.

  Example:

    >>> header = ">sp|P05783|K1C18_HUMAN Keratin, type I cytoskeletal 18 OS=Homo sapiens OX=9606 GN=KRT18 PE=1 SV=2"
    >>> extractIdentifier(header, ["OS"])
    ['Homo sapiens']
    >>> extractIdentifier(header, ["GN"])
    ['KRT18']
    >>> extractIdentifier(header, ["PE", "OX", "DB", "ID"])
    ['1', '9606', 'sp', 'P05783']
    
  """

  # There are multiple ways to extract the requested contents, these are just one way of doing it.
  identifier_contents: list = []
  for identifier in identifiers:
    if identifier == "DB":
      identifier_contents.append[fasta_header[:2]]  # DB is always the first two characters of the header.
      continue  #  As every identifier only corresponds to one if-condition, we can always continue.

    if identifier == "ID":
      split_header: list = fasta_header.split('|')
      uniprot_id: str = split_header[1]
      identifier_contents.append(uniprot_id)
      continue
    
    if identifier == "EN":
      tokens: list = tokenise(header, "[| ]+")
      entry_name: str = tokens[2]  # The above tokenise splits >DB|ID|EN PN... into >DB, ID, EN, PN...
      identifier_contents.append(entry_name)
      continue

    if identifier == "PN":
      # This is the trickiest to extract. Can't really tokenise easily because of unpredictable
      # contents. The best way to do is to find the previous and the following identifiers and 
      # append whatever is between them. Since EN and OS are always required (e.g. not optional),
      # we can use those as our boundaries.
      tokens: list = tokenise(header, "[| ]+")
      entry_name: str = tokens[2]

      # TODO: Possibly need to adjust indices to not include bordering spaces
      entry_name_start_pos: int =  fasta_header.rfind(entry_name)  # Use rfind because we want the last position of the match
      organism_name_start_pos: int = fasta_header.find("ON=")

      protein_name: str = fasta_header[entry_name_start_pos:organism_name_start_pos]
      identifier_contents.append(protein_name)
      continue

    # For the rest of the identifiers we need to find where their identifier is in the string, and
    # find the next space, which denotes the end of the identifier contents. Since the content sizes
    # vary we can't simply use string indices. This could be done with regex but I think it's an 
    # overkill.
    if identifier == "OS":
      organism_name_pos: int = fasta_header.rfind("ON=")
      next_space: int = fasta_header[organism_name_pos:].find(' ')  # Look for the next space starting from the end of ON=
      organism_name = fasta_header[organism_name_pos:next_space]
      identifier_contents.append(organism_name)
      continue

    if identifier == "OX":
      organism_taxonomy_pos: int = fasta_header.rfind("OX=")
      next_space: int = fasta_header[organism_taxonomy_pos:].find(' ')  # Look for the next space starting from the end of OX=
      organism_taxonomy = fasta_header[organism_taxonomy_pos:next_space]
      identifier_contents.append(organism_taxonomy)
      continue 

    if identifier == "GN":
      if fasta_header.rfind("GN=") != -1: # GN is an optional parameter and may not be present
        gene_name_pos: int = fasta_header.rfind("GN=")
        next_space: int = fasta_header[gene_name_pos:].find(' ')  # Look for the next space starting from the end of GN=
        gene_name = fasta_header[gene_name_pos:next_space]
        identifier_contents.append(gene_name)
      continue
      
    if identifier == "PE":
      protein_existence_pos: int = fasta_header.rfind("PE=")
      next_space: int = fasta_header[protein_existence_pos:].find(' ')  # Look for the next space starting from the end of PE=
      protein_existence = fasta_header[protein_existence_pos:next_space]
      identifier_contents.append(protein_existence) 
    #   
    if identifier == "SV":
       sequence_variant_pos: int = fasta_header.rfind("SV=")
       # Since SV is the last token, append substring from = till the end of the header
       identifier_contents.append(fasta_header[sequence_variant_pos:]) 

  return identifier_contents

def extractUniprotID(fasta_header: str, protein_existence_cutoff: int) -> str:
  #TODO 15/05/2019, Valdeko: Maybe let user specify what record they want to extract,
  #possiby by specifying a column?
  """Extract the Uniprot ID from a UniProtKB FASTA header.

  For a detailed description of UniProt FASTA headers, see here:
  https://www.uniprot.org/help/fasta-headers

  Args:
    fasta_header: UniProt FASTA header for a protein record.
    protein_existence_cutoff: An integer representing which ProteinExistence levels (see link
        above) to filter out. Filters out everything that is equal to 
        AND larger (e.g. protein_existence_cutoff=3 only shows proteins
        with PE level of 1 and 2)

  Returns:
    A string containing the UniProt ID of the given FASTA record. If no UniProt ID can be detected 
    or if ProteinExistence level is equal to or above the threshold, an empty string is returned.
  """

  if extractProteinExistenceLevel(fasta_header) >= protein_existence_cutoff:
    return ""

  # Split the FASTA header by `|`, this results in a list where the UniProt ID is in the
  # second column, unless the header is malformed.
  split_header: str = fasta_header.split('|')
  uniprot_id: str = split_header[1]
  return uniprot_id


def tokenise(string: str, delimiter: str) -> List[str]:
  """Splits a string into tokens based on the specified delimiter(s).

  Args:
    string: String to be tokenised.
    delimiter: Regular expression containing the delimiters to split the string by. 

  Returns:
    A list of tokens as string, split at the specified delimiter(s).

  Example:
    Split a string at every comma (,) and hyphen (-):
      >>> string = "Test, string to-be split"
      >>> tokenise(string, "[,\-]+")
      ["Test", " string to", "be split"]

    Split a string at every space and exclamation point:
      >>> string = "This! Is another example!"
      >>> tokenise(string, "[ !]+")
      ["This", "Is", "another", "example"]

  """

  tokens = list(filter(None, re.split(delimiter, string)))  # Need to wrap in list() in Python3
  return tokens
