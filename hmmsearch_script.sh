#!/bin/bash

input_folder=$(basename "$3")
output_folder=$1
hmm_file=$(basename "$2")
hmm_name="${hmm_file%.hmm}"

mkdir -p "${output_folder}"

for file in "$input_folder"/*.fasta; do
    # Get the base file name without extension
    file_fasta=$(basename "$file")
    file_name="${file_fasta%.fasta}"
    hmmsearch --domtblout "${output_folder}/${file_name}.${hmm_name}.domtblout" "$hmm_file" "$input_folder"/"$file_fasta"
done 
