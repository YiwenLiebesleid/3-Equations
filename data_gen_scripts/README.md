# 3-Equations
### This dataset has:
 - 10000 examples
 - An example consists of three equations on a blank image in **random** locations (each example comes in 3 different fonts)
 - Equations contain more advanced operations than Dataset 1 (e.g. logs, exponents, fractions)
 - Each example has an audio sample reading out two of the three equations at random, with a one second silence between the equations
 - Each of the 10000 audio samples have gaussian noise added with increasing standard deviation

### File info
 - `dataset.csv` has all information compiled into one csv - LaTeX equations, their spoken word plaintext translations, the (x, y) positions on the corresponding image, and which equations are read out loud by the audio sample (0 based)
