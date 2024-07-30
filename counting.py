import pandas as pd
import os


def counting_pipe(op_pf, hf):
    directory_name = op_pf
    directory_path = os.path.abspath(directory_name)
    hf = hf.split(".")[0]
    data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".ids"):
            species_name = filename.split(".")[0]
            file_path = os.path.join(directory_path, filename)
            number_of_hits = hit_counting(file_path)
            data.append([species_name, number_of_hits])
    final_df = pd.DataFrame(data, columns=["Species", f"{hf}"])
    reordered_df = reordering(final_df)
    return reordered_df


def hit_counting(file_path):
    with open(file_path, "r") as file:
        return sum(1 for _ in file)


def reordering(df):
    taxon_table = pd.read_csv("taxon_table.tsv", sep="\t")
    reordered_df = pd.merge(taxon_table, df, on="Species", how="inner")
    missing_species = set(df["Species"]) - set(taxon_table["Species"])
    if missing_species:
        print("warning: these species are not find in taxon table:")
        print(missing_species)
    return reordered_df
