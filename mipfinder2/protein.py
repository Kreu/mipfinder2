import logging
import typing

def filterBySize(proteins: typing.Dict[str, str], min_length: int=0, max_length: float=float('inf')):
  """Filters proteins based on sequence length.

  Args:
    proteins (dict): A dictionary with FASTA headers as keys and sequences as values
    min_length (int): Minimum length of a protein to keep, inclusive.
    max_length (int): Maximum length of a protein to keep, inclusive.

  Returns:
    A dictionary containing only the proteins with the specified length. The keys are the FASTA
    headers and the values are the protein sequences.

  """
  filtered_proteins: dict = {}
  for fasta_header, protein_sequence in proteins.items():
    if (len(protein_sequence) >= min_length) and (len(protein_sequence) <= max_length):
      filtered_proteins[fasta_header] = protein_sequence
    else:
      continue

  logging.info(f"Found {len(filtered_proteins)} proteins between {min_length} and {max_length} amino acids in length from a set of {len(proteins)}")
  return filtered_proteins 