# import the os module
import os
import librosa
import soundfile as sf
import numpy as np

apath = "./assets/"
newpath = "./new/samples"
hop = 2048
# sr = 44100
os.system("rm -rf new")
os.system("mkdir new")


def smooth(samples, hop_length=512):
    incr = 1 / hop_length
    for i, sample in enumerate(samples[:hop_length]):
        samples[i] = sample * incr
        samples[(i + 1) * -1] = samples[(i + 1) * -1] * incr
        incr *= i
    return samples


def process_samples(track, fname, sr=44100, hop=2048):

    oenv = librosa.onset.onset_strength(y=track, sr=sr, hop_length=hop)

    onsets = librosa.onset.onset_detect(onset_envelope=oenv, backtrack=False)

    onset_bt = librosa.onset.onset_backtrack(onsets, oenv)

    sft = librosa.frames_to_samples(onsets, hop_length=hop)
    sfbt = librosa.frames_to_samples(onset_bt, hop_length=hop)

    for i, start in enumerate(sfbt):

        diff = sft[i] - start
        end = sfbt[i + 1] if len(sfbt) > i + 1 else sft[i] + diff

        # start = s - 256
        # if start < 0:
        #     start = s

        new = track[start:end]

        print(diff)
        print("difff")
        print(start)
        print("start")
        print(end)
        print("end")
        newname = fname + str(i) + ".wav"
        print(new)
        print(newname)
        new_smoothed = smooth(new)
        sf.write(newname, new_smoothed, sr, "PCM_24")


folder = os.fsencode(apath)
files = []
for file in os.listdir(folder):
    f = file.decode("utf-8")

    fpath = folder.decode("utf-8") + f
    print(fpath)

    files.append(fpath)


for fp in files:
    fp = str(fp)
    smpr = 44100
    tr, sr = librosa.load(fp, offset=0, duration=None, mono=True)
    print("SRRRR")
    print(sr)
    track = librosa.resample(tr, sr, 44100)
    # low = librosa.effects.percussive(track)
    # high = librosa.effects.harmonic(track)
    #
    # process_samples(low, newpath + "perc_", sr=sr)
    # process_samples(high, newpath + "harm_")
    process_samples(track, newpath + "_full_", sr=sr)
