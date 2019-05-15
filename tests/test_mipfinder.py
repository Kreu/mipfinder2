# TODO: This is just a test for unittest, will write actual tests when I have functions in the main 
# program.

import unittest
import os

import sys
# Hacky way of doing it, for some reason relative imports don't work
sys.path.insert(0, "/home/troy/Documents/git/mipfinder2/mipfinder2")

import mpf

class TestextractFastaRecord (unittest.TestCase):

	def setUp(self):
		pass

	def testValidInput(self):
		with open("test_fasta.txt", 'w') as f:
			f.write(">1\nTEST1\n")
			f.write(">2\nTEST2\n")
			f.write(">3\nTEST3\n")
			f.write(">4\nTEST4")
		
		expected_results = {">1": "TEST1",
												">2": "TEST2",
												">3": "TEST3",
												">4": "TEST4"
		}

		self.assertEqual(mpf.extractFastaRecords("test_fasta.txt"), expected_results)
		os.remove("test_fasta.txt")

	def testMalFormedInput(self):
		with open("test_fasta.txt", 'w') as f:
			f.write("Erroneous line\n")
			f.write(">1\nTEST1\n")
			f.write(">2\nTEST2\n")
			f.write(">3\nTEST3\n")
			f.write(">4\nTEST4")
		
		expected_results = {">1": "TEST1",
												">2": "TEST2",
												">3": "TEST3",
												">4": "TEST4"
		}

		self.assertEqual(mpf.extractFastaRecords("test_fasta.txt"), expected_results)
		os.remove("test_fasta.txt")

class TestgetKnownMicroproteins (unittest.TestCase):

	def setUp(self):
		self.expected_list = ["MIP1", "MIP2", "MIP3"]
		pass

	def testNormalFile(self):
		with open("test_mip.txt", "w") as f:
			f.write("MIP1\nMIP2\nMIP3")
		
		self.assertListEqual(mpf.getKnownMicroproteins("test_mip.txt"), self.expected_list)
		os.remove("test_mip.txt")

# 	def test_string(self):
# 		with self.assertRaises(TypeError):
# 			self.assertEqual(mpf.addOne("Invalid"))

# 		#The following code won't work, left in here as a historical reminder. This is because
# 		#unittest's assertRaises needs a wrapper to be able to access the raised exception.
# 		#self.assertRaises(ValueError, sequencer.FilterSequence, nucleotides, scores, 20)

if __name__ == '__main__':
	unittest.main()