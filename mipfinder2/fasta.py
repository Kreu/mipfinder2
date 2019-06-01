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
  logging.info(f"Writing {output_file}.fasta")
  with open(output_file, 'w') as f:
    for protein_id, protein_sequence in sequences.items():
      f.write(f">{protein_id}\n{protein_sequence}\n")
  logging.info(f"Finished writing {output_file}.fasta")

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

def extractAraportHeader(fasta_header: str) -> List[str]:
  """Extracts information from an Araport FASTA header.

  Araport headers are set up as follows:
  >GENOMIC_LOCUS_TAG.VERSION_NUMBER | PROTEIN_DESCRIPTION | CHROMOSOME_LOCATION <space> FORWARD <space> LENGTH=xxxxx | TODO: What's the last number?

  Args:
    fasta_header: FASTA header in Araport format

  Returns:
    A list of strings containing GENOMIC_LOCUS_TAG, VERSION_NUMBER, PROTEIN_DESCRIPTION in that 
    order.

  Raises:
    ValueError: If GENOMIC_LOCUS_TAG or VERSION_NUMBER cannot be found.
  """
  fasta_header = fasta_header.strip('\n')
  tokens: List[str] = tokenise(fasta_header, "[> .|]+")
  genomic_locus_tag = tokens[0]
  version_number = tokens[1]
  
  protein_desc_tokens: List[str] = tokenise(fasta_header, "[|]+")
  protein_description = protein_desc_tokens[1].strip(' ')

  if genomic_locus_tag == "" or version_number == "":
    raise ValueError("Genomic locus tag or version number is not present in Araport FASTA record header.")
    logging.info(f"Genomic locus tag or version number is not present in Araport FASTA record header.")

  header_contents = [genomic_locus_tag, version_number, protein_description]
  return header_contents

# def extractUniprotHeader(fasta_header: str, identifiers: List[str]) -> List[str]:
#   """Extracts one or more identifiers from a UniProtKB FASTA header.

#   | The general format of a UniProtKB header is represented as:
#   | >db|UniqueIdentifier|EntryName ProteinName OS=OrganismName OX=OrganismIdentifier [GN=GeneName ]PE=ProteinExistence SV=SequenceVersion

#   | Using the identifiers described below, this is represented as:
#   | >DB|ID|EN PN OS OX GN PE SV

#   For a more detailed explanation of the identifiers, see https://www.uniprot.org/help/fasta-headers

#   Args:
#     fasta_header: FASTA header in UniProtKB format
#     identifiers: A list of one or more identifiers to extract from the header. The potential 
#         identifiers are as follows: 

#         * DB - UniProt database
#         * ID - UniProt protein accession identifier
#         * EN - UniProt entry name
#         * PN - Protein name
#         * OS - Organism name
#         * OX - Organism NCBI taxonomy identifier
#         * GN - Gene Name
#         * PE - Protein existence level
#         * SV - Sequence version

#   Returns:
#     A list containing the contents of the identifiers. The order in which the contents are in the
#     list is the same order in which they were listed in `identifiers` list. If the identifier is not
#     present in the FASTA header, an empty string is returned.

#   Example:

#     >>> header = ">sp|P05783|K1C18_HUMAN Keratin, type I cytoskeletal 18 OS=Homo sapiens OX=9606 GN=KRT18 PE=1 SV=2"
#     >>> extractIdentifier(header, ["OS"])
#     ['Homo sapiens']
#     >>> extractIdentifier(header, ["GN"])
#     ['KRT18']
#     >>> extractIdentifier(header, ["PE", "OX", "DB", "ID"])
#     ['1', '9606', 'sp', 'P05783']
    
#   """
#   identifier_contents: list = []
#   for identifier in identifiers:
#     tokens = tokenise(fasta_header, "[>| ]+")
#     print(tokens)
#     # After tokenising, the first three identifiers will the the 0, 1 and 2 indices in the returned
#     # list.
#     if identifier == "DB":
#       uniprot_database_type: str = tokens[0]
#       identifier_contents.append(uniprot_database_type)
#       continue  #  As every identifier only corresponds to one if-condition, we can always continue.

#     if identifier == "ID":
#       uniprot_id: str = tokens[1]
#       identifier_contents.append(uniprot_id)
#       continue
    
#     if identifier == "EN":
#       entry_name: str = tokens[2] 
#       identifier_contents.append(entry_name)
#       continue

#     if identifier == "PN":
#       # This is the trickiest to extract. Can't really tokenise easily because of unpredictable
#       # contents. The best way to do is to find the previous and the following identifiers and 
#       # append whatever is between them. Since EN and OS are always required (e.g. not optional),
#       # we can use those as our boundaries.
#       entry_name: str = tokens[2]
#       entry_name_start_pos: int = fasta_header.find(entry_name)
#       entry_name_end_pos: int = entry_name_start_pos + len(entry_name)

#       organism_name_start_pos: int = fasta_header.find("OS=")

#       protein_name: str = fasta_header[entry_name_end_pos:organism_name_start_pos]

#       # Rather than use string slicing, we can just strip the leading and trailing spaces.
#       identifier_contents.append(protein_name.strip(' '))
#       continue

#     # For the rest of the identifiers we need to find where their identifier is in the string, and
#     # find the next identifier, which denotes the end of the identifier contents. Since the content
#     # sizes vary we can't simply use string indices. This could be done with regex but I think it's
#     # an overkill.
#     # To make this general for all the identifiers, we can just look for the next '=' character
#     # which (should) only exist in the identifiers.
#     if identifier == "OS" or identifier == "OX" or identifier == "PE" or identifier == "GN":
#       # Since "GN" identifier is optional, we must test whether it is present.
#       if identifier == "GN" and fasta_header.find("GN=") == -1:  # find() returns -1 if string not found.
#         identifier_contents.append("")  # As per API
#         continue

#       searchable_identifier = identifier + '='  # User-searchable list of identifiers lacks the '='
#       current_identifier_start_pos: int = fasta_header.find(searchable_identifier)
#       current_identifier_end_pos: int = current_identifier_start_pos + len(searchable_identifier)

#       next_identifier_pos: int = fasta_header[current_identifier_end_pos:].find('=')

#       # As the identifier are in the format of XX=Y and we look for =, we must subtract 2 to get the
#       # beginning of the next identifier.
#       next_identifier_start: int = current_identifier_end_pos + next_identifier_pos - 2

#       current_identifier_contents = fasta_header[current_identifier_end_pos:next_identifier_start]

#       # Strip extra spaces from either end (cleaner than string slicing) before appending.
#       identifier_contents.append(current_identifier_contents.strip(' '))
#       continue

#     if identifier == "SV":
#        sequence_variant_pos: int = fasta_header.find("SV=")
#        # Since SV is the last token, append substring from = till the end of the header
#        # find() returns the position of 'S' in "SV=3", so we add three to get the number.
#        identifier_contents.append(fasta_header[sequence_variant_pos + 3:])
#        continue 

#   return identifier_contents

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
