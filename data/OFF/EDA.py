import os
import json
from PIL import Image
import requests
from io import BytesIO

"""
# Document Understanding Benchmark

The idea is to make Q&A on food labels! 

Inspiration:
* https://openfoodfacts.github.io/robotoff/references/api/#questions
* https://github.com/ramsyy0/OpenFoodFactsCategorizer 
* https://github.com/openfoodfacts/openfoodfacts-ai


# FDF is another alternative
## https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
## would be nice to add metadata inside the pdf
"""


WHITELIST = ["image"]
BLACKLIST = ["small", "thumb"]

"""
natural hierarchy

"image_front_small_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/front_en.6.200.jpg",
"image_front_thumb_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/front_en.6.100.jpg",
"image_front_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/front_en.6.400.jpg",
"image_ingredients_small_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/ingredients_en.10.200.jpg",
"image_ingredients_thumb_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/ingredients_en.10.100.jpg",
"image_ingredients_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/ingredients_en.10.400.jpg",
"image_nutrition_small_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/nutrition_en.12.200.jpg",
"image_nutrition_thumb_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/nutrition_en.12.100.jpg",
"image_nutrition_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/nutrition_en.12.400.jpg",
"image_small_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/front_en.6.200.jpg",
"image_thumb_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/front_en.6.100.jpg",
"image_url": "https://images.openfoodfacts.org/images/products/073/762/806/4502/front_en.6.400.jpg",
"""


def open_online_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def get_images(data=None, save=False, identifier=None, binary=False):
    images = []
    if data is None:
        data = json.load(open("sample.json"))["product"]
        identifier = "sample"

    if save:
        assert identifier is not None, "specify some unique identifier for linking to metadata"

    # keys = [
    #     k for k in data if all([w in k for w in WHITELIST]) and not any([b in k for b in BLACKLIST])
    # ]
    #potential_images = ["front", "ingredients", "nutrition", "back"]
    
    potential_images = ["", "_ingredients", "_nutrition"]
    for p in potential_images:
        potential_url = f"image{p}_url"
        #if potential_url in keys:
        if binary:
            images.append(open_online_image(data[potential_url]))
        else:
            images.append(data[potential_url])
    if save:
        out = os.path.join("PDFs", f"{identifier}.pdf")
        if not os.path.exists(out):
            # Save as pdf as if it was a multipage document
            images[0].save(
                out, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
            )
    return images

if __name__ == "__main__":
    get_images()
