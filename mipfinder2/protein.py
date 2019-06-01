from __future__ import annotations

import logging
from typing import Dict, List 

class Protein(object):

  # Maps a unique identifier of each protein to Protein objects for fast search. The unique
  # identifier is made up of the protein's genomic locus tag and sequence version.
  proteins: Dict[str, List[Protein]] = {}

  def __init__(self, sequence: str, genomic_locus_tag: str, sequence_version: int, desc: str):
    """Class Protein is a wrapper for protein information.

    Proteins are identified by their unique ID made up from their genomic locus tag and their
    sequence version number.

    Args:
      sequence: Protein sequence in string format.
      genomic_locus_tag: The araport genomic locus tag of the protein.
      sequence_version: The sequence version of the protein sequence. This is to distinguish
          splice variants of the same gene.
      desc: Description of protein function.

    """
    self._sequence: str = sequence 
    self._genomic_locus_tag: str = genomic_locus_tag 
    self._sequence_version: int = int(sequence_version)
    self._desc: str = desc

    self._unique_id: str = genomic_locus_tag + "." + str(sequence_version)
    self._length: int = len(sequence)
    self._uniprot_accession: str = ""

    # The list contains the unique_ids of other interacting proteins
    self._interactors: List[str] = []

    # self.domains: List[str] = None
    # self.nr_of_domains = len(self._domains)

    if self._unique_id not in Protein.proteins:
      Protein.proteins[self._unique_id] = self
    else:
      logging.error(f"Error: {self._unique_id} already exists. Two different proteins should not "
                    f"share the same unique ID!")

  ##################
  #   PROPERTIES   #
  ##################

  @property
  def sequence(self):
    return self._sequence

  @property
  def genomic_locus_tag(self):
    return self._genomic_locus_tag

  @property
  def sequence_version(self):
    return self._sequence_version
  
  @property
  def desc(self):
    return self._desc
  
  @property
  def unique_id(self):
    return self._unique_id

  @property
  def length(self):
    return self._length

  @property
  def uniprot_accession(self):
    return self._uniprot_accession 

  @property
  def interactors(self):
    return self._interactors

  @interactors.setter
  def interactors(self, interaction_partners: List[str]):
    self._interactors += interaction_partners

  ###############
  #   METHODS   #
  ###############

  @classmethod
  def filterByLength(cls,
                     min_length: int=0,
                     max_length: float=float('inf'),
                     protein_data: Dict[str, List[Protein]]=proteins) -> Dict[str, Protein]:
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
