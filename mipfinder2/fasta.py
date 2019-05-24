import logging
import re
from typing import Dict, List

def createFile(sequences: Dict[str, str], output_file: str):
  """Creates a FASTA file from the supplied protein IDs and sequences.

  Args:
    sequences: A dictionary containing FASTA headers as keys and corresponding sequences as values
    output_file: Name of the output file. Overwrites the file if it already exists, otherwise
        creates a new file.
  
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

def extractProteinExistenceLevel(fasta_header: str) -> int:
  """Extracts ProteinExistence level from a UniProtKB FASTA header.

  From https://www.uniprot.org/help/fasta-headers:
  * ProteinExistence is the numerical value describing the evidence for the existence of the protein. (From 1-5)
    1. Experimental evidence at protein level
    2. Experimental evidence at transcript level
    3. Protein inferred from homology
    4. Protein predicted
    5. Protein uncertain

  Returns:
    An integer denoting the ProteinExistence level for a given header. If ProteinExistence
    cannot be found within the header, returns -1

  """
  # PE level is always a single digit number, we can just access the character after `PE=` substring.
  pe_position: int  = fasta_header.find("PE=")
  pe_level: int = -1
  if pe_position != -1:  #If string is not found, find() returns -1
    pe_level = fasta_header[pe_position + 3]  # It's `3` because in `PE=x` x denotes the PE level integer
    return int(pe_level)
  else:
    return -1

def extractUniprotID(fasta_header: str, protein_existence_cutoff: int) -> str:
  #TODO 15/05/2019, Valdeko: Maybe let user specify what record they want to extract,
  #possiby by specifying a column?
  """Extract the Uniprot ID from a UniProtKB FASTA header.

  For a detailed description of UniProt FASTA headers, see here:
  https://www.uniprot.org/help/fasta-headers

  Args:
    fasta_header: UniProt FASTA header for a protein record.
    protein_existence_cutoff: An integer representing which ProteinExistence levels (see
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
