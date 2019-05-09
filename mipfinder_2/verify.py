"""Checks whether all the appropriate programs have been installed properly

Verify whether the tools required for miPFinder to work properly have been installed. If not, raises
an EnvironmentError.

TODO: Is EnvironmentError most appropriate?
"""

import configparser

configuration = configparser.ConfigParser()   
configFilePath = r'c:\abc.txt'
configParser.read(configFilePath)

######ARGUMENT PARSER & VERIFICATION
os.environ["CYGWIN"] = "nodosfilewarning" #avoid hmmer warnings
currentPATH = os.getcwd().replace('\\','/')
def isFile(string):
    if os.path.isfile(string) == False:
        msg = "%r does not exist" % string
        raise argparse.ArgumentTypeError(msg)
    return string
def isBlast(string):
	output = open('testtest.txt','w')
	output.write('>1\nCRTTATPMWRG\n>2\nCNTTKTPLWRS')
	output.close()
	try:
		subprocess.check_output(('\"'+string+'\"makeblastdb.exe -dbtype prot -in testtest.txt'), shell=True)
	except subprocess.CalledProcessError, e:
		msg = "%r does not point to blast folder (tested for makeblastdb.exe)" % string
		subprocess.check_output(('del testtest.*'), shell=True)
		raise argparse.ArgumentTypeError(msg)
	return string
def isClustal(string):
	output = open('testtest.txt','w')
	output.write('>1\nCRTTATPMWRG\n>2\nCNTTKTPLWRS')
	output.close()
	try:
		subprocess.check_output(('\"'+string+'\"clustalw2.exe -INFILE=testtest.txt -ALIGN -TYPE=PROTEIN -OUTFILE=testtest.txt'), shell=True)
	except subprocess.CalledProcessError, e:
		msg = "%r does not point to clustalw2 folder" % string
		subprocess.check_output(('del testtest.*'), shell=True)
		raise argparse.ArgumentTypeError(msg)
	return string
def isHmmer(string):
	output = open('testtest.txt','w')
	output.write('1 MKVRSSVKKMCEFCKTVKRRGR\n2 MKIRASVRKICEKCRLIRRRGR')
	output.close()
	try:
		subprocess.check_output(('\"'+string+'hmmbuild.exe\" --amino testtest.txt '+currentPATH+'/testtest.txt'), shell=True)
	except subprocess.CalledProcessError, e:
		msg = "%r does not point to Hmmer folder (tested for hmmbuild.exe)"
		subprocess.check_output(('del testtest.*'), shell=True)
		raise argparse.ArgumentTypeError(msg)
	subprocess.check_output(('del testtest.*'), shell=True)
	return string
def isInt(string):
	try:
		int(string)
	except:
		msg = "%r is not recognized as Integer, but must be!" % string
		raise argparse.ArgumentTypeError(msg)
	return int(string)
def isFloat(string):
	try:
		float(string)
	except:
		msg = "%r is not recognized as Float, but must be!" % string
		raise argparse.ArgumentTypeError(msg)
	return float(string)


print '\n'
parser = argparse.ArgumentParser(
description='MiPFinder v1 - a script to produce a list enriched in microProteins. - Straub, D; Wenkel, S (2016): \"Cross-species genome-wide identification of evolutionary conserved microProteins.\"',
epilog='Only -f is required, however, if blast/clustalw/hmmer are not in evironment variables, -B/-C/-H are required too. Specify path using "/" instead of "\\". \nDefault values are in round brackets.')
parser.add_argument('-f', '--fasta', dest='fastadb', help='fasta file of all proteins, must be in the working directory! Recommended: http://www.phytozome.net, http://www.ensembl.org/, ftp://ftp.ncbi.nlm.nih.gov/refseq ->protein.faa files', required=True, type=isFile)
parser.add_argument('-s', '--species', dest='species', default='NA', help='Prefix for output files [string] (NA)')
parser.add_argument('-p', '--ProteinGeneList', dest='ProteinGeneList', help='List of identifiers of protein and genes. column1: protein_id, column2: gene_id; tab separated', type=isFile)
parser.add_argument('-a', '--annotation', dest='annotationdb', help='Annotation file for fasta file. column1: protein_id, column2: description; tab separated', type=isFile)
parser.add_argument('-m', '--hmmscanDB', dest='hmmscandb', help='Domain annotation file hmmscan, is created if not specified', type=isFile)
parser.add_argument('-B', '--blast', dest='blastPATH', default='', help='path/to/blast-folder/, available at ftp://ftp.ncbi.nih.gov/blast/executables/blast+/', type=isBlast) 
parser.add_argument('-C', '--clustalw', dest='ClustalPATH', default='', help='path/to/clustalw2-folder/, available at http://www.clustal.org/clustal2/', type=isClustal) 
parser.add_argument('-H', '--hmm', dest='hmmPATH', default='', help='path/to/hmmsearch-folder/, available at http://hmmer.org/', type=isHmmer)
parser.add_argument('-S', '--STRING', dest='STRINGdb', help='STRING v10 detailed protein interaction file. XXXX.protein.links.detailed.v10.txt, available at http://string-db.org/cgi/download.pl', type=isFile)
parser.add_argument('-d', '--PfamA', dest='PfamAdb', help='Pfam-database.hmm, available at ftp://ftp.ebi.ac.uk/pub/databases/Pfam/', type=isFile)
parser.add_argument('-i', '--iPfam', dest='iPfamdb', help='iPfam-database.tsv, available at http://www.ipfam.org/. Merge homodomain and heterodomain interaction file.', type=isFile)
parser.add_argument('-M', '--maxMIPlength', dest='miPmaxlength', default=140, help='Maximum length of a microProtein in aminoacids [integer] (140)', type=isInt) 
parser.add_argument('-A', '--minANCESTORlength', dest='ancestorminlength', default=250, help='Minimum length of a microProtein ancestor in aminoacids [integer] (250)', type=isInt) 
parser.add_argument('-L', '--blastCUTOFF', dest='blastCUTOFF', default=1e-3, help='E-value cutoff for Blast search [0-1, float] (1e-3)', type=isFloat) 
parser.add_argument('-O', '--overlapCUTOFF', dest='overlapCUTOFF', default=0.6, help='Pfam domains: minimum overlap of a microProtein with an annotated domain; 0.5=miP matches at least half the domain, [0-1, float] (0.6)', type=isFloat) 
parser.add_argument('-E', '--evalueCUTOFF', dest='evalueCUTOFF', default=0.1, help='E-value cutoff for HMMscan and HMMsearch [0-1, float] (0.1)', type=isFloat) 
parser.add_argument('-V', '--cvalueCUTOFF', dest='cvalueCUTOFF', default=0.05, help='c-Evalue cutoff for HMMscan and HMMsearch [0-1, float] (0.05)', type=isFloat)
parser.add_argument('-c', '--STRINGcolumn', dest='STRINGcolumn', default=9, help='Column in STRING v10 file that is compared to STRINGminscore. E.g. 9=combined score, 6=experimental, 8=textmining; [2-9, integer] (9)', type=isInt)
parser.add_argument('-e', '--STRINGminscore', dest='STRINGminscore', default=400, help='Minimum score in STRING v10 file in column STRINGcolumn. E.g. 700=high confidence, 400=medium confidence; [0-1000, integer] (400)', type=isInt)
knownMIP = 'AT5G39860.1;AT1G26945.1;AT5G15160.1;AT3G28857.1;AT1G74500.1;AT3G47710.1;AT4G15248.1;AT3G21890.1;AT3G28917.1;AT1G74660.1;AT1G18835.1;AT1G14760.2;AT3G58850.1;AT2G42870.1;AT1G01380.1;AT2G30424.1;AT5G53200.1;AT2G30420.1;AT2G30432.1;AT2G46410.1;AT4G01060.1;AT3G52770.1'
parser.add_argument('-l', '--IDlist', dest='IDlist', default=knownMIP, help='list of IDs that will be searched against miP candidate protein IDs and reported in the final result table [string, semicolon-separated list] (22 known Ath miPs)') 
args = vars(parser.parse_args())