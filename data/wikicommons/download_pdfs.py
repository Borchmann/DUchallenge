import csv
import os
import time
import pandas as pd

from tqdm import tqdm
from pathlib import Path


from conf import DEFAULT_SLEEP_TIME, FILEPATH_CATEGORIES_PDFS, FILEPATH_DOWNLOADING_ERRORS, FILEPATH_PDFS

df_data = pd.read_csv(FILEPATH_CATEGORIES_PDFS)
error_list = []
errors_files = set()
if os.path.exists(FILEPATH_DOWNLOADING_ERRORS):
    errors_files = set(list(pd.read_csv(FILEPATH_DOWNLOADING_ERRORS, quoting=csv.QUOTE_ALL)['filename_md5']))

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
    err = os.system(command)
    if err and row['filename_md5'] not in errors_files:
        errors_files.add(row['filename_md5'])
        error_list.append(row)
    time.sleep(DEFAULT_SLEEP_TIME)

    if index % 10 == 9:
        df = pd.DataFrame(error_list)
        df.to_csv(FILEPATH_DOWNLOADING_ERRORS,
                  mode='a',
                  header=not os.path.exists(FILEPATH_DOWNLOADING_ERRORS),
                  index=False,
                  quoting=csv.QUOTE_ALL)
