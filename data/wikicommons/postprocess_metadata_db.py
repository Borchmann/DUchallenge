import csv

import pandas as pd
from langdetect import detect
from loguru import logger
from tqdm import tqdm

filepath_metadata = '/home/tstanislawek/Downloads/docvqa_v2/commonswiki-20220801_db.csv'
filepath_metadata_postprocess = filepath_metadata[:-4] + '_postprocess.csv'


def detect_lang(text):
    try:
        return detect(text[:200])
    except Exception as e:
        return 'error'


tqdm.pandas()
df = pd.read_csv(filepath_metadata, quoting=csv.QUOTE_NONNUMERIC)
logger.info(f'All docs count: {len(df)}')
df_fixed = df[df['imginfo_pages'].astype(str).str.endswith(".0") | df['imginfo_pages'].astype(str).str.isnumeric()]
logger.info(f'Proper docs count: {len(df_fixed)}')

df_fixed['lang_first_page'] = df_fixed['imginfo_text_first_page'].progress_apply(detect_lang)
logger.info(f"Detected English texts count: {len(df_fixed[df_fixed['lang_first_page'] == 'en'])}")

df_fixed['lang_filename'] = df_fixed['filename'].progress_apply(detect_lang)
logger.info(f"Detected English filenames count: {len(df_fixed[df_fixed['lang_filename'] == 'en'])}")

df_fixed.to_csv(filepath_metadata_postprocess, index=False, quoting=csv.QUOTE_ALL)
