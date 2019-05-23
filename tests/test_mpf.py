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

if __name__ == '__main__':
  unittest.main()