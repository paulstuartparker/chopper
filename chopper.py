# import the os module
import os
import librosa
import soundfile as sf
import numpy as np

apath = "./assets/"
newpath = "./new/samples"
hop = 2048
sr = 44100
os.system("rm -rf new")
os.system("mkdir new")


def process_samples(track, fname, sr=44100, hop=2048):

    oenv = librosa.onset.onset_strength(y=track, sr=sr, hop_length=hop)

    onsets = librosa.onset.onset_detect(onset_envelope=oenv, backtrack=False)

    onset_bt = librosa.onset.onset_backtrack(onsets, oenv)

    sft = librosa.frames_to_samples(onsets, hop_length=hop)
    sfbt = librosa.frames_to_samples(onset_bt, hop_length=hop)

    for i, s in enumerate(sfbt):

        diff = sft[i] - s
        if i + 1 < len(sft):
            end = sft[i + 1] - 512
        else:
            end = sft[i] + diff
        start = s - 512

        if start < 0:
            start = 0
        if end > len(track):
            print("DONE")
            break
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
    track, sr = librosa.load(fp, sr=sr, offset=0.5, duration=15, mono=True)

    low = librosa.effects.percussive(track)
    # high = librosa.effects.harmonic(track)
    #
    process_samples(low, newpath + "perc_")
    # process_samples(high, newpath + "harm_")
    # process_samples(track, newpath + "def_")
