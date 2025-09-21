# It's a simple utility to download all data (pdfs) from the sources json 

# A BIG NOTE:
# src12 - Eaton safety manual... is too big for the utility to write, please get it manually and save in DATA PATH as src12.pdf
# Also src03, src14 and src15 weren't downloadable by this utility. so add them manually. 


import os, requests, json
from tqdm import tqdm 

DATA_PATH = "sourced_data"
os.makedirs(DATA_PATH, exist_ok=True)

def load_srcs(file_path:str="sources.json"):
    with open(file_path, "r", encoding="utf-8") as data_src:
        sources = json.load(data_src)
        return sources

def download_and_save_files():
    sources = load_srcs()

    for src in tqdm(sources, desc="Downloading Data from Sources file..."):
        file_id = src["id"]
        file_title = src["title"]
        file_url = src["url"]


        # I already added ids in source file so that's what we'll use for the file names
        filename = file_id + ".pdf"

        filepath = os.path.join(DATA_PATH, filename)

        # if file isnt already there then download it from the web
        if not os.path.exists(filepath):
            try:
                print(f"Downloading {file_title} from {file_url}")
                resp = requests.get(file_url, stream=True)
                if resp.status_code == 200:
                    # save the file
                    with open(filepath, "wb") as data_file:
                        for chunk in resp.iter_content(2048): # chunk size 2048 for faster writing
                            data_file.write(chunk)
            except Exception as e:
                print(f"Encountered an issue downloading {file_id} | {file_title} from {file_url} : {e}")
    
    print(f"Done! PDFs are downloaded and saved at {DATA_PATH}")


if __name__ == '__main__':
    download_and_save_files()