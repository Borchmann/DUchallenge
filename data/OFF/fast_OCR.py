import os
import sys
import json
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


def OCR_it(path):
    model = ocr_predictor(pretrained=True)
    # PDF
    doc = DocumentFile.from_pdf(path)
    # Analyze
    result = model(doc)

    name, extension = os.path.splitext(path)

    out_path = open(os.path.join(name + "-OCR.json"), "w")
    json.dump(result.export(), out_path, indent=4)

    #XML format is also possible

def OCR_model_loaded(model, path):

    name, extension = os.path.splitext(path)
    out_path = os.path.join(name + "-OCR.json")
    if os.path.exists(out_path):
        return
    out_path = open(out_path, "w")
    # PDF
    doc = DocumentFile.from_pdf(path)
    # Analyze
    result = model(doc)

    json.dump(result.export(), out_path, indent=4)



if __name__ == "__main__":
    OCR_it(sys.argv[1])
