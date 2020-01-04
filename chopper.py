import os
import librosa
import soundfile as sf
import numpy as np

apath = "./assets/"
newpath = "./new/samples"

os.system("rm -rf new")
os.system("mkdir new")


def smooth(current_slice, fade_length=1024):
    incr = 1 / fade_length
    fadeOut = 0
    original_incr = 1 / fade_length

    for i, sample in enumerate(current_slice[:fade_length]):
        current_slice[i] = sample * incr
        current_slice[(i + 1) * -1] = current_slice[(i + 1) * -1] * incr # * (fadeOut += incr)
        incr += original_incr
        if incr >= .999:
            break
        # if incr <= 0.001
        #     break

    return current_slice


def get_end_indices(peaks, energy):
    # Find points where energy is non-increasing
    # all points:  energy[i] <= energy[i-1]
    # tail points: energy[i] < energy[i+1]
    minima = np.flatnonzero((energy[1:-1] <= energy[:-2]) & (energy[1:-1] < energy[2:]))
    # Pad on a 0, just in case we have onsets with no preceding minimum
    # Shift by one to account for slicing in minima detection
    minima = librosa.util.fix_frames(1 + minima, x_min=0)
    print(minima)
    print(peaks)
    # Only match going right from the detected events
    return minima[librosa.util.match_events(peaks, minima, left=False, right=True)]


def process_samples(track, fname, sr, hop=2048):

    oenv = librosa.onset.onset_strength(y=track, sr=sr, hop_length=hop)

    onsets = librosa.onset.onset_detect(onset_envelope=oenv, backtrack=False)

    onset_bt = librosa.onset.onset_backtrack(onsets, oenv)

    # onset_ft = get_end_indices(onsets, oenv)

    peaks = librosa.frames_to_samples(onsets, hop_length=hop)
    sample_starts = librosa.frames_to_samples(onset_bt, hop_length=hop)
    # sample_ends = librosa.frames_to_samples(onset_ft, hop_length=hop)
    # rack = []
    track_length = len(track)
    for i, start in enumerate(sample_starts):
        # real_start = start if start - hop < 0 else start - hop
        peak = peaks[i]
        end = sample_starts[i + 1] if i + 1 < len(sample_starts) else -1
        # real_end = end if end + hop > track_length else end + hop
        print(start)
        print("start")
        print(peaks[i])
        print("peak")
        print(end)
        print("end")

        raw = track[start:end]
        # Strip trailing silence
        trimmed, _ = librosa.effects.trim(raw)
        # Add short silence before and after.
        # padded = librosa.util.pad_center(trimmed, len(trimmed) + 1028, mode="constant")
        faded = smooth(trimmed)

        # print(trimmed)
        # print("trimmed clip")

        newname = fname + str(i) + ".wav"
        print(newname)

        sf.write(newname, faded, sr)


folder = os.fsencode(apath)
files = []
for file in os.listdir(folder):
    f = file.decode("utf-8")

    fpath = folder.decode("utf-8") + f
    print(fpath)

    files.append(fpath)


for fp in files:
    fp = str(fp)
    track, sr = librosa.load(fp, sr=None, offset=18, duration=10)
    print(f"Sample Rate is set to {sr}")

    # TODO: Optionally support percussive sampling.
    # track = librosa.resample(tr, sr, 44100)
    # low = librosa.effects.percussive(track)
    # high = librosa.effects.harmonic(track)
    #
    # process_samples(low, newpath + "perc_", sr=sr)
    # process_samples(high, newpath + "harm_")
    process_samples(track, newpath + "_full_", sr)
