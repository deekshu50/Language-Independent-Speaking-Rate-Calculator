import os
import glob
import numpy as np
import pandas as pd
import librosa
from scipy.signal import find_peaks

# --- Configuration ---
WAV_DIR = "wav"
OUTPUT_FILE = "results.txt"
OUTPUT_COLUMNS = ["File Name", "Duration (sec)", "Speaking Rate (syllables/sec)"]

# Signal Processing Hyperparameters
MIN_PEAK_HEIGHT = 0.02
MIN_PEAK_DISTANCE_SEC = 0.1


def get_audio_files(directory):
    """Finds all .wav files in the specified directory."""
    if not os.path.exists(directory):
        print(
            f"Error: Directory '{directory}' not found. Please create it and add .wav files."
        )
        return []

    files = glob.glob(os.path.join(directory, "*.wav"))
    return files


def calculate_rate(file_path):
    """
    Analyzes audio waveform to count syllable nuclei (peaks in energy)
    and returns filename, duration, and rate.
    """
    filename = os.path.basename(file_path)

    try:
        # Load audio (native sampling rate)
        y, sr = librosa.load(file_path, sr=None)

        # Calculate Duration
        duration_sec = librosa.get_duration(y=y, sr=sr)

        # Extract Intensity Envelope (RMS)
        hop_length = 512
        rms_energy = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop_length)[
            0
        ]

        # Peak Detection
        time_per_frame = hop_length / sr
        min_distance_indices = int(MIN_PEAK_DISTANCE_SEC / time_per_frame)

        rms_normalized = (rms_energy - np.min(rms_energy)) / (
            np.max(rms_energy) - np.min(rms_energy)
        )

        peaks, _ = find_peaks(
            rms_normalized, height=MIN_PEAK_HEIGHT, distance=min_distance_indices
        )

        syllable_count = len(peaks)

        # Calculate Speaking Rate
        if duration_sec > 0:
            rate_sps = syllable_count / duration_sec
        else:
            rate_sps = 0

        return {
            OUTPUT_COLUMNS[0]: filename,
            OUTPUT_COLUMNS[1]: round(duration_sec, 2),
            OUTPUT_COLUMNS[2]: round(rate_sps, 2),
        }

    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return None


def main():
    print("--- Starting Speaking Rate Analysis ---")
    files = get_audio_files(WAV_DIR)

    if not files:
        print("No .wav files found.")
        return

    results = []

    print(f"Processing {len(files)} files...")

    for file_path in files:
        data = calculate_rate(file_path)
        if data:
            results.append(data)

    # Create DataFrame
    df = pd.DataFrame(results)

    if not df.empty:
        # 1. Print to console
        table_string = df.to_string(index=False)
        print("\n" + "=" * 60)
        print(table_string)
        print("=" * 60 + "\n")

        # 2. Save to .txt file (Writing the formatted string to preserve alignment)
        try:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(table_string)
            print(f"✅ Results successfully saved to '{OUTPUT_FILE}'")
        except Exception as e:
            print(f"❌ Error saving text file: {e}")

    else:
        print("No results generated.")


if __name__ == "__main__":
    main()
