# TODO: This is just a test for unittest, will write actual tests when I have functions in the main 
# program.

import mipfinder.mipfinder as mpf

import unittest
import os

import sys
sys.path.append(os.getenv('PWD'))

# class TestAddOne(unittest.TestCase):

# 	def setUp(self):
# 		pass

# 	def test_one(self):
# 	  self.assertEqual(mpf.addOne(1), 2)

# 	def test_two(self):
# 		self.assertEqual(mpf.addOne(2), 3)

# 	def test_string(self):
# 		with self.assertRaises(TypeError):
# 			self.assertEqual(mpf.addOne("Invalid"))

# 		#The following code won't work, left in here as a historical reminder. This is because
# 		#unittest's assertRaises needs a wrapper to be able to access the raised exception.
# 		#self.assertRaises(ValueError, sequencer.FilterSequence, nucleotides, scores, 20)

if __name__ == '__main__':
	unittest.main()