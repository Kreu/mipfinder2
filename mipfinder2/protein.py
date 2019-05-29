from __future__ import annotations

import logging
from typing import Dict, List 

class Protein(object):

  # Maps a unique identifier of each protein to Protein objects for fast search. The unique
  # identifier is made up of the protein's genomic locus tag and sequence version.
  proteins: Dict[str, List[Protein]] = {}

  def __init__(self, sequence: str, araport_tag: str, sequence_version: int, desc: str):
    """Class Protein is a wrapper for protein information.

    Proteins are identified by their unique ID made up from their genomic locus tag and their
    sequence version number.

    Args:
      sequence: Protein sequence in string format.
      araport_tag: The araport genomic locus tag of the protein.
      sequence_version: The sequence version of the protein sequence. This is to distinguish
          splice variants of the same gene.
      desc: Description of protein function.

    """
    self.unique_id: str = araport_tag + "." + str(sequence_version)
    self.sequence: str = sequence 
    self.araport_tag: str = araport_tag 
    self.sequence_version: int = int(sequence_version)
    self.length: int = len(sequence)
    self.desc: str = desc

    # self.domains: List[str] = None
    # self.nr_of_domains = None

    # Unique IDs (genomic locus tag + version number) of all known interactors
    self.interactors: List[str] = []

    # self.uniprot_accession: str = None
    
    #  
    if self.unique_id not in Protein.proteins:
      Protein.proteins[self.unique_id] = self
    else:
      logging.error(f"Error: {self.unique_id} already exists. Two different proteins should not "
                    f"share the same unique ID!")

  @classmethod
  def filterByLength(cls,
                     min_length: int=0,
                     max_length: float=float('inf'),
                     protein_data: Dict[str, List[Protein]]=proteins) -> Dict[str, List[Protein]]:
    """Filters all created Protein objects by length.

    Args:
      protein_data: A dictionary containing protein unique IDs as keys and Protein objects
          as values. Defaults to `Protein.proteins` class variable.
      min_length: Minimum length of a protein to keep, inclusive. Defaults to `0`.
      max_length: Maximum length of a protein to keep, inclusive. Defaults to `infinity`.

    Returns:
      A dictionary containing proteins that are between the lenghts of specified. The keys are
      the protein unique IDs and values are Protein objects. 

    """
    logging.info(f"Keeping proteins between the length of {min_length} and {max_length} amino acids.")
    filtered_proteins: Dict[str, Protein] = {}

    for unique_id, protein_obj in Protein.proteins.items():
        if (protein_obj.length >= min_length) and (protein_obj.length <= max_length):
            filtered_proteins[unique_id] = protein_obj
    
    logging.info(f"{len(filtered_proteins)} out of {len(Protein.proteins)} proteins match the length criteria.")
    return filtered_proteins

# def filterBySize(proteins: Dict[str, str], min_length: int=0, max_length: float=float('inf')):
#   """Filters proteins based on sequence length.

#   Args:
#     proteins: A dictionary with FASTA headers as keys and sequences as values
#     min_length: Minimum length of a protein to keep, inclusive.
#     max_length: Maximum length of a protein to keep, inclusive.

#   Returns:
#     A dictionary containing only the proteins with the specified length. The keys are the FASTA
#     headers and the values are the protein sequences.

#   """
#   filtered_proteins: dict = {}
#   for fasta_header, protein_sequence in proteins.items():
#     if (len(protein_sequence) >= min_length) and (len(protein_sequence) <= max_length):
#       filtered_proteins[fasta_header] = protein_sequence
#     else:
#       continue

#   logging.info(f"Found {len(filtered_proteins)} proteins between {min_length} and {max_length} amino acids in length from a set of {len(proteins)}")
#   return filtered_proteins 
