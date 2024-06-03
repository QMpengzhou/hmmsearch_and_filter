#!/bin/bash

input_folder="MBD_hmmer_search"

for file in "$input_folder"/*.MBD.domtblout; do
    file_domtblout=$(basename "$file")
    file_name="${file_domtblout%.MBD.domtblout}"
    cat "$input_folder"/"$file_domtblout" | grep -v "#" | tr -s " " "\t" | awk '$7 < 0.0001 && $12 < 0.0001' | cut -f 1 | sort -u > "${input_folder}/${file_name}.MBD.ids"
    seqkit grep -f "${input_folder}/${file_name}.MBD.ids" "proteome/${file_name}.fasta" > "${input_folder}/${file_name}.MBD.fasta"
done 
