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
    self.header_with_no_gene_name = ">sp|P0CG48|UBC_HUMAN Polyubiquitin-C OS=Homo sapiens OX=9606 PE=1 SV=3"
  
  def test_extract_single_identifier(self):
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["DB"]), ["sp"])
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["ID"]), ["P05783"])
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["EN"]), ["K1C18_HUMAN"])
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["PN"]), ["Keratin, type I cytoskeletal 18"])
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["OS"]), ["Homo sapiens"])
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["OX"]), ["9606"])
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["GN"]), ["KRT18"])
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["PE"]), ["1"])
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["SV"]), ["2"])

  def test_multiple_identifiers(self):
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["DB", "EN"]), ["sp", "K1C18_HUMAN"])
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["ID", "SV"]), ["P05783", "2"])
    self.assertEqual(fasta.extractUniprotHeader(self.header, ["EN", "ID"]), ["K1C18_HUMAN", "P05783"])

  def test_extract_single_no_gene_name(self):
    self.assertEqual(fasta.extractUniprotHeader(self.header_with_no_gene_name, ["DB"]), ["sp"])
    self.assertEqual(fasta.extractUniprotHeader(self.header_with_no_gene_name, ["ID"]), ["P0CG48"])
    self.assertEqual(fasta.extractUniprotHeader(self.header_with_no_gene_name, ["EN"]), ["UBC_HUMAN"])
    self.assertEqual(fasta.extractUniprotHeader(self.header_with_no_gene_name, ["PN"]), ["Polyubiquitin-C"])
    self.assertEqual(fasta.extractUniprotHeader(self.header_with_no_gene_name, ["OS"]), ["Homo sapiens"])
    self.assertEqual(fasta.extractUniprotHeader(self.header_with_no_gene_name, ["OX"]), ["9606"])
    self.assertEqual(fasta.extractUniprotHeader(self.header_with_no_gene_name, ["PE"]), ["1"])
    self.assertEqual(fasta.extractUniprotHeader(self.header_with_no_gene_name, ["SV"]), ["3"])

  def test_extract_GN_from_no_GN_string(self):
    self.assertEqual(fasta.extractUniprotHeader(self.header_with_no_gene_name, ["GN"]), [""])

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


class Test_extractAraportHeader (unittest.TestCase):

  def setUp(self):
    self.header = ">AT5G61190.10 | putative endonuclease or glycosyl hydrolase with C2H2-type zinc finger domain-containing protein | Chr5:24615480-24619886 FORWARD LENGTH=1010 | 201606"

  def test_valid_header(self):
    self.assertEqual(fasta.extractAraportHeader(self.header), ["AT5G61190", "10", "putative endonuclease or glycosyl hydrolase with C2H2-type zinc finger domain-containing protein"])
                                                      