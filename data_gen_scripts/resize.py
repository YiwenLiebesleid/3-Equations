# very brief script to resize my data to whatever size you need. refer to README.md for usage details.
# author: vivek

import sys
import os
import re
from PIL import Image

def main(orig_img_directory, new_img_directory, width, height):
    os.makedirs(new_img_directory, exist_ok=True)
    for img_file in os.listdir(orig_img_directory):
        img = Image.open(os.path.join(orig_img_directory, img_file))
        resized = img.resize((width, height))
        resized.save(os.path.join(new_img_directory, img_file))

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("python3 resize.py <orig_img_directory> <new_img_directory> <width> <height>")
        exit()
    
    sys.argv[3] = int(sys.argv[3])
    sys.argv[4] = int(sys.argv[4])
    main(*sys.argv[1:])
