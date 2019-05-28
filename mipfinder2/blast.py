import logging
import subprocess

def createDatabase(fasta_file: str, output_file: str):
  """Creates a BLAST database files from a FASTA file.

  Creating a BLAST database file greatly speeds up blast searches. This is an optional but a
  highly recommended step.

  Args:
    fasta_file: FASTA file containing all of the sequences to be turned into a database.
    output_file: Name for the BLAST database files. Creates three files in the current directory
        called `output_file`.pin, `output_file`.psq and `output_file`.phr.

  """

  logging.info(f"Creating a BLAST database.")
  make_db_command: str = f"makeblastdb -in {sequence_file} -out {output} -dbtype prot"
  logging.info(f"Running the command: {make_db_command}")
  subprocess.run(make_db_command.split(' '))

def run(command: str):
  """Runs the specified command in the terminal. 

  Args:
    command: Exact terminal command to run.

  Example:
    >>> command = "blastp -query query_file.fasta -db database_file -out results.txt"
    >>> run(command)
  
  """
  subprocess.run(command.split(' '))

def extractResults(blast_results: str):
  """Extracts """
  pass