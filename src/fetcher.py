from scidownl import scihub_download
import os


# Pipelined function to get the DOIs from the files
def get_dois_from_file(file_path):

    # Get all the files in the directory
    directory = '../data/unfetched_dois'
    files = os.listdir(directory)
    dois = []

    for file in files:
        filepath = os.path.join(directory, file)
        print("Extracting DOIs from file: ", file, "... ")
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                print("Returning partial results", line.strip(), "... ")
                yield line.strip()
        print("Extracting DOIs from file: ", file, " : DONE ")
        break



#Stopper with upperbound 3 papers for testing
def main():

    papers_number = 0
    dois = get_dois_from_file('../data/unfetched_dois')

    for doi in get_dois_from_file(dois):

        #Call scihub api to download the paper
        paper = "https://doi.org/" + doi
        paper_type = "doi"
        target_directory = f"../data/papers/{doi.replace('/', '_')}.pdf"
        proxies = {
            'http': 'socks5://127.0.0.1:7890'
        }
        scihub_download(paper, paper_type=paper_type, out=target_directory, proxies=proxies)

        papers_number += 1
        if papers_number == 3:
            break

if __name__ == "__main__":
    main()