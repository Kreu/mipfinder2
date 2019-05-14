MIPFINDER v2.0

MIPFINDER v2.0 is a tool to detect microproteins within genomes. WIP WIP WIP WIP WIP


Prerequisites

  MIPFINDER v2.0 requires that you have Clustal Omega, HMMER and BLAST+ installed on your system. To do this, run the following commands in your terminal

	sudo apt install clustalo
	sudo apt install hmmer
	sudo apt install ncbi-blast+

	MIPFINDER v2.0 has been developed using Python 3.6.7 but in theory every version above 3.5 should work.


Configuration options

	Here are all the configuration options in config.ini explained

	Section [MIPFINDER] 
		species_prefix:
		maximum_mip_length:
		minimum_ancestor_length:
		blast_cutoff:
		overlap_cutoff:
		e_value_cutoff:
		c_value_cutoff:

		mostSIMILARcutoff:
		open_gap_penalty:
		maxMIPgroupSIZE:
		dropfile:

	Section [DATA]
		organism_protein_list: FASTA file containing all the known proteins in the organism of interest
		hmmscan_database :
		pfam_database:
		ipfam_database:
		protein_gene_list:
		annotation_file:
		known_microproteins: A list of all known microproteins

	Section [PATH]
		#Paths to the appropriate exexutables
		blast_path:
		clustalo_path:
		hmmsearch_path:
		hmmbuild_path:
		hmmscan_path:

	Section [STRING]
		STRING_database:
		STRING_column:
		STRING_min_score:



