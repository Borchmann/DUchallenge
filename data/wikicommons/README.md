# Wikimedia commons pdf files downloader 

The aim of this repository is to download wikimedia commons pdf files (and their metadata) which comes from specific pre-defined categories.


Useful links:
1. [Browsing pdf files on wikimedia common webpage](https://commons.wikimedia.org/w/index.php?search=&title=Special:MediaSearch&go=Go&type=other&filemime=pdf)
2. [Wikimedia dumps](https://dumps.wikimedia.org/)


# Processing instruction  

1. [Download commonswiki dump](#download-commonswiki-dump)
2. [Create metadata db](#create-metadata-db)
3. [Find pdf files by keywords](#find-pdf-files-by-keywords)
4. [Download files](#download-files)

## Download commonswiki dump

At first, we need to download wikimedia dump to have access to all filenames.

```commandline
mkdir data
cd data/
wget https://dumps.wikimedia.org/commonswiki/20220801/commonswiki-20220801-pages-articles-multistream-index.txt.bz2
tar -xf commonswiki-20220801-pages-articles-multistream-index.txt.bz2
```

## Create metadata db

This script create csv file with metadata of each pdf file from wikimedia commons database 

```commandline
cd data/wikicommons/
python create_metadata_db.py
```

## Find pdf files by keywords

This script create csv file with filenames to download (based on search keywords defined in `conf.py` script) 

```commandline
cd data/wikicommons/
python find_pdf_files_by_keywords.py
```

## Download files

This script download pdf files from wikimedia commons

```commandline
cd data/wikicommons/
python download_pdfs.py
``` 
