# TODO: This is just a test for unittest, will write actual tests when I have functions in the main 
# program.

import unittest
import os
import sys
# Hacky way of doing it, for some reason relative imports don't work
sys.path.insert(0, "/home/troy/Documents/git/mipfinder2/mipfinder2")

import protein
import mpf

# 	def test_string(self):
# 		with self.assertRaises(TypeError):
# 			self.assertEqual(proteinj.addOne("Invalid"))

# 		#The following code won't work, left in here as a historical reminder. This is because
# 		#unittest's assertRaises needs a wrapper to be able to access the raised exception.
# 		#self.assertRaises(ValueError, sequencer.FilterSequence, nucleotides, scores, 20)


class TestgetKnownMicroproteins (unittest.TestCase):

  def setUp(self):
    self.expected_list = ["MIP1", "MIP2", "MIP3"]
    pass

  def test_valid_input(self):
    with open("test_mip.txt", "w") as f:
      f.write("MIP1\nMIP2\nMIP3")
    
    self.assertListEqual(mpf.getKnownMicroproteins("test_mip.txt"), self.expected_list)
    os.remove("test_mip.txt")


# TODO: VSC is not discovering this test for some reason
class TestisLengthBetween (unittest.TestCase):

  def setUp(self):
    self.long_sequence = "AGCTAGCATGCTACTAGTCGTAGCTATGCG"
    self.short_sequence = "AGTGA"
    self.empty_sequence = ""

  def test_bigger_bounds(self):
    self.assertEqual(protein.isLengthBetween(self.long_sequence, 20, 50), True)
    self.assertEqual(protein.isLengthBetween(self.short_sequence, 0, 6), True)

  def test_same_bounds(self):
  	self.assertEqual(protein.isLengthBetween(self.long_sequence, 0, 0), False)
  	self.assertEqual(protein.isLengthBetween(self.long_sequence, 30, 30), True)
  	self.assertEqual(protein.isLengthBetween(self.empty_sequence, 0, 0), True)

  def test_smaller_bounds(self):
    self.assertEqual(protein.isLengthBetween(self.short_sequence, 2, 4), False)



if __name__ == '__main__':
  unittest.main()