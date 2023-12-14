import re, os

def parse_header(header):
    # KIR number and DL number/letter 
    kir_match = re.search(r'KIR(\d+)', header)
    dl_match = re.search(r'(?<=D)[A-Za-z]?\d*', header)
    
    kir_num = kir_match.group(1) if kir_match else ""
    dl = dl_match.group() if dl_match else ""
    
    return kir_num, dl

def kir_split(filename):
    gene_seqs = {}

    with open(filename, 'r') as input_file:
        cur_name = None
        data = []

        for s in input_file:
            s = s.strip()
            if s.startswith('>'): # Header, get the name
                header = s[1:]
                kir_num, dl = parse_header(header)
                full_header = f"KIR{kir_num}D{dl}"

                if cur_name is not None:
                    # Save the previous gene's data to a file
                    if cur_name in gene_seqs:
                        gene_seqs[cur_name].extend(data)
                    else:
                        gene_seqs[cur_name] = data
                cur_name = full_header
                data = [s]
            else:
                data.append(s) # Append seqs

        if cur_name is not None:
            if cur_name in gene_seqs:
                gene_seqs[cur_name].extend(data)
            else:
                gene_seqs[cur_name] = data

    for gene_name, data in gene_seqs.items():
        # Parse if name contains a letter after D (e.g.,DP1,...)
        if re.search(r'D[A-Za-z]', gene_name):
            kir_num, dl = parse_header(gene_name)
            output_filename = f"{gene_name}.fa"
            with open(output_filename, 'w') as output_file:
                output_file.write("\n".join(data))

filename = "KIR.fa"
kir_split(filename)
