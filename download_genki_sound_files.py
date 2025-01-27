import gdown
import os
import zipfile

# Create directories if they don't exist
os.makedirs('./data/genki_1/sound', exist_ok=True)
os.makedirs('./data/genki_2/sound', exist_ok=True)

# Function to unzip the downloaded files
def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Unzipped {zip_path} to {extract_to}")

# Download the Genki sound files
# https://drive.google.com/file/d/1RXnr3nEiv5gFGIQqdMugrETwXu-lsar1/view?usp=share_link
gdown.download(id='1RXnr3nEiv5gFGIQqdMugrETwXu-lsar1', output='./data/genki_1/sound/genki_1_sounds.zip')

# Unzip the first file
unzip_file('./data/genki_1/sound/genki_1_sounds.zip', './data/genki_1/sound')

# https://drive.google.com/file/d/1KPkNM85bM4zymzqO-aLWELah-RVM2p3O/view?usp=share_link
gdown.download(id='1KPkNM85bM4zymzqO-aLWELah-RVM2p3O', output='./data/genki_2/sound/genki_2_sounds.zip')

# Unzip the second file
unzip_file('./data/genki_2/sound/genki_2_sounds.zip', './data/genki_2/sound')
