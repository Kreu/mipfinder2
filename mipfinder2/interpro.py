import typing

def processTSV(filename: str) -> typing.Dict[str, typing.Set[str]]:
  """Extracts information from the basic InterProScan tab-separated values (TSV) output file.

  Example output, as taken from interproscan github page is as follows:

  P51587	14086411a2cdf1c4cba63020e1622579	3418	Pfam	PF09103	BRCA2, oligonucleotide/oligosaccharide-binding, domain 1	2670	2799	7.9E-43	T	15-03-2013
  P51587	14086411a2cdf1c4cba63020e1622579	3418	ProSiteProfiles	PS50138	BRCA2 repeat profile.	1002	1036	0.0	T	18-03-2013	IPR002093	BRCA2 repeat	GO:0005515|GO:0006302
  P51587	14086411a2cdf1c4cba63020e1622579	3418	Gene3D	G3DSA:2.40.50.140		2966	3051	3.1E-52	T	15-03-2013

  The columns are as follows:
    1. Protein Accession (e.g. P51587)
    2. Sequence MD5 digest (e.g. 14086411a2cdf1c4cba63020e1622579)
    3. Sequence Length (e.g. 3418)
    4. Analysis (e.g. Pfam / PRINTS / Gene3D)
    5. Signature Accession (e.g. PF09103 / G3DSA:2.40.50.140)
    6. Signature Description (e.g. BRCA2 repeat profile)
    7. Start location
    8. Stop location
    9. Score - is the e-value (or score) of the match reported by member database
       method (e.g. 3.1E-52)
    10. Status - is the status of the match (T: true)
    11. Date - is the date of the run
    12. (InterPro annotations - accession (e.g. IPR002093) - optional column; only
        displayed if -iprlookup option is switched on)
    13. (InterPro annotations - description (e.g. BRCA2 repeat) - optional column;
        only displayed if -iprlookup option is switched on)
    14. (GO annotations (e.g. GO:0005515) - optional column; only displayed if
        --goterms option is switched on)
    15. (Pathways annotations (e.g. REACT_71) - optional column; only displayed if
        --pathways option is switched on)

  We are interested only in the protein accession number (column 1) and signature
  accession (column 5). We do not care for the e-value because the member databases
  treat e-values differently and they are not directly comparable. InterProScan 
  itself says that as long as the result is in the results table, it is a real match.

  Args:
    filename (str): Path to a InterProScan results file in TSV format
  
  Returns:
    A dictionary containing protein accession codes as keys (str) and a set of domain
    accession codes as values (set of strings)

  """

  results = {}
  with open(filename, 'r') as f:
    for line in f:
      individual_entries: list = line.split('\t')
      protein_accession: str = individual_entries[0]
      domain_accession: str = individual_entries[4]

      if protein_accession not in results:
        # Using a set provides a convenient way to avoid duplicate domain codes
        results[protein_accession] = set([domain_accession])

      elif protein_accession in results:
        domains: set = results[protein_accession]
        domains.add(domain_accession)

  return results


  

