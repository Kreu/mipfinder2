import unittest

import protein

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