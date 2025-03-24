import os
import sys
import glob
from tqdm import tqdm
import re
import easyocr

def get_ocr(path, tgt_path):
    if os.path.exists(tgt_path):
        return
    results = reader.readtext(path)
    ocr = ""
    pattern = r'[^a-zA-Z0-9\+\-=]'
    for (_,text,_) in results:
        text = text.upper()
        text = re.sub(pattern, '', text)
        ocr += text + " "
    with open(tgt_path, 'w+') as f:
        f.write(ocr)

if __name__ == "__main__":
    reader = easyocr.Reader(['en'])

    src_dir="./images"
    tgt_dir="./real_ocr"
    files=glob.glob(src_dir+f"/*.png")
    
    for i in tqdm(range(len(files))):
        file = files[i]
        tgt_path = os.path.join(tgt_dir, f'{i}.txt')
        get_ocr(file, tgt_path)
