def stringToUniProt(string_protein_info: str):
    """Match STRING IDs to UniProt IDs.

    This uses an organism-specific file from STRING database from here:
    https://string-db.org/cgi/download.pl?sessionId=QSuugpq1Ea5l&species_text=Arabidopsis+thaliana

    Specifically, this one:
    3702.protein.info.v11.0.txt.gz (2.4 Mb) - list of STRING proteins incl. their display names and descriptions

    This file maps all of STRING protein IDs to different database IDs. Because
    mipfinder is written to work with UniProt IDs, we only extract those.

    The column contents differ for different databases but for the UniProt lines
    the first column is the STRING identifier and the second column is the UniProt
    identifier.

    Args:
        string_protein_info (str): File containing organism-specific list of STRING IDs and
                                   descrpitions of how they relate to other databases. See
                                   above where to download this file.

    Returns:
        A dictionary with STRING IDs as keys and UniProt IDs as string values.
        Each key maps to exactly one UniProt ID.
        
    """
    id_map = {}
    with open(string_protein_info) as f:
        line_count = 1
        for line in f:
            # The line count numbers are where the UniProt IDs are. Could be done
            # with regex but this way is easier (or this is way easier ;))
            # Might break if the format changes though.
            if (line_count >= 712094) and (line_count <= 765105):
                tokens = line.split('\t')

                # All STRING aliases in an organism database are suffixed with the
                # organism identifier (3702 for A. thaliana) in the following format:
                # 3702.AT1G55020.1	Q9FZ30
                # We are only interested in the protein ID.
                string_alias = tokens[0][5:]

                uniprot_alias = tokens[1]

                # Some of the UniProt IDs have suffixes even though they map to
                # the same STRING database alias, so we filter them out to
                # remove the redundancy.
                if (uniprot_alias.find('_') == -1): # -1 indicates substring not found
                    id_map[string_alias] = uniprot_alias
            line_count += 1
    return id_map

def writeProteinAliases(aliases: dict, output: str):
    """Writes the STRING to UniProt ID mappings into a file.

    Args:
        aliases (dict)
    """
    with open("string_to_uniprot_ids.txt", 'w') as x:
        for string_alias, uniprot_alias in aliases.items():
            x.write(f"{string_alias}\t{uniprot_alias}\n")


id_map = extractProteinAliases("3702.protein.aliases.v11.0.txt")

writeProteinAliases(id_map)
