import typing
import logging

# TODO: Write unit tests for this
def createFile(sequences: dict, output: str):
  """Creates a FASTA file from the supplied protein IDs and sequences.

  Args:
    sequences (dict): A dictionary containing protein IDs as keys and corresponding sequences as values
    output (str): Name of the output file. Overwrites the file if it already exists, otherwise creates
                  a new file.
  
  """
  logging.info(f"Writing {output}.fasta")
  with open(output, 'w') as f:
    file_contents: list  = []
    for protein_id, protein_sequence in sequences.items():
      f.write(f">{protein_id}\n{protein_sequence}\n")
  logging.info(f"Finished writing {output}.fasta")

def extractRecords(fasta_file: str) -> typing.Dict[str, str]:
  """Extracts all FASTA records from a file into individual entries.

  Args:
    fasta_file (str): Path to a file containing all the proteins of the target
                      organism in FASTA format.
  Returns:
    Dictionary containing protein FASTA header as the key and protein sequence
    as the value.

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

def getProteinExistenceLevel(fasta_header: str) -> int:
  """Extracts ProteinExistence level from a UniProtKB FASTA header.

  Returns:
    An integer denoting the ProteinExistence level for a given header. If ProteinExistence
    cannot be found within the header, return -1

  """
  # PE level is always a single digit number, we can just access the character after `PE=` substring.
  pe_position: int  = fasta_header.find("PE=")
  pe_level: int = -1
  if pe_position != -1: #If string is not found, find() returns -1
    pe_level = fasta_header[pe_position + 3] #It's `3` because in `PE=x` x denotes the PE level integer
    return int(pe_level)
  else:
    return -1

def extractUniprotID(fasta_header: str, protein_existence_cutoff: int) -> str:
  #TODO 15/05/2019, Valdeko: Maybe let user specify what record they want to extract,
  #possiby by specifying a column?
  """Extract the Uniprot ID from a FASTA record.

  Different databases have different FASTA record headers, however MIPFINDER v2.0 has been developed
  using UniProtKB database and serves as an example here.

  A generic example of a FASTA record in UniprotKB is as follows:
  >db|UniqueIdentifier|EntryName ProteinName OS=OrganismName OX=OrganismIdentifier [GN=GeneName ]PE=ProteinExistence SV=SequenceVersion

  An example of an actual FASTA record header in UniProtKB is as follows.
  >sp|Q9C5U0|AHK4_ARATH Histidine kinase 4 OS=Arabidopsis thaliana OX=3702 GN=AHK4 PE=1 SV=1

  A detailed description of the header is found at https://www.uniprot.org/help/fasta-headers, 
  here is just a copied version from their website
# class TestcreateFastaFile (unittest.TestCase):
#   pass
    db is ‘sp’ for UniProtKB/Swis# class TestcreateFastaFile (unittest.TestCase):
#   passs-Prot and ‘tr’ for UniProtKB/TrEMBL.
    UniqueIdentifier is the prima# class TestcreateFastaFile (unittest.TestCase):
#   passry accession number of the UniProtKB entry.
    EntryName is the entry name o# class TestcreateFastaFile (unittest.TestCase):
#   passf the UniProtKB entry.
    ProteinName is the recommende# class TestcreateFastaFile (unittest.TestCase):
#   passd name of the UniProtKB entry as annotated in the RecName field. For UniProtKB/TrEMBL entries without a RecName field, the SubName field is used. In case of multiple SubNames, the first one is used. The ‘precursor’ attribute is excluded, ‘Fragment’ is included with the name if applicable.
    OrganismName is the scientifi# class TestcreateFastaFile (unittest.TestCase):
#   passc name of the organism of the UniProtKB entry.
    OrganismIdentifier is the unique identifier of the source organism, assigned by the NCBI.
    GeneName is the first gene name of the UniProtKB entry. If there is no gene name, OrderedLocusName or ORFname, the GN field is not listed.
    ProteinExistence is the numerical value describing the evidence for the existence of the protein. (From 1-5)
      1. Experimental evidence at protein level
      2. Experimental evidence at transcript level
      3. Protein inferred from homology
      4. Protein predicted
      5. Protein uncertain
    SequenceVersion is the version number of the sequence.

  Args:
    fasta_header (str): String representation of the FASTA header for a protein record
    protein_existence_cutoff (int): An integer representing which ProteinExistence levels (see
                                    above) to filter out. Filters out everything that is equal to 
                                    AND larger (e.g. protein_existence_cutoff=3 only shows proteins
                                    with PE level of 1 and 2)

  Returns:
    A string containing the UniProt ID of the given FASTA record. If no UniProt ID can be detected 
    or if ProteinExistence level is equal to or above the threshold, an empty string is returned.
  """

  if getProteinExistenceLevel(fasta_header) >= protein_existence_cutoff:
    return ""

  # Split the FASTA header by `|`, this results in a list where the UniProt ID is in the
  # second column, unless the header is malformed.
  split_header: str = fasta_header.split('|')
  uniprot_id: str = split_header[1]
  return uniprot_id