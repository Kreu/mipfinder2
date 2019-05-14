"""miPFinder version 2.0

WIP WIP WIP WIP
"""
import logging
import datetime
import pathlib
import shutil
import typing
import subprocess

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
from scripts import read_v13
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
                    format='%(asctime)s %(module)s.%(funcName)s %(levelname)-8s %(message)s',
                    datefmt = "%Y-%m-%d %H:%M:%S")
                #     format='%(asctime)s %(module)s %(name)s.%(funcName)s %(levelname)-8s %(message)s')

# TODO: Write a unit test for this
def getKnownMicroproteins(microprotein_list: str) -> typing.List[str]:
  """Extract known microprotein IDs from a file into a list.""" 
  known_microproteins = []
  with open(microprotein_list, 'r') as f:
    for line in f:
      known_microproteins.append(f)
  return known_microproteins 

def createTempDirs():
  """Create temporary directories to hold processing files."""
  pathlib.Path('temp').mkdir(parents = True, exist_ok = True)
  pathlib.Path('temp/blast').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/clustalo').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/hmmer').mkdir(parents=True, exist_ok = True)
  pathlib.Path('temp/aligment').mkdir(parents=True, exist_ok = True)

def removeTempDirs():
  """Remove temporary directories that hold processing files.
  
  If temporary directories do not exist, the function does nothing
  
  """
  try:
    shutil.rmtree('temp')
  except FileNotFoundError:
    pass

def createTempFiles(species_prefix: str):
  # TODO (Valdeko, 14/05/2019): Clean this up and localise the variables to where they are used
  blast_database = 'blast/'+species_prefix+'_smallVSall_seq.blast'

  #CLUSTALW output
  CLUSTALfile = 'tempfiles/'+species_prefix+'_clustalW.txt'
  clustalwIN = 'tempfiles/tempfile.fasta'
  clustalwTEMP = 'tempfiles/tempout.fasta'

  #HMMBUILD output
  HMMfile = 'tempfiles/'+species_prefix+'_hmmbuild.hmm'

  #HMMSEARCH
  #-output
  outfile = species_prefix+'_miPlist.txt'
  HMMsearchTBL = 'tempfiles/'+species_prefix+'_HMMsearchTBL.txt'
  HMMsearchDOMTBL = 'tempfiles/'+species_prefix+'_HMMsearchDOMTBL.txt'
  hmmbuildOUT = '/tempfiles/'+species_prefix+'_hmmbuildtOUT.hmm'
  #-input 
  HMMsearchDATABASE = 'blast/big.fasta'

  open(HMMfile,'w').close()
  open(CLUSTALfile,'w').close()

###########################################################################################
#   _____               _   _   _____   ______   _        _    _____                      # 
#  |  __ \      /\     | \ | | |_   _| |  ____| | |      ( )  / ____|                     #
#  | |  | |    /  \    |  \| |   | |   | |__    | |      |/  | (___                       #
#  | |  | |   / /\ \   | . ` |   | |   |  __|   | |           \___ \                      #
#  | |__| |  / ____ \  | |\  |  _| |_  | |____  | |____       ____) |                     #
#  |_____/  /_/    \_\ |_| \_| |_____| |______| |______|     |_____/                      #
#                                                                                         #
#   ______   _    _   _   _    _____   _______   _____    ____    _   _    _____          #
#  |  ____| | |  | | | \ | |  / ____| |__   __| |_   _|  / __ \  | \ | |  / ____|         #
#  | |__    | |  | | |  \| | | |         | |      | |   | |  | | |  \| | | (___           #
#  |  __|   | |  | | | . ` | | |         | |      | |   | |  | | | . ` |  \___ \          #
#  | |      | |__| | | |\  | | |____     | |     _| |_  | |__| | | |\  |  ____) |         #
#  |_|       \____/  |_| \_|  \_____|    |_|    |_____|  \____/  |_| \_| |_____/          #
#                                                                                         #
###########################################################################################

# ###########START####################################################
# ######SPLIT DB +BLAST#->###
# if os.path.isfile(conf.blast_database) == False or os.path.isfile(HMMsearchDATABASE) == False:
#         splitdb(conf.blast_path,conf.protein_list,'blast/small.fasta',HMMsearchDATABASE,blast_database,maximum_mip_length,minimum_ancestor_length,fastasplit)
	
# ###########ONLY_1VS1->###########

# def sizeFilter(data,maxsize,minsize,sizedb):
#         temp = [[],[]]
#         for i in range(len(data[0])):
#                 mip = ''
#                 if len(sizedb[1][sizedb[0].index(data[0][i])]) <= maxsize:
#                         mip = data[0][i]
#                 anc = []
#                 if isinstance(data[1][i],list):
#                         for j in range(len(data[1][i])):
#                                 if len(sizedb[1][sizedb[0].index(data[1][i][j])]) >= minsize:
#                                         anc.append(data[1][i][j])
#                 elif len(sizedb[1][sizedb[0].index(data[1][i])]) >= minsize:
#                         anc.append(data[1][i])
#                 if mip != '' and anc != []:
#                         temp[0].append(mip)
#                         temp[1].append(anc)
#         print 'found',len(temp[0]),'blast results with query <=',maxsize,'and hit >=',minsize
#         return temp

# def maxSizeFilter(tofilter,sizedb,size):
#         temp = [[],[]]
#         for i in range(len(tofilter[1])):
#                 temptemp = []
#                 for j in range(len(tofilter[1][i])):
#                         if len(sizedb[1][sizedb[0].index(tofilter[1][i][j])]) <= size:
#                                 temptemp.append(tofilter[1][i][j])
#                 if not temptemp == []:
#                         temp[0].append(tofilter[0][i])
#                         temp[1].append(temptemp)
#         print 'found',len(temp[0]),'sequences <=',size
#         return temp

# def eValueFilter(tofilter,evalue):
#         temp = [[],[],[],[],[]]
#         for i in range(len(tofilter[1])):
#                 temptemp = [[],[]]
#                 for j in range(len(tofilter[1][i])):
#                         if float(tofilter[2][i][j]) <= evalue:
#                                 temptemp[0].append(tofilter[1][i][j])
#                                 temptemp[1].append(float(tofilter[2][i][j]))
#                 if not temptemp[0] == []:
#                         temp[0].append(tofilter[0][i])
#                         temp[1].append(temptemp[0])
#                         temp[2].append(tofilter[3][i])
#                         temp[3].append(tofilter[4][i])
#                         temp[4].append(temptemp[1])
#         print 'found',len(temp[0]),'sequence hits with evalue <=',evalue
#         return temp

# def makeProteinGeneList(database):
# 	temp = [[],[]]
# 	for item in database:
# 		temp[0].append(item)
# 		temp[1].append(item)
# 	return temp

# #########ONLY_GROUPS->##########

# def makeGroups(data,protein_gene_list):
#         print '\ncluster miP candidates based on sequence similarity'
#         temparray = []
#         for l in range(len(data[0])):
#                 temp = []
#                 for m in range(len(data[0])):
#                         if data[0][l] in data[1][m]:
#                                 for n in range(len(data[1][m])):
#                                         temp.append(data[1][m][n])
#                 temp = list(set(temp))
#                 temp.sort()
#                 temparray.append(temp)
#         temp = []
#         for array in temparray:
#                 if not array in temp:
#                         temp.append(array)
#         temparray = temp

#         def findDouble(temparray,number):
#             temp = []
#             dropped = []
#             for group in temparray:
#                 newgroup = ''
#                 if len(group) >= maxMIPgroupSIZE: 
#                         print '[1] drop group with',len(group),'members'
#                 else:
#                         newgroup = group
#                         for groupsplit in temparray:
#                             if not group == groupsplit:
#                                 for AGI in groupsplit:
#                                     if AGI in group:
#                                         newgroup.extend(groupsplit)
#                                         newgroup = list(set(newgroup))
#                                         if len(newgroup) >= maxMIPgroupSIZE+1:
#                                                 break
#                             if len(newgroup) >= maxMIPgroupSIZE+1:
#                                     break
#                 newgroup  = list(set(newgroup))
#                 newgroup.sort()
#                 if newgroup != '' and len(newgroup) < maxMIPgroupSIZE:
#                         temp.append(newgroup)
#                 else:
#                         dropped.extend(newgroup)
#                         dropped = list(set(dropped))
#             temparray = temp        
#             temp = []
#             for array in temparray:
#                     if not array in temp:
#                             temp.append(array)
        
#             Input = open(dropfile,'a')
#             dropped = list(set(dropped))
#             Input.write((';'.join(dropped)+'\n'))
#             Input.close()
#             if len(dropped) > 0:
#                     print '[2] skip groups with >=',maxMIPgroupSIZE,'members; total',len(dropped),'sequences'
#             return temp           
#         temparray = findDouble(temparray,2)
#         temparray = findDouble(temparray,3)
#         temparray = findDouble(temparray,4)
#         countWOsplice=0
#         countRATIOtwo=0
#         countOTHER=0
#         tempreturn = [[],[]]
#         i=0
#         for array in temparray:
#                 i+=1
#                 array = splicevariantsSEQ(array,protein_gene_list,protein_list
#                 if len(array) >= 2:
#                         name = str(i)+'_'+str(len(array))
#                         tempreturn[1].append(array)
#                         tempreturn[0].append(name)
#                 elif len(array) == 0:
#                         print 'WARNING: no sequence info after splice variant filtering!',name
#                 else:
#                         name = str(i)+'_1'
#                         tempreturn[1].append(array)
#                         tempreturn[0].append(name)                
#         print 'large groups of small proteins with more than',maxMIPgroupSIZE,'members are discarded, but saved in',dropfile                
#         return tempreturn

# def alignAndBuildHMM(data,name):
#         #make sequencefile of group
#         global protein_list, HMMfile, hmmbuildLINE, clustalwLINE
#         line = ''
#         for AGI in data:
#                 line += '>'+AGI+'\n'+protein_list1][protein_list[].index(AGI)]+'\n'
#         output = open(clustalwIN,'w')
#         output.write(line)
#         output.close()

#         #align with clustalW2.1
#         clustalwLINE = clustalwPATH+' -INFILE='+clustalwIN+' -ALIGN -ENDGAPS'+gapopen+' -TYPE=PROTEIN -OUTFILE='+clustalwTEMP
#         subprocess.check_output(clustalwLINE, shell=True)        
#         Input = open(clustalwOUT,'r')
#         clustal = Input.read()
#         Input.close()
#         Input = open(CLUSTALfile,'a')
#         Input.write(clustal)
#         Input.close()        

#         #build hmm
#         hmmbuildLINE = hmmbuildPATH+' --amino '+hmmbuildOUT+' '+currentPATH+'/'+clustalwTEMP
#         subprocess.check_output(hmmbuildLINE, shell=True)
#         Input = open(hmmbuildOUT,'r')
#         hmm = Input.read()
#         Input.close()
#         hmm = hmm.split('\n')
#         line = hmm[1].split()
#         line = line[0]+'  '+name
#         Input = open(HMMfile,'a')
#         Input.write((hmm[0]+'\n'))
#         Input.write((line+'\n'))
#         for i in range(2,len(hmm)):
#             Input.write((hmm[i]+'\n'))
#         Input.close()

# def searchWithHMM():
#         global protein_list, HMMfile, HMMsearchTBL, HMMsearchDOMTBL, HMMsearchDATABASE
#         hmmsearchLINE = hmmsearchPATH+' --domtblout '+HMMsearchDOMTBL+' '+HMMfile+' '+protein_list
#         print '\n'+hmmsearchLINE
#         subprocess.check_output(hmmsearchLINE, shell=True)

# ###########-------------
# def checkForMIPs(data,knownMIPs):
#     temp = []
#     for i in range(len(data)):
#         if isinstance(data[i],list):
#             temp.extend(data[i])
#         else:
#             temp.append(data[i])
#     temp = list(set(temp))
#     notthere = []
#     isthere = []
#     for mip in knownMIPs:
#         if not mip in temp:
#             notthere.append(mip)
#         else:
#             isthere.append(mip)
#     print '\nfound',len(temp),'proteins and',len(isthere),'known miPs (',len(notthere),'known miPs are not found)'
#     print 'not found:',notthere
		
# def checkCisMIP(mip,anc,List):
#         ancestorgenes = []
#         for agi in anc:
#                 ancestorgenes.append(List[1][List[0].index(agi)])
#         mipgenes = []
#         if isinstance(mip,(list,long)):
#                 for agi in mip:
#                         mipgenes.append(List[1][List[0].index(agi)])
#         else:
#                 mipgenes.append(List[1][List[0].index(mip)])
#         temp = []
#         for agi in mipgenes:
#                 if agi in ancestorgenes:
#                         temp.append('y')
#         if temp == []:
#                 temp.append('n')
#         return temp
		
# def addSTRING(mipinput,ancinput,interactions):
# 	miphits = set(interactions[0]).intersection(mipinput)
# 	anchits = ''
# 	if len(miphits) > 0:#if hit in miPs
# 		anchit = []
# 		for hit in miphits:
# 			for j in range(len(interactions[0])):
# 				if interactions[0][j] == hit:
# 					anchit.append(interactions[1][j])
# 		if len(set(anchit).intersection(ancinput)) > 0:#if hits in ancestors
# 			anchits = (';'.join(set(anchit).intersection(ancinput)))
			
# 	temp = ''
# 	if len(anchits) > 0:
# 		temp = 'y\t'
# 		temp+= ';'.join(miphits)+'\t'
# 		temp+= anchits
# 	else:
# 		temp = 'n\t\t'
# 	return temp










###################################################################################
#   __  __   _____   _____    ______   _____   _   _   _____    ______   _____    #
#  |  \/  | |_   _| |  __ \  |  ____| |_   _| | \ | | |  __ \  |  ____| |  __ \   #
#  | \  / |   | |   | |__) | | |__      | |   |  \| | | |  | | | |__    | |__) |  #
#  | |\/| |   | |   |  ___/  |  __|     | |   | . ` | | |  | | |  __|   |  _  /   #
#  | |  | |  _| |_  | |      | |       _| |_  | |\  | | |__| | | |____  | | \ \   #
#  |_|  |_| |_____| |_|      |_|      |_____| |_| \_| |_____/  |______| |_|  \_\  #
#                                                                                 #
#                                 ___         ___                                 #
#                                |__ \       / _ \                                #
#                        __   __    ) |     | | | |                               #
#                        \ \ / /   / /      | | | |                               #
#                         \ V /   / /_   _  | |_| |                               #
#                          \_/   |____| (_)  \___/                                #
#                                                                                 #
###################################################################################

if __name__ == "__main__":
  logging.info("Starting MIPFINDER v2.0")
  logging.debug(f"Working directory is {os.getcwd()}")
  start_time = datetime.datetime.now() 

  # TODO: Maybe rewrite using ConfigArgParser module rather than configuration file? Would allow to 
  # quickly override paramteres from the command line. Howveer it is not currently important.
  conf = config.Config('config.ini')

  # getKnownMicroproteins(configuration.known_microproteins)
  removeTempDirs()
  createTempDirs()

  fasta_delimiters = [' ','\n','\t','gi|','|','>']
  # TODO (14/05/2019, Valdeko): Document this code
#   if conf.annotation_file:
#     annotation = read_v13.readAnnotation(conf.annotation_file,fasta_delimiters) #[[AGI],[annotation]]

#   protein_list= read_v13.readFasta(conf.protein_list,fasta_delimiters) #[[AGI],[sequence]]

#   if conf.protein_gene_list:
#     protein_gene_list = read_v13.readprotein_gene_list(conf.protein_gene_list,fasta_delimiters)
#   else:
#     protein_gene_list = makeProteinGeneList(protein_list[0])

#   if conf.STRING_database:
#     STRING_interactions = read_v13.readSTRING(conf.STRING_database, conf.STRING_column, conf.STRING_min_score)
#   else:
#     STRING_interactions = None
#   if conf.ipfam_database:
#     ipfam_database_content = read_v13.readiPfam(conf.ipfam_database)#[Pfam]
#   else:
#     ipfam_database_content = None

#   # TODO (14/05/2019, Valdeko): Does this just run the command and then delete the file?
#   if conf.pfam_database and not conf.hmmscan_database:
#     hmmscanLINE = hmmscanPATH+' -o hmmscan_terminal.txt --domtblout '+hmmscan_database+' '+pfam_database+' '+HMMsearchDATABASE#+' >terminal.txt'
#     print hmmscanLINE
#     subprocess.check_output(hmmscanLINE, shell=True)
#     subprocess.check_output(('del hmmscan_terminal.txt'), shell=True)

#   if conf.hmmscan_database != None and os.path.isfile(conf.hmmscan_database) == True:
#     domainsDB = domains(conf.hmmscan_database,HMMsearchDATABASE,fasta_delimiters,e_value_cutoff,c_value_cutoff,hmmscanPATH)


#   blast_database = read_v13.readBlastTAB(conf.blast_database,fasta_delimiters)#[[queryAGI],[[hitAGIs]],[[evalues]],[[starts]],[[stops]]
#   blast_database = eValueFilter(blast_database,conf.blast_cutoff)#[[queryAGI],[[hitAGIs]],[[starts]],[[stops]],[[evalues]]
#   blast_database_all = blast_database
#   blast_database = maxSizeFilter(blast_database[:2],protein_list, conf.maximum_mip_length)#[[queryAGI],[hitAGI]]

#   grouping = makeGroups(blast_database,protein_gene_list)#[[ID,...][[AGI,...],[],[],...]]
#   groups = [[],[]]
#   singlecopy = [[],[]]
#   for i in range(len(grouping[0])):
#           if grouping[0][i].endswith('_1'):
#                   singlecopy[0].append(grouping[0][i])
#                   singlecopy[1].append(grouping[1][i])
#                   if grouping[1][i] == []:
#                     logging.info(f"Error: {grouping[0][i], grouping[1][i]}")
#           else:
#                   groups[0].append(grouping[0][i])
#                   groups[1].append(grouping[1][i])

#   logging.info(f"Found {len(groups[0])} groups and {len(singlecopy[0])} single copy genes")