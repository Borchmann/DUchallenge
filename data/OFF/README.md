# Openfoodfacts Document VQA

Some existing projects are here: https://github.com/orgs/openfoodfacts/projects/16

## Installation of API

We will exploit the existing Robotoff API to analyze and prune the database for interesting data

Robotoff is currently compatible with Python 3.7 and 3.8. Robotoff can be installed following https://openfoodfacts.github.io/robotoff/how-to-guides/deployment/dev-install/

(### docker installation)


### poetry installation

```sh
cd $HOME/code/DUchallenge/data/OFF; git clone git@github.com:openfoodfacts/robotoff.git
```
We will create new virtualenvironment in which to install all required packages.
```sh
mkvirtualenv -p /usr/bin/python3.8 -a . robotoff
```

Using poetry and the readily defined pyproject.toml, we will install all required packages
```sh
workon robotoff 
pip3 install poetry
cd ./robotoff
poetry install

#some custom installs for parsing
poetry add jupyterlab

```

Then we need to run some tests on the installation

```sh
sudo apt install gettext
cd i18n && bash compile.sh && cd ..
```

For sake of compatibility we need to create a symbolic link to where you downloaded the jsonlines tar or just put it at DUchallenge/data/OFF/robotoff/datasets/products.jsonl.gz

## Data exploration

1. we want to better understand the data fields

Inspiration: https://www.kaggle.com/datasets/openfoodfacts/world-food-facts 

2. we want to have an automated way of scraping the images from the DB
3. we need to come up with some filters for language, country, quality of metadata/images


#### Moving to Gdrive

We're going to use pydrive2: 
Follow instructions there.

```sh
pip install PyDrive2
```


## OCR

Could optionally use free OCR: https://github.com/mindee/doctr 

```sh
poetry add python-doctr[pytorch]

#dependent on cuda version; mine is 11.2
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu112
pip3 install pypdfium2==1.0.0 #small patch fix
```

```python
    from doctr.io import DocumentFile
    from doctr.models import ocr_predictor
    model = ocr_predictor(pretrained=True)
    # PDF
    doc = DocumentFile.from_pdf("path/to/your/doc.pdf")
    # Analyze
    result = model(doc)
`