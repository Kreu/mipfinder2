"""miPFinder version 2.0

WIP WIP WIP WIP
"""

#Initialise Argparser
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
parser.add_argument('-l', '--IDlist', dest='IDlist', default=knownMIP, help='list of IDs that will be searched against miP candidate protein IDs and reported in the final result table [string, semicolon-separated list] (22 known Ath miPs)') 

args = vars(parser.parse_args())
