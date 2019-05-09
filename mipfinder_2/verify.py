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






