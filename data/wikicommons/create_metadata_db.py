import csv
import multiprocessing
import os.path
import pandas as pd
import requests
import html

from loguru import logger
from typing import Dict, List
from tqdm import tqdm

from conf import DATA_LIST_SEP, FILEPATH_DB_PDFS, FILEPATH_DUMP, FILEPATH_DUMP_CACHE_PDF, NUMBER_OF_PROCESSORS, \
    URL_INFO_TEMPLATE


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def filter_out_pdf_files(filepath_in, cache_filepath) -> List[str]:
    if os.path.exists(cache_filepath):
        with open(cache_filepath) as f:
            return [line[:-1] for line in f.readlines()]
    else:
        pdf_files = []
        with open(filepath_in) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if (line.strip().endswith('.pdf') or line.strip().endswith('.PDF')) and ':File' in line:
                    pdf_files.append(html.unescape(line.strip()))

        textfile = open(cache_filepath, "w")
        for element in pdf_files:
            textfile.write(element + "\n")
        textfile.close()
        return pdf_files


def get_pdf_info(file_entry: str) -> Dict:
    pdf_file = 'File:' + file_entry.split(":")[-1]
    url = URL_INFO_TEMPLATE.replace('[[]]', pdf_file)

    params = dict()
    resp = requests.get(url=url, params=params)
    data = resp.json()

    data['filename'] = file_entry
    file_data_extracted = extract_data_from_json(data)
    return file_data_extracted


def clean_text(text):
    if isinstance(text, float):
        return text
    else:
        return ' '.join(''.join(ch for ch in text if ch.isalnum() or ch == ' ').split())


def extract_data_from_json(json_data: Dict) -> Dict:
    doc_data = {'filename': json_data['filename']}
    pages = json_data['query']['pages']
    page_data = list(pages.values())[0]

    if 'imageinfo' not in page_data or len(page_data['imageinfo']) == 0:
        return doc_data

    try:
        page_data_img = {entry['name']: entry['value'] for entry in page_data['imageinfo'][0]['metadata']}
        for key in ['Pages', 'CreationDate', 'Form', 'Encrypted']:
            doc_data['imginfo_' + key.lower()] = page_data_img[key] if key in page_data_img else ''

        doc_data['general_touched'] = page_data['touched'] if 'touched' in page_data else ''
        doc_data['general_categories'] = DATA_LIST_SEP.join(
            [clean_text(c['title']) for c in page_data['categories']]) if 'categories' in page_data else ''

        if 'File size' in page_data_img:
            doc_data['imginfo_filesize'] = page_data_img['File size'].replace(' bytes', '')
        if 'text' in page_data_img:
            doc_data['imginfo_text_first_page'] = clean_text(page_data_img['text'][0]['value'])

        if 'mergedMetadata' in page_data_img:
            page_data_img_meta = {entry['name']: entry['value'] for entry in page_data_img['mergedMetadata']}
            if 'DateTimeDigitized' in page_data_img_meta:
                doc_data['imginfo_date_digitized'] = page_data_img_meta['DateTimeDigitized']
            if 'Software' in page_data_img_meta:
                doc_data['imginfo_software'] = page_data_img_meta['Software']
            if 'pdf-Producer' in page_data_img_meta:
                doc_data['imginfo_producer'] = page_data_img_meta['pdf-Producer']
    except Exception as e:
        logger.warning(e)

    return doc_data


pdf_files = filter_out_pdf_files(FILEPATH_DUMP, FILEPATH_DUMP_CACHE_PDF)
logger.info(f"Total files: {len(pdf_files)}")

if os.path.exists(FILEPATH_DB_PDFS):
    filenames_already_processed = set(pd.read_csv(FILEPATH_DB_PDFS, quoting=csv.QUOTE_ALL)['filename'])
    logger.info(f"Files already processed: {len(filenames_already_processed)}")
    pdf_files = [pdf for pdf in pdf_files if pdf not in filenames_already_processed]
    logger.info(f"Total files to process: {len(pdf_files)}")

data_list = []
pdf_files_chunks = chunks(pdf_files, 100)
p = multiprocessing.Pool(NUMBER_OF_PROCESSORS)
for idx, pdf_file_chunk in tqdm(enumerate(pdf_files_chunks)):

    for out_pdf_file in p.imap(get_pdf_info, pdf_file_chunk):
        data_list.append(out_pdf_file)

    if idx % 10 == 9:
        logger.info(f'Current idx: {idx}, current data_list_size: {len(data_list)}')
        df = pd.DataFrame(data_list)
        df.to_csv(FILEPATH_DB_PDFS,
                  mode='a',
                  header=not os.path.exists(FILEPATH_DB_PDFS),
                  index=False,
                  quoting=csv.QUOTE_ALL)
        data_list = []

df = pd.DataFrame(data_list)
df.to_csv(FILEPATH_DB_PDFS,
          mode='a',
          header=not os.path.exists(FILEPATH_DB_PDFS),
          index=False,
          quoting=csv.QUOTE_ALL)
