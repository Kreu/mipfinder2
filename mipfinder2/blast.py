import subprocess

def createBlastDatabase(sequence_file: str, output: str):
  """Creates a BLAST database from a FASTA file.

  Creating a BLAST database file greatly speeds up searches with blast.

  Args:
    sequence_file (str): FASTA file containing sequences to be turned into a database
    output (str): Name for the BLAST database files. Creates three files called `output`.pin,
                  `output`.psq and `output`.phr

  """

  make_db_command = f"makeblastdb -in {sequence_file} -out {output} -dbtype prot" 
  print(make_db_command)
  subprocess.run(make_db_command.split(' '))