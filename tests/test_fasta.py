import os
import re
import sys
import unittest


# Hacky way of doing it, for some reason relative imports don't work
sys.path.insert(0, "/home/troy/Documents/git/mipfinder2/mipfinder2")
import fasta  # Has to be after sys.path.insert

class Test_extractRecords (unittest.TestCase):

  def setUp(self):
    pass

  def test_valid_input(self):
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

    self.assertEqual(fasta.extractRecords("test_fasta.txt"), expected_results)
    os.remove("test_fasta.txt")

  def test_extra_line_in_beginning(self):
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

    self.assertEqual(fasta.extractRecords("test_fasta.txt"), expected_results)
    os.remove("test_fasta.txt")

  def test_extra_line_in_end(self):
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

    self.assertEqual(fasta.extractRecords("test_fasta.txt"), expected_results)
    os.remove("test_fasta.txt")


class Test_extractIdentifier (unittest.TestCase):
  def setUp(self):
    self.header = ">sp|P05783|K1C18_HUMAN Keratin, type I cytoskeletal 18 OS=Homo sapiens OX=9606 GN=KRT18 PE=1 SV=2"
  
  def test_extract_single_identifier(self):
    self.assertEqual(fasta.extractIdentifier(self.header, ["DB"]), ["sp"])
    self.assertEqual(fasta.extractIdentifier(self.header, ["ID"]), ["P05783"])
    self.assertEqual(fasta.extractIdentifier(self.header, ["EN"]), ["K1C18_HUMAN"])
    self.assertEqual(fasta.extractIdentifier(self.header, ["PN"]), ["Keratin, type I cytoskeletal 18"])
    self.assertEqual(fasta.extractIdentifier(self.header, ["OS"]), ["Homo sapiens"])
    self.assertEqual(fasta.extractIdentifier(self.header, ["OX"]), ["9606"])
    self.assertEqual(fasta.extractIdentifier(self.header, ["GN"]), ["KRT18"])
    self.assertEqual(fasta.extractIdentifier(self.header, ["PE"]), ["1"])
    self.assertEqual(fasta.extractIdentifier(self.header, ["SV"]), ["2"])

  def test_multiple_identifiers(self):
    self.assertEqual(fasta.extractIdentifier(self.header, ["DB", "EN"]), ["sp", "K1C18_HUMAN"])
    self.assertEqual(fasta.extractIdentifier(self.header, ["ID", "SV"]), ["P05783", "2"])
    self.assertEqual(fasta.extractIdentifier(self.header, ["EN", "ID"]), ["K1C18_HUMAN", "P05783"])

class Test_extractUniprotID (unittest.TestCase):

  def setUp(self):
    self.fasta_header = ">sp|Q9C5U0|AHK4_ARATH Histidine kinase 4 OS=Arabidopsis thaliana OX=3702 GN=AHK4 PE=1 SV=1"
    self.expected_output = "Q9C5U0"

  def test_uniprot_kb_header(self):
    self.assertEqual(fasta.extractUniprotID(self.fasta_header, 3), self.expected_output)


class Test_tokenise (unittest.TestCase):

  def test_delimiters_present(self):
    string = "This! Is another example!"
    self.assertEqual(fasta.tokenise(string, "[! ]+"), ["This", "Is", "another", "example"])

  def test_no_delimiters_present(self):
    string = "This is an! Example. of no matching delimiters."
    self.assertEqual(fasta.tokenise(string, "[?,]+"), ["This is an! Example. of no matching delimiters."])

  def test_backslash(self):
    string = "String \ with a single backslash"
    self.assertEqual(fasta.tokenise(string, r"[\\ ]+"), ["String", "with", "a", "single", "backslash"])

  def test_forward_slash(self):
    string = "String with /a forward slash"
    self.assertEqual(fasta.tokenise(string, "[/ ]+"), ["String", "with", "a", "forward", "slash"])

  def test_hyphen(self):
    string = "A hyphenated-example."
    self.assertEqual(fasta.tokenise(string, "[\- ]+"), ["A", "hyphenated", "example."])
