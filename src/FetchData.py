import pandas as pd
import urllib.request as request
import re


def get_info(response, pattern):
    result = re.search(pattern, response, re.M)
    if result is not None:
        return result.group()
    else:
        return ""


def fetch_data_from_biosample(id):
    url = f'https://www.ncbi.nlm.nih.gov/biosample/?term={id}&report=full&format=text'
    try:
        response = request.urlopen(url).read().decode('utf-8')
    except Exception as e:
        print(f'{id}, Error: {e}')
        return "", "", "", str(e)
    Identifiers = get_info(response, "^Ident.*")
    Organism = get_info(response, "^Organ.*")
    Attributes = get_info(response, "^Att.*")
    Attributes_context = get_info(response, "(^    .*\n)+")
    return Identifiers, Organism, Attributes, Attributes_context


if __name__ == "__main__":
    import os
    path_idlist = "./idlist-Jie.csv"
    save_folder = "./BioSample"
    # Load the ids from a text file that saves the ids
    ids = pd.read_csv(path_idlist, header=None, usecols=[0])

    # Create a folder to store the data
    os.makedirs(save_folder, exist_ok=True)
    # Loop all the ids
    for id in ids[0]:
        identify, organism, attribute, attributes_context = fetch_data_from_biosample(id)
        # Write the data to the file
        with open(f"./BioSample/{id}.txt", "w") as f:
            f.write(identify + "\n")
            f.write(organism + "\n")
            f.write(attribute + "\n")
            f.write(attributes_context + "\n")
