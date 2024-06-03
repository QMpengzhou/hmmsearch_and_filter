#!/bin/bash

input_folder="proteome"
output_folder="MBD_hmmer_search"

for file in "$input_folder"/*.fasta; do
    # Get the base file name without extension
    file_fasta=$(basename "$file")
    file_name="${file_fasta%.fasta}"
    hmmsearch --domtblout "${output_folder}/${file_name}.MBD.domtblout" MBD.hmm "$input_folder"/"$file_fasta"
done 
