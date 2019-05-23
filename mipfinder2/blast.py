import subprocess
import logging

def createBlastDatabase(sequence_file: str, output: str):
  """Creates a BLAST database from a FASTA file.

  Creating a BLAST database file greatly speeds up searches with blast.

  Args:
    sequence_file (str): FASTA file containing sequences to be turned into a database
    output (str): Name for the BLAST database files. Creates three files called `output`.pin,
                  `output`.psq and `output`.phr

  """

  logging.info(f"Creating a BLAST database.")
  make_db_command = f"makeblastdb -in {sequence_file} -out {output} -dbtype prot"
  logging.info(f"Running the command: {make_db_command}")
  subprocess.run(make_db_command.split(' '))

def runBlast(blast_commmand: str):
  """Runs BLAST using the command specified.
  
  Args:
    blast_command (str): Terminal command to run. Has to specify blastp/blasn/etc.
  
  """
  subprocess.run(blast_commmand.split(' '))