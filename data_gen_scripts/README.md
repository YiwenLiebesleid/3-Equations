# 3-Equations
Dataset description:
 - In our experiments, we have 10000 examples
 - An example consists of three equations on a blank image in **random** locations
 - Equations contain operations like logs, exponents, fractions rather than just additions or subtractions
 - Each example has an audio sample reading out two of the three equations at random, with a one-second silence between the equations
 - Each example has a lip video related to the synthesized audio clip

File info
 - `dataset.csv` has all information compiled into one CSV - LaTeX equations, their spoken word plaintext translations, the (x, y) positions on the corresponding image, and which equations are read out loud by the audio sample (0 based)

## Image
Use ```sympy.printing.latex.LatexPrinter``` to create equations, the equations may include fractions, logarithms, and exponents. Use PIL to create the images. In our dataset, each image contains 3 equations.

See: ```generate-strings.py```, ```generate-images.py```

## Speech
Use [pyttsx3](https://github.com/nateshmbhat/pyttsx3) to synthesize speech audio. In our dataset, only 2 out of the 3 equations will be read out.

See: ```generate-voiceovers.py```

## Lip
Use [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) to synthesize synchronized lip movement videos. Use the following command to synthesize the corresponding lip movement video from an image and an audio file.

```python ./wav2lip/Wav2Lip/inference.py --checkpoint_path ./wav2lip/Wav2Lip/checkpoints/wav2lip.pth --face /path/to/your/face/image --audio /path/to/your/audio --outfile /path/to/output```


## Reference
[1] pyttsx3: https://github.com/nateshmbhat/pyttsx3

[2] Prajwal K R, Mukhopadhyay R, Namboodiri V P, et al. A lip sync expert is all you need for speech to lip generation in the wild[C]//Proceedings of the 28th ACM international conference on multimedia. 2020: 484-492.
