import string

import pandas as pd
from loguru import logger
from collections import defaultdict
from tqdm import tqdm
import hashlib

from conf import CATEGORIES_KEYWORDS, DATA_LIST_SEP, FILEPATH_CATEGORIES_PDFS, FILEPATH_DB_PDFS, MAX_DOC_PAGES, \
    MAX_DOC_SIZE


def preprocess_text(text):
    if isinstance(text, float):
        return ''

    text = text.split(':File:')[1] if "File:" in text else text
    text = text.lower()

    text = text.translate({k: ' ' for k, w in str.maketrans('', '', string.punctuation).items()})
    text = " ".join(text.split())

    text = ' ' + text + ' '
    return text


# load files db
df = pd.read_csv(FILEPATH_DB_PDFS, low_memory=False)
logger.info(f'Loaded {len(list(df["filename"]))} files')

# filter our proper pdf documents
df = df[df['imginfo_pages'].astype(str).str.endswith(".0") | df['imginfo_pages'].astype(str).str.isnumeric()]
logger.info(f'Loaded {len(df)} fixed files (skip files without empty page count)')
df = df[(df['imginfo_pages'].astype(float) <= MAX_DOC_PAGES) & (df['imginfo_filesize'] <= MAX_DOC_SIZE)]
logger.info(f'Loaded {len(df)} files limited to the {int(MAX_DOC_PAGES)} pages and filesize {MAX_DOC_SIZE}')
df['filename_processed'] = df['filename'].apply(preprocess_text)
df['categories_processed'] = df['general_categories'].apply(preprocess_text)

# filter files by keywords
search_prefix_suffix = ' '
list_to_download = []
categories_filename = defaultdict(list)
categories_wikicategories = defaultdict(list)
for category in CATEGORIES_KEYWORDS.keys():
    def find_category(text):
        cat_keywords = CATEGORIES_KEYWORDS[category]

        for keyword in cat_keywords:
            if search_prefix_suffix + keyword + search_prefix_suffix in text:
                return True

        return False

    count_matched_filenames = 0
    for filename in list(df[df['filename_processed'].apply(find_category)]['filename']):
        categories_filename[filename].append(category)
        count_matched_filenames += 1

    count_matched_categories = 0
    for filename in list(df[df['categories_processed'].apply(find_category)]['filename']):
        categories_wikicategories[filename].append(category)
        count_matched_categories += 1

    logger.info(f'Stats for "{category}" | # matched by filenames: {count_matched_filenames} '
                f'| # matched by categories: {count_matched_categories}')

filename_to_row = {}
for index, row in tqdm(df.iterrows()):
    filename_to_row[row['filename']] = row

list_to_download = []
for filename in tqdm(set(categories_filename.keys()).union((categories_wikicategories.keys()))):
    category_filename_1 = None
    category_filename_2 = None
    categories_all = set()
    if filename in categories_filename:
        categories_all.update(categories_filename[filename])
        category_filename_1 = categories_filename[filename][0]
        if len(categories_filename[filename]) == 2:
            category_filename_2 = categories_filename[filename][1]

    category_wiki_1 = None
    category_wiki_2 = None
    if filename in categories_wikicategories:
        categories_all.update(categories_wikicategories[filename])
        category_wiki_1 = categories_wikicategories[filename][0]
        if len(categories_wikicategories[filename]) == 2:
            category_wiki_2 = categories_wikicategories[filename][1]

    filename_row = filename_to_row[filename]
    pages = filename_row['imginfo_pages']
    filesize = filename_row['imginfo_filesize']
    creation_date = filename_row['imginfo_creationdate']
    all_wiki_categories = filename_row['general_categories']

    filename_simple = filename.split(':File:')[1]
    list_to_download.append(
        {
            'filename_full': filename,
            'filename_wiki': 'File:' + filename_simple,
            'filename_md5': hashlib.md5(filename_simple.encode('utf-8')).hexdigest() + '.pdf',
            'category_filename_1': category_filename_1,
            'category_filename_2': category_filename_2,
            'category_wiki_1': category_wiki_1,
            'category_wiki_2': category_wiki_2,
            'categories_all': DATA_LIST_SEP.join(categories_all),
            'categories_all_count': len(categories_all),
            'pages': pages,
            'creation_date': creation_date,
            'filesize': filesize,
            'all_wiki_categories': all_wiki_categories,
        }
    )

df_to_download = pd.DataFrame(list_to_download)
df_to_download.to_csv(FILEPATH_CATEGORIES_PDFS, index=False)
