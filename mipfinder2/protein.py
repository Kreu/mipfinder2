from __future__ import annotations

import logging
from typing import Dict, List 

class Protein(object):

  # Maps protein genomic locus tags to Protein objects for fast search
  proteins: Dict[str, List[Protein]] = {}

  def __init__(self, sequence: str, araport_tag: str, sequence_version: int, desc: str):
    """Class Protein is a wrapper for protein information.

    Uses Araport genome locus tags as unique identifiers for proteins.

    Args:
      sequence: Protein sequence in string format.
      araport_tag: The araport genomic locus tag of the protein.
      sequence_version: The sequence version of the protein sequence. This is to distinguish
          splice variants of the same gene.
      desc: Description of protein function.

    """
    self.sequence: str = sequence 
    self.araport_tag: str = araport_tag 
    self.sequence_version: int = int(sequence_version)
    self.length: int = len(sequence)
    self.desc: str = desc


    self.domains: List[str] = None
    self.nr_of_domains = None
    self.interacting_domain: List[str] = None
    self.uniprot_accession: str = None
    
    # TODO: What if a protein with an existing araport_tag and existing sequence version is
    # added to the list of Protein objects? 
    if araport_tag not in Protein.proteins:
      Protein.proteins[araport_tag] = [self]
    else:
      Protein.proteins[araport_tag].append(self)

  @classmethod
  def filterByLength(cls,
                     min_length: int=0,
                     max_length: float=float('inf'),
                     protein_data: Dict[str, List[Protein]]=proteins) -> Dict[str, List[Protein]]:
    """Filters all created Protein objects by length.

    Args:
      protein_data: A dictionary containing Araport genomic locus tags as keys and Protein objects
          as a list of values. Defaults to `Protein.proteins` class variable.
      min_length: Minimum length of a protein to keep, inclusive. Defaults to `0`.
      max_length: Maximum length of a protein to keep, inclusive. Defaults to `infinity`.

    Returns:
      A dictionary containing proteins that are between the lenghts of specified. The keys are
      the Araport genome locus tags and values are a list of Protein objects. 

    """
    logging.info(f"Keeping proteins between the length of {min_length} and {max_length} amino acids.")
    filtered_proteins: Dict[str, List[Protein]] = {}

    for genomic_locus_tag, protein_obj_list in Protein.proteins.items():
      for individual_protein  in protein_obj_list:
        if (individual_protein.length >= min_length) and (individual_protein.length <= max_length):
          if genomic_locus_tag not in filtered_proteins:
            filtered_proteins[genomic_locus_tag] = [individual_protein]
    
          if genomic_locus_tag in filtered_proteins:
            filtered_proteins[genomic_locus_tag].append(individual_protein)

    logging.info(f"{len(filtered_proteins)} out of {len(Protein.proteins)} proteins match the length criteria.")
    return filtered_proteins

def filterBySize(proteins: Dict[str, str], min_length: int=0, max_length: float=float('inf')):
  """Filters proteins based on sequence length.

  Args:
    proteins: A dictionary with FASTA headers as keys and sequences as values
    min_length: Minimum length of a protein to keep, inclusive.
    max_length: Maximum length of a protein to keep, inclusive.

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
