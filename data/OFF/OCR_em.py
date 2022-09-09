import os
import sys
import json
import pandas as pd
from tqdm import tqdm
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from fast_OCR import OCR_model_loaded

#data
image_df = pd.read_csv("25drop-allimages-en-world.csv")

#model
model = ocr_predictor(pretrained=True)


for i, row in tqdm(image_df.iterrows()):
    file = os.path.join("PDFs", str(row["code"])+".pdf")
    if not os.path.exists(file):
        print(f"{file} does not exist")
        continue
    OCR_model_loaded(model, file)