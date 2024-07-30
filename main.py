import argparse
import subprocess
import os
from counting import counting_pipe


def extract_pipe(ev, op_pf, me, c, hf, sdb):
    merged_fasta = "true" if me else "false"
    arguments = [str(ev), op_pf, merged_fasta, hf, sdb]
    extraction_script_path = "./extraction_script.sh"
    command = [extraction_script_path] + arguments
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        if c:
            table = counting_pipe(op_pf, hf)
            hf = hf.split(".")[0]
            output_file = f"hits_counting_{hf}.tsv"
            table.to_csv(output_file, sep="\t", index=False)
        print("program executed successfully")
    else:
        print("program failed with return code:", result.returncode)


def search_pipe(ev, op, me, c, hf, sdb):  # run script with hmmsearch
    if op is not None:
        output_prefix = op
    else:
        output_prefix, _ = os.path.splitext(hf)
        output_prefix += "_hmmer_search"
    hmmsearch_script_path = "./hmmsearch_script.sh"
    arguments = [output_prefix, hf, sdb]
    command = [hmmsearch_script_path] + arguments
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        extract_pipe(ev, output_prefix, me, c, hf, sdb)
    else:
        print("program failed with return code:", result.returncode)


# parser commands below
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", help="sub-commands")

# first sub-command
parser_f = subparsers.add_parser("search", help="perform hmmsearch and filter the hits based on threshold")
parser_f.add_argument("-e", "--evalue", metavar="", dest="evalue", type=float, default=0.0001,
                      help="E-value threshold to filter hits, default is 0.0001")
parser_f.add_argument("-o", "--output_prefix", type=str, metavar="", dest="output_prefix",
                      help="Prefix in output directory, default is hmmfile prefix + \"hmmer_search\"")
parser_f.add_argument("-m", "--merged", action="store_true",
                      help="An optional argument to provide a merged fasta file for further multiple sequence "
                           "alignment.")
parser_f.add_argument("-c", "--counting", action="store_true",
                      help="An optional argument to provide a table with hits per species according to their taxonomy")
parser_f.add_argument("hmmfile", metavar="hmmfile", type=str, help="the query HMM profile")
parser_f.add_argument("seqdb", metavar="seqdb", type=str,
                      help="the target directory with sequences in fasta format")

args = parser.parse_args()

if args.command == "search":
    search_pipe(args.evalue, args.output_prefix, args.merged, args.counting, args.hmmfile, args.seqdb)
