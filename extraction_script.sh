#!/bin/bash

evalue=$1
input_folder=$2
merged_fasta=$3
hmm_file=$(basename "$4")
hmm_name="${hmm_file%.hmm}"
seq_db=$5

for file in "$input_folder"/*.domtblout; do
    file_domtblout=$(basename "$file")
    file_name="${file_domtblout%."$hmm_name".domtblout}"
    cat "$input_folder"/"$file_domtblout" | grep -v "#" | tr -s " " "\t" | awk -v evalue="$evalue" '$7 < evalue && $12 < evalue' | cut -f 1 | sort -u > "${input_folder}/${file_name}.${hmm_name}.ids"
    seqkit grep -f "${input_folder}/${file_name}.${hmm_name}.ids" "${seq_db}/${file_name}.fasta" > "${input_folder}/${file_name}.${hmm_name}.fasta"
done
if [ "$merged_fasta" = "true" ]; then
  seqkit concat --full "${input_folder}"/*."${hmm_name}".fasta > "merged_${hmm_name}.fasta"
fi
