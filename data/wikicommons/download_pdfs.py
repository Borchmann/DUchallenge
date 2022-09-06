import os
import time
import pandas as pd

from tqdm import tqdm
from pathlib import Path


from conf import DEFAULT_SLEEP_TIME, FILEPATH_CATEGORIES_PDFS, FILEPATH_PDFS

df_data = pd.read_csv(FILEPATH_CATEGORIES_PDFS)
for index, row in tqdm(df_data.iterrows()):
    file = row['filename_md5']

    if row['categories_all_count'] == 1:
        file_dir = os.path.join(FILEPATH_PDFS, row['categories_all'])
    else:
        file_dir = os.path.join(FILEPATH_PDFS, 'mix_categories')

    Path(file_dir).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(file_dir, file)
    if os.path.exists(filepath):
        continue

    file = row['filename_wiki']
    command = f"wikiget 'https://commons.wikimedia.org/wiki/{file}' -o '{filepath}'"
    os.system(command)
    time.sleep(DEFAULT_SLEEP_TIME)
