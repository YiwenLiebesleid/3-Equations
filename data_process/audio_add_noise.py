import os
import numpy as np
import librosa
import soundfile as sf
import random
from tqdm import tqdm
import glob
import pandas as pd
from pydub import AudioSegment

def add_2_noise_to_signal_snr(clean_signal, noise_signal_list, snr=0, time_intervals=None, sample_rate=16000):
    # Normalize the signal
    clean_signal = clean_signal / np.max(np.abs(clean_signal))
    clean_length = len(clean_signal)

    # initialize a noisy signal
    noisy_signal = clean_signal.copy()
    
    for i, noise_signal in enumerate(noise_signal_list):
        noise_signal = noise_signal / np.max(np.abs(noise_signal))
        start_time, hard_end_time = time_intervals[i]
        start_sample = int(start_time * sample_rate)
        end_sample = start_sample + len(noise_signal)
        hard_end_sample = int(hard_end_time * sample_rate)   ## the time that the noise must stop before
        hard_end_sample = min(hard_end_sample, end_sample)

        ## if the noise signal is longer than current segment
        if end_sample > hard_end_sample:
            noise_signal = noise_signal[:(hard_end_sample-start_sample)]
        else:
            noise_signal = np.pad(noise_signal, (0, (hard_end_sample-start_sample)-len(noise_signal)), 'constant')

        # Calculate the signal power and noise power, and add desired noise power for the given SNR
        signal_power = np.mean(clean_signal[start_sample:hard_end_sample] ** 2)
        noise_power = np.mean(noise_signal ** 2)
    
        desired_noise_power = signal_power / (10 ** (snr / 10))
        noise_signal = noise_signal * np.sqrt(desired_noise_power / noise_power)
        noisy_signal[start_sample:hard_end_sample] += noise_signal
    
    noisy_signal = noisy_signal / np.max(np.abs(noisy_signal))
    return noisy_signal

def add_2_noise_to_signal_length_ratio(clean_signal, noise_signal_list, snr=0, time_intervals=None, length_ratio=0.25, sample_rate=16000):
    # Normalize the signal
    clean_signal = clean_signal / np.max(np.abs(clean_signal))
    clean_length = len(clean_signal)

    # initialize a noisy signal
    noisy_signal = clean_signal.copy()
    
    for i, noise_signal in enumerate(noise_signal_list):
        noise_signal = noise_signal / np.max(np.abs(noise_signal))
        start_time, hard_end_time = time_intervals[i]
        hard_start_time = hard_end_time - (hard_end_time-start_time)*length_ratio
        
        start_sample = int(hard_start_time * sample_rate)
        end_sample = start_sample + len(noise_signal)
        hard_end_sample = int(hard_end_time * sample_rate)   ## the time that the noise must stop before
        hard_end_sample = min(hard_end_sample, end_sample)

        ## if the noise signal is longer than current segment
        if end_sample > hard_end_sample:
            noise_signal = noise_signal[:(hard_end_sample-start_sample)]
        else:
            noise_signal = np.pad(noise_signal, (0, (hard_end_sample-start_sample)-len(noise_signal)), 'wrap')

        # Calculate the signal power and noise power, and add desired noise power for the given SNR
        signal_power = np.mean(clean_signal[start_sample:hard_end_sample] ** 2)
        noise_power = np.mean(noise_signal ** 2)
        
        desired_noise_power = signal_power / (10 ** (snr / 10))
        noise_signal = noise_signal * np.sqrt(desired_noise_power / noise_power)
        noisy_signal[start_sample:hard_end_sample] += noise_signal
    
    noisy_signal = noisy_signal / np.max(np.abs(noisy_signal))
    return noisy_signal

def process_audio_files(clean_dir, df_audio, df_noise, output_dir, snr, epsilon=0.1, method='snr', length_ratio=0.25):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if type(clean_dir) is str:
        clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.wav')]
    elif type(clean_dir) is list:
        clean_files = clean_dir

    snr_infos = []

    for clean_file in tqdm(clean_files):
        if type(clean_dir) is str:
            clean_path = os.path.join(clean_dir, clean_file)
        elif type(clean_dir) is list:
            clean_path = clean_file
        clean_signal, sr = librosa.load(clean_path, sr=None)

        row = df_audio[df_audio.file_name==clean_path]
        start1, end1 = list(row.first_start)[0], list(row.first_end)[0]
        start2, end2 = list(row.second_start)[0], list(row.second_end)[0]
        dur1, dur2 = end1-start1, end2-start2
        
        noise_line1 = df_noise.sample(1)
        noise_line2 = df_noise.sample(1)
        noise_path1 = list(noise_line1.file_name)[0]
        noise_path2 = list(noise_line2.file_name)[0]
        noise_dur1 = list(noise_line1.duration)[0]
        noise_dur2 = list(noise_line2.duration)[0]
        noise_signal1, _ = librosa.load(noise_path1, sr=sr)
        noise_signal2, _ = librosa.load(noise_path2, sr=sr)

        if method == 'snr':
            noise_start1 = random.uniform(start1+epsilon, end1-epsilon)
            noise_start2 = random.uniform(start2+epsilon, end2-epsilon)
            noisy_signal = add_2_noise_to_signal_snr(clean_signal, [noise_signal1, noise_signal2], snr=snr
                                     , time_intervals=[(noise_start1, end1-epsilon), (noise_start2, end2-epsilon)]
                                    , sample_rate=sr)
        elif method == 'snrs':
            noise_start1 = start1
            noise_start2 = start2
            choose_snr = random.choice(snr)
            noisy_signal = add_2_noise_to_signal_length_ratio(clean_signal, [noise_signal1, noise_signal2], snr=choose_snr
                                     , time_intervals=[(noise_start1, end1-epsilon), (noise_start2, end2-epsilon)]
                                    , length_ratio=length_ratio, sample_rate=sr)
            snr_infos += [choose_snr]
        
        if type(clean_dir) is str:
            output_path = os.path.join(output_dir, clean_file)
        elif type(clean_dir) is list:
            output_path = os.path.join(output_dir, os.path.basename(clean_file))
        sf.write(output_path, noisy_signal, sr)
    return clean_files, snr_infos

if __name__ == "__main__":
    ## speech_info.csv contains the information of the starting and endding timestamp of each equation sentence
    df = pd.read_csv('./speech_info.csv')
    ## noise_info.csv contains the information of the candidate noise audio
    df_noise = pd.read_csv('./noise_info.csv')
    
    clean_dir = "./audio/clean"
    snrs = [20,10,5,0,-5,-10,-20]
    epsilon = 0.15      # hard left bound
    method = 'snrs'
    length_ratio = 0.5    # add noise to the second half of each sentence
    output_dir = f"./audio/MIX_2noise_20dB_to_-20dB"
    fids, snr_infos = process_audio_files(clean_dir, df, df_noise, output_dir, snrs, epsilon, method=method, length_ratio=length_ratio)

    ## save SNR information of each audio
    df_snr = pd.DataFrame()
    df_snr['file_name'] = fids
    df_snr['snr'] = snr_infos
    df_snr.to_csv("./audio/MIX_2noise_20dB_to_-20dB/snr.csv",index=False)
