import argparse


def search_pipe(ev, op, hf, sdb):
    print(ev, op, hf, sdb)


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
