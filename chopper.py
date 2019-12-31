# import the os module
import os
import librosa
import soundfile as sf
import numpy as np

# detect the current working directory and print it
apath = "./assets/"
newpath = "./new/samples"
hop = 882
sr = 44100


def process_samples(track, fname, sr=44100, hop=2205):

    oenv = librosa.onset.onset_strength(y=track, sr=sr, hop_length=hop)

    onsets = librosa.onset.onset_detect(y=track, onset_envelope=oenv, backtrack=False)

    onset_bt = librosa.onset.onset_backtrack(onsets, oenv)

    sft = librosa.frames_to_samples(onsets, hop_length=hop)
    sfbt = librosa.frames_to_samples(onset_bt, hop_length=hop)

    for i, s in enumerate(sfbt):
        print(s)
        print("ssss")
        diff = sft[i] - s
        print(diff)
        print("DIFFFF")
        end = sft[i] + diff + hop
        start = s - hop
        if start < 0:
            start = 0
        if end > len(track):
            print("DONE")
            break
        new = track[start:end]
        newname = fname + str(i) + ".wav"
        print(new)
        print(newname)

        sf.write(newname, new, sr, "PCM_24")


folder = os.fsencode(apath)
files = []
for file in os.listdir(folder):
    f = file.decode("utf-8")

    fpath = folder.decode("utf-8") + f
    print(fpath)

    files.append(fpath)


for fp in files:
    fp = str(fp)
    track, sr = librosa.load(fp, sr=sr, offset=0.5, duration=None, mono=True)

    low = librosa.effects.percussive(track)
    high = librosa.effects.harmonic(track)

    process_samples(low, newpath + "perc_")
    # process_samples(high, newpath + "harm_")
    # process_samples(track, newpath + "def_")
