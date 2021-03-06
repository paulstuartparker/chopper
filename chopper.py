import os
import librosa
import soundfile as sf
import numpy as np


class Chopper:
    def __init__(self, input_path=None, output_directory=None):
        self.input_path = input_path if input_path else "./assets/"
        self.output_path = output_directory if output_directory else "./output/samples"
        self.hop_length = 512

    def set_fade_len(self, newlength):
        self.fade_len = int(newlength)

    def set_hop_length(self, hop_length):
        self.hop_length = int(hop_length)

    def set_input_path(self):
        pass

    def set_output_path(self):
        pass

    def chop(self):
        self.reset_tmp_directory()
        self.input_file_paths, self.filenames = self.collect_input_file_paths()
        self.fade_len = 441
        self.chop_audio_files()

    def reset_tmp_directory(self):
        """
        DANGER ZONE
        Nuke output directory and then create new
        """
        os.system(f"rm -rf ./.tmp_samples")
        os.system(f"mkdir ./.tmp_samples")

    def fade_edges_linear(self, audio_slice):
        current_gain = 1 / self.fade_len
        original_incr = 1 / self.fade_len

        for i, sample in enumerate(audio_slice[: self.fade_len]):
            audio_slice[i] = sample * current_gain
            audio_slice[(i + 1) * -1] = audio_slice[(i + 1) * -1] * current_gain
            current_gain += original_incr
            if current_gain >= 0.99999:
                break

        return audio_slice

    def extract_samples(self, track, fname, sr):

        oenv = librosa.onset.onset_strength(y=track, sr=sr, hop_length=self.hop_length)

        onsets = librosa.onset.onset_detect(onset_envelope=oenv, backtrack=False)

        onset_bt = librosa.onset.onset_backtrack(onsets, oenv)

        peaks = librosa.frames_to_samples(onsets, hop_length=self.hop_length)
        sample_starts = librosa.frames_to_samples(onset_bt, hop_length=self.hop_length)

        track_length = len(track)
        for i, start in enumerate(sample_starts):
            peak = peaks[i]
            end = sample_starts[i + 1] if i + 1 < len(sample_starts) else -1

            raw = track[start:end]
            # Strip trailing silence
            trimmed, _ = librosa.effects.trim(raw)

            # Apply linear fade in/out
            faded = self.fade_edges_linear(trimmed)

            newname = fname + str(i) + ".wav"
            print(newname)

            sf.write(newname, faded, sr)

    def collect_input_file_paths(self):
        input_dir = os.fsencode(self.input_path)
        input_file_paths = []
        filenames = []
        for file in os.listdir(input_dir):
            f = file.decode("utf-8")

            if f == ".DS_Store":
                continue
            fpath = input_dir.decode("utf-8") + f
            print(fpath)

            input_file_paths.append(fpath)
            filenames.append(f)
            print(fpath)
            print(filenames)
            print(input_file_paths)
        return input_file_paths, filenames

    def chop_audio_files(self):
        for idx, fp in enumerate(self.input_file_paths):
            fp = str(fp)
            print(fp)
            track, sr = librosa.load(fp, sr=None, offset=0, duration=None)
            print(f"Sample Rate is set to {sr}")

            # TODO: Optionally support percussive sampling.
            # track = librosa.resample(tr, sr, 44100)
            # low = librosa.effects.percussive(track)
            # high = librosa.effects.harmonic(track)
            #
            # process_samples(low, newpath + "perc_", sr=sr)
            # process_samples(high, newpath + "harm_")
            self.extract_samples(track, self.output_path + "_full_", sr)
