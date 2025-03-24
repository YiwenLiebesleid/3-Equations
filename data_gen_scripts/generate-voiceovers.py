import pyttsx3
import os
import pandas as pd
import random
from pydub import AudioSegment
import numpy as np

def tts(engine, text, file_name):
    # check proper file ext
    if not file_name.endswith(".wav"):
        file_name = f"{file_name}.wav"
    
    # convert text to speech
    engine.save_to_file(text, file_name)
    engine.runAndWait()

def main():
    # init engine
    engine = pyttsx3.init()
    engine.setProperty("rate", 175) # in wpm
    engine.setProperty("volume", 0.9) # from 0-1

    # data & housekeeping
    os.makedirs("../audio/clean", exist_ok=True)
    df = pd.read_csv("../dataset.csv", header=None)
    eq1_voiceover_texts = df.iloc[:, 1]
    eq2_voiceover_texts = df.iloc[:, 4]
    eq3_voiceover_texts = df.iloc[:, 7]
    all_voiceovers = [eq1_voiceover_texts, eq2_voiceover_texts, eq3_voiceover_texts]

    # run tts
    read_aloud_indices = np.zeros(len(eq1_voiceover_texts), dtype=object)
    for i in range(len(eq1_voiceover_texts)):
        # pick two voice lines at random
        indices = random.sample(range(3), 2)
        line1 = all_voiceovers[indices[0]][i]
        line2 = all_voiceovers[indices[1]][i]
        read_aloud_indices[i] = indices

        # save temp files  
        tts(engine, line1, f"temp-{i}-1.wav")
        tts(engine, line2, f"temp-{i}-2.wav")

        # load in temp files
        audio1 = AudioSegment.from_wav(f"temp-{i}-1.wav")
        audio2 = AudioSegment.from_wav(f"temp-{i}-2.wav")

        # add one second of silence b/t examples
        combined = audio1 + AudioSegment.silent(duration=1000) + audio2
        combined.export(f"../audio/clean/{i}.wav", format="wav")

        # clean up
        os.remove(f"temp-{i}-1.wav")
        os.remove(f"temp-{i}-2.wav")

    # add data and cleanup
    df.insert(df.shape[1], "read_aloud_indices", read_aloud_indices)
    df.to_csv("../dataset.csv", index=False, header=False)

if __name__ == "__main__":
    main()  
