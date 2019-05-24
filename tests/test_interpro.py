import unittest
import os

import sys
# Hacky way of doing it, for some reason relative imports don't work
sys.path.insert(0, "/home/troy/Documents/git/mipfinder2/mipfinder2")

import interpro

class Test_processTSV (unittest.TestCase):
  def setUp(self):
    with open("test.tsv", 'w') as f:
      f.write("P51587\t14086411a2cdf1c4cba63020e1622579\t3418\tPfam\tPF09103\tBRCA2, oligonucleotide/oligosaccharide-binding, domain 1\t2670\t2799\t7.9E-43	T	15-03-2013\n")
      f.write("P51587\t14086411a2cdf1c4cba63020e1622579\t3418\tProSiteProfiles\tPS50138	BRCA2 repeat profile.\t1002\t1036\t0.0\tT\t18-03-2013\tIPR002093\tBRCA2 repeat\tGO:0005515|GO:0006302\n")
      f.write("P51587\t14086411a2cdf1c4cba63020e1622579\t3418\tGene3D\tG3DSA:2.40.50.140\t2966\t3051\t3.1E-52\tT\t15-03-2013")

  def test_normal_input(self):
    expected_output = {"P51587": {"PF09103", "PS50138", "G3DSA:2.40.50.140"}}
    self.assertEqual(interpro.processTSV("test.tsv"), expected_output)

  def tearDown(self):
    os.remove("test.tsv")
