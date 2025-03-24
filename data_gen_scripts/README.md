# 3-Equations
## Speech and Image
### This dataset has:
 - 10000 examples
 - An example consists of three equations on a blank image in **random** locations (each example comes in 3 different fonts)
 - Equations contain more advanced operations than Dataset 1 (e.g. logs, exponents, fractions)
 - Each example has an audio sample reading out two of the three equations at random, with a one second silence between the equations
 - Each of the 10000 audio samples have gaussian noise added with increasing standard deviation

### File info
 - `dataset.csv` has all information compiled into one csv - LaTeX equations, their spoken word plaintext translations, the (x, y) positions on the corresponding image, and which equations are read out loud by the audio sample (0 based)

## Lip
Use [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) to synthesize synchronized lip movement videos.
```python ./wav2lip/Wav2Lip/inference.py --checkpoint_path ./wav2lip/Wav2Lip/checkpoints/wav2lip.pth --face /path/to/your/face/image --audio /path/to/your/audio --outfile /path/to/output```


## Reference
[1] Prajwal K R, Mukhopadhyay R, Namboodiri V P, et al. A lip sync expert is all you need for speech to lip generation in the wild[C]//Proceedings of the 28th ACM international conference on multimedia. 2020: 484-492.
