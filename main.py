import argparse
import subprocess
import os


def extract_pipe(ev, op_pf, hf, sdb):
    arguments = [str(ev), op_pf, hf, sdb]
    extraction_script_path = "./extraction_script.sh"
    command = [extraction_script_path] + arguments
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("program executed successfully")
    else:
        print("program failed with return code:", result.returncode)


def search_pipe(ev, op, hf, sdb):  # run script with hmmsearch
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
        extract_pipe(ev, output_prefix, hf, sdb)
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
                      help="Prefix in output directory, default is hmmfile prefix + hmmer_search")
parser_f.add_argument("hmmfile", metavar="hmmfile", type=str, help="the query HMM profile")
parser_f.add_argument("seqdb", metavar="seqdb", type=str,
                      help="the target directory with sequences in fasta format")

args = parser.parse_args()

if args.command == "search":
    search_pipe(args.evalue, args.output_prefix, args.hmmfile, args.seqdb)
