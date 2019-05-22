# TODO: This is just a test for unittest, will write actual tests when I have functions in the main 
# program.

import unittest
import os
import sys

# Hacky way of doing it, for some reason relative imports don't work
# sys.path.insert(0, "/media/troy/Data/Valdeko/documents/git/mipfinder2/mipfinder2")


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


if __name__ == '__main__':
  unittest.main()