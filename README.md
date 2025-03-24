# 3-Equations
## Descriptions
This repo is for the 3-Equation dataset we created for our paper: [Multi-modal Speech Transformer Decoders: When Do Multiple Modalities Improve Accuracy?](https://arxiv.org/abs/2409.09221)

The dataset consists of 10,000 examples, each containing one image sample with its OCR text, one audio sample, and one lip movement video sample. Specifically, the images depict three mathematical equations, involving operations such as addition, subtraction, logarithms, fractions and exponentiation, with each image sized 450×200. The audio part contains 25.2 hours of synthesized speech, averaging 9 seconds per sample. The lip movement videos are generated from the synthesized audio at 25 FPS using a static portrait image. To create the dataset, we employ pyttsx3 to generate speech utterances, latex command to produce equation images, EasyOCR to obtain OCR texts, and Wav2Lip to generate lip-synced videos.

### 2-noise
We added noise from the MUSAN dataset to the second half of each equation utterance at varying SNRs. The first half of each utterance remains clean, allowing the model to leverage this “incomplete” clean auditory information to locate the correct equation in the image, and subsequently complete the speech transcription with clean visual information.

## Scripts
```data_gen_scripts``` is for generating the image, speech audio, and the corresponding lip video for each example.

```data_process``` is to add noise to the audio, and get the OCR texts of each image.

## References
[1] "pyttsx3: Offline text to speech (tts) converter for python," https://github.com/nateshmbhat/pyttsx3.

[2] K. Prajwal, R. Mukhopadhyay, V. P. Namboodiri, and C. Jawahar,"A lip sync expert is all you need for speech to lip generation in the wild," in Proceedings of the 28th ACM international conference on multimedia, 2020, pp. 484–492.

[3] "Easyocr: Ready-to-use ocr with 80+ supported languages," https://github.com/JaidedAI/EasyOCR.

[4] "Musan: A music, speech, and noise corpus," arXiv preprint arXiv:1510.08484, 2015.
