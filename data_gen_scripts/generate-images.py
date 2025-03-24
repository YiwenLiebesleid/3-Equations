from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd
import re
import random
import numpy as np

def render_equation(equation, name):
    """
    renders one equation in LaTeX with under the given file name.

    :param equation (str): the LaTeX equation to render
    :param name (str): the file name as an image file
    """

    # create and compile LaTeX
    tex_doc = ["\\documentclass[preview]{minimal}\n", "\\begin{document}\n", f"${equation}$\n", "\\end{document}\n"]
    open("a.tex", "w").writelines(tex_doc)
    os.system(f"latex a.tex && dvipng -D 200 -T tight -o {name} a.dvi")

def create_image(all_equations):
    # render the equations
    for i, eqn in enumerate(all_equations):
        render_equation(eqn, f"eqn-{i}.png")
    
    eqn_images = [Image.open(f"eqn-{i}.png") for i in range(len(all_equations))]
    eqn_sizes = [img.size for img in eqn_images]

    # helpers
    def is_overlapping(pos1, size1, pos2, size2):
        """
        Check if two rectangles overlap
        """
        return not (pos1[0] + size1[0] <= pos2[0] or pos2[0] + size2[0] <= pos1[0] or
                    pos1[1] + size1[1] <= pos2[1] or pos2[1] + size2[1] <= pos1[1])

    def rand_pos(base_size, overlay_size):
        """
        Get a random position within the base image bounds
        """
        max_x = base_size[0] - overlay_size[0]
        max_y = base_size[1] - overlay_size[1]
        return (random.randint(0, max_x), random.randint(0, max_y))
    
    # create new base image
    base_size = (450, 450)
    base_image = Image.new("RGB", base_size, color=(255, 255, 255))

    # randomly find points that work (relies on blank base image being big enough)
    positions = []
    for i in range(len(eqn_images)):
        while True:
            # get random pos
            position = rand_pos(base_size, eqn_sizes[i])

            # check overlap
            if all(not is_overlapping(position, eqn_sizes[i], p, eqn_sizes[j]) for j, p in enumerate(positions)):
                positions.append(position)
                break
    
    # paste images and return
    for eq_img, pos in zip(eqn_images, positions):
        base_image.paste(eq_img, pos)
    return base_image, positions

def main():
    # read in dataset
    df = pd.read_csv("../dataset.csv", header=None)
    eq1s = df.iloc[:, 0] # equation 1 LaTeX column
    eq2s = df.iloc[:, 2] # equation 2 LaTeX column
    eq3s = df.iloc[:, 4] # equation 3 LaTeX column

    # housekeeping
    os.makedirs("../images", exist_ok=True)
    all_eqn_positions = np.zeros((len(eq1s), 3), dtype=object)

    # create and save image per font
    for i in range(len(eq1s)):
        image, eqn_positions = create_image([eq1s[i], eq2s[i], eq3s[i]])
        image.save(f"../images/{i}.png")
        all_eqn_positions[i] = eqn_positions

    # cleanup
    df.insert(2, "pos0", all_eqn_positions[:, 0])
    df.insert(5, "pos1", all_eqn_positions[:, 1])
    df.insert(8, "pos2", all_eqn_positions[:, 2])
    df.to_csv("../dataset.csv", index=False, header=False)
    os.system("rm *.png a.aux a.dvi a.log a.tex")

if __name__ == "__main__":
    main()
