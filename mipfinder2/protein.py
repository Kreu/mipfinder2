# class Protein:
#   """A class wrapper for protein entries in an UniProtKB database
  
#   Provides convenience functions to work with UniProt protein entries
  
#   """

#   def __init__(self, fasta_header):
#     pass

def isLengthBetween(sequence, min_length: int=0, max_length: float=float('inf')) -> bool:
  """Checks whether the sequence length is between specified numbers.

  The sequence bound are checked as [min_length, max_length].

  Args:
    sequence (str): Sequence to check the length of.
    min_length (int): Minimum acceptable sequence length.
    max_length (int): Maximum acceptable sequence length.
  
  Returns:
    True if sequence length is within the specified bounds, else returns False.

  """
  if (len(sequence) < min_length) or (len(sequence) > max_length):
    return False
  else:
    return True