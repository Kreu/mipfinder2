import unittest
import sys
# Hacky way of doing it, for some reason relative imports don't work
sys.path.insert(0, "/home/troy/Documents/git/mipfinder2/mipfinder2")

import protein

class Test_filterBySize (unittest.TestCase):

  def setUp(self):
    self.proteins = {"30": "AGCTAGCATGCTACTAGTCGTAGCTATGCG",
                    "15": "AGCTGTAGCTAGATG",
                    "14": "AGCTGTAGCTAGAT",
                    "5": "AGTGG",
                    "0": ""}

    self.five_plus = {"30": "AGCTAGCATGCTACTAGTCGTAGCTATGCG",
                    "15": "AGCTGTAGCTAGATG",
                    "14": "AGCTGTAGCTAGAT",
                    "5": "AGTGG"}

    self.fourteen_plus = {"30": "AGCTAGCATGCTACTAGTCGTAGCTATGCG",
                        "15": "AGCTGTAGCTAGATG",
                        "14": "AGCTGTAGCTAGAT"}

    self.fifteen_plus = {"30": "AGCTAGCATGCTACTAGTCGTAGCTATGCG",
                        "15": "AGCTGTAGCTAGATG"}

    self.thirty = {"30": "AGCTAGCATGCTACTAGTCGTAGCTATGCG"}

    self.fifteen_minus = {"15": "AGCTGTAGCTAGATG",
                        "14": "AGCTGTAGCTAGAT",
                        "5": "AGTGG",
                        "0": ""}

    self.fourteen_minus = {"14": "AGCTGTAGCTAGAT",
                          "5": "AGTGG",
                          "0": ""}

    self.five_minus = {"5": "AGTGG",
                    "0": ""}

    self.zero = {"0": ""}

    self.fourteen_fifteen = {"15": "AGCTGTAGCTAGATG",
                            "14": "AGCTGTAGCTAGAT"}

  def test_bigger_bounds(self):
    self.assertEqual(protein.filterBySize(self.proteins, 20, 35), self.thirty)

  def test_max_bound_equals_length(self):
    self.assertEqual(protein.filterBySize(self.proteins, 20, 30), self.thirty)
    self.assertEqual(protein.filterBySize(self.proteins, 0, 15), self.fifteen_minus)
    self.assertEqual(protein.filterBySize(self.proteins, 0, 14), self.fourteen_minus)

  def test_min_bound_equals_length(self):
    self.assertEqual(protein.filterBySize(self.proteins, 30, 35), self.thirty)
    self.assertEqual(protein.filterBySize(self.proteins, 14, 35), self.fourteen_plus)
    self.assertEqual(protein.filterBySize(self.proteins, 15, 35), self.fifteen_plus)

  def test_same_bounds(self):
    self.assertEqual(protein.filterBySize(self.proteins, 30, 30), self.thirty)

  def test_smaller_bounds(self):
    self.assertEqual(protein.filterBySize(self.proteins, 6, 15), self.fourteen_fifteen)

  def test_no_bounds(self):
    self.assertEqual(protein.filterBySize(self.proteins), self.proteins)
