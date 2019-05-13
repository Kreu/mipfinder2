"""miPFinder version 2.0

WIP WIP WIP WIP
"""
import logging
import datetime
import pathlib
import typing

# TODO (Valdeko, 13/05/2019): This is here to get relative imports to work. This will have to change
# though. 
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# from scripts import alignments_v13

import config

# from ..scripts import alignments_v13
# from ..scripts import splicevariants_v13
# from ..scripts import splitdb_v13
# from ..scripts import read_v13
# from ..scripts import delta_v13
# from ..scripts import domains_v13

# from alignments_v13 import ALIGNMENTRATING
# from splicevariants_v13 import splicevariantsSEQ
# from splitdb_v13 import splitdb
# from read_v13 import readAnnotation, readFasta, readBlastTAB, readProteinGeneList, readiPfam, readDOMTBL, readSTRING
# from delta_v13 import percentsmall, percentZones
# from domains_v13 import domains, domainOverlap






# Set up logging configuration
logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    filename = 'mipfinder.log',
                    filemode = 'w',
                    format='%(asctime)s %(module)s %(name)s.%(funcName)s %(levelname)-8s %(message)s')

# TODO: Write a unit test for this
def getKnownMicroproteins(microprotein_list: str) -> typing.List[str]:
  """Extract known microprotein IDs from a file into a list.""" 
  known_microproteins = []
  with open(microprotein_list, 'r') as f:
    for line in f:
      known_microproteins.append(f)
  return known_microproteins 

######################
#   MIPFINDER v2.0   #
######################

if __name__ == "__main__":
  logging.info("Starting MIPFINDER v2.0")
  # TODO (12/05/2019, Valdeko): No need to log this, but need to time the script runtime 
  # logging.info(f"Starting at {datetime.datetime.now()}")
  logging.debug(f"Working directory is {os.getcwd()}")

  # TODO: Maybe rewrite using ConfigArgParser module rather than configuration file? Not important atm
  configuration = config.Config('config.ini')

  # getKnownMicroproteins(configuration.known_microproteins)


  # Create temporary directories to hold files necessary for processing
  pathlib.Path('temp').mkdir(parents = True, exist_ok = True)
  pathlib.Path('temp/blast').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/clustalo').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/hmmer').mkdir(parents=True, exist_ok = True)


# ######FILES AND FOLDERS##########
# #BLAST
# fastasplit = [' ','\n','\t','gi|','|','>']
# blastdb = 'blast/'+species+'_smallVSall_seq.blast'

# #CLUSTALW output
# CLUSTALfile = 'tempfiles/'+species+'_clustalW.txt'
# clustalwIN = 'tempfiles/tempfile.fasta'
# clustalwTEMP = 'tempfiles/tempout.fasta'

# #HMMBUILD output
# HMMfile = 'tempfiles/'+species+'_hmmbuild.hmm'

# #HMMSEARCH
# #-output
# outfile = species+'_miPlist.txt'
# HMMsearchTBL = 'tempfiles/'+species+'_HMMsearchTBL.txt'
# HMMsearchDOMTBL = 'tempfiles/'+species+'_HMMsearchDOMTBL.txt'
# hmmbuildOUT = currentPATH+'/tempfiles/'+species+'_hmmbuildtOUT.hmm'
# #-input 
# HMMsearchDATABASE = 'blast/big.fasta'

# #prepare files and folders
# if os.path.exists(currentPATH+'/alignment') or os.path.exists(currentPATH+'/blast'):
# 	q = raw_input('\ndelete /alignment and /blast folder? (Y/n/exit): ')
# 	if q == 'Y':
# 		if os.path.exists(currentPATH+'/alignment'):
# 			shutil.rmtree(currentPATH+'/alignment')
# 			os.makedirs(currentPATH+'/alignment')
# 		if os.path.exists(currentPATH+'/blast'):
# 			shutil.rmtree(currentPATH+'/blast')
# 			os.makedirs(currentPATH+'/blast')
# 	elif q == 'n':
# 		print 'WARNING: Will not delete /alignment and /blast folder, that may cause problems\n'
# 	else:
# 		print 'terminated'
# 		sys.exit()	
# if not os.path.exists(currentPATH+'/alignment'):
#     os.makedirs(currentPATH+'/alignment')
#     print 'create /alignment'
# if not os.path.exists(currentPATH+'/blast'):
#     os.makedirs(currentPATH+'/blast')
#     print 'create /blast'
# if not os.path.exists(currentPATH+'/tempfiles'):
#     os.makedirs(currentPATH+'/tempfiles')
#     print 'create /tempfiles'

# open(HMMfile,'w').close()
# open(CLUSTALfile,'w').close()