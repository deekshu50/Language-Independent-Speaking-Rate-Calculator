import os
import glob
import numpy as np
import pandas as pd
import librosa
from scipy.signal import find_peaks

# --- Configuration ---
WAV_DIR = "wav"
OUTPUT_FILE = "results.txt"
# [CHANGE 1] Added 'Avg Energy (Non-Silent)' to columns
OUTPUT_COLUMNS = [
    "File Name",
    "Duration (sec)",
    "Speaking Rate (syllables/sec)",
    "Avg Energy (Non-Silent)",
]

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
    Analyzes audio waveform to count syllable nuclei and calculate average energy.
    """
    filename = os.path.basename(file_path)

    try:
        # Load audio
        y, sr = librosa.load(file_path, sr=None)

        # Calculate Duration
        duration_sec = librosa.get_duration(y=y, sr=sr)

        # Extract Intensity Envelope (RMS)
        hop_length = 512
        rms_energy = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop_length)[
            0
        ]

        # Normalize RMS (0 to 1 scale)
        if np.max(rms_energy) - np.min(rms_energy) == 0:
            rms_normalized = rms_energy  # Handle absolute silence case
        else:
            rms_normalized = (rms_energy - np.min(rms_energy)) / (
                np.max(rms_energy) - np.min(rms_energy)
            )

        # --- [CHANGE 2] Calculate Average Energy (Ignoring Silence) ---
        # We consider "non-silence" as any frame with energy > MIN_PEAK_HEIGHT
        # This prevents the silence between sentences from dragging down the average.
        non_silent_frames = rms_normalized[rms_normalized > MIN_PEAK_HEIGHT]

        if len(non_silent_frames) > 0:
            avg_energy = np.mean(non_silent_frames)
        else:
            avg_energy = 0.0

        # Peak Detection
        time_per_frame = hop_length / sr
        min_distance_indices = int(MIN_PEAK_DISTANCE_SEC / time_per_frame)

        peaks, _ = find_peaks(
            rms_normalized, height=MIN_PEAK_HEIGHT, distance=min_distance_indices
        )

        syllable_count = len(peaks)

        # Calculate Speaking Rate
        if duration_sec > 0:
            rate_sps = syllable_count / duration_sec
        else:
            rate_sps = 0

        # --- [CHANGE 3] Add new metric to return dictionary ---
        return {
            OUTPUT_COLUMNS[0]: filename,
            OUTPUT_COLUMNS[1]: round(duration_sec, 2),
            OUTPUT_COLUMNS[2]: round(rate_sps, 2),
            OUTPUT_COLUMNS[3]: round(avg_energy, 4),  # 4 decimal places for precision
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
        # Format output
        table_string = df.to_string(index=False)

        print("\n" + "=" * 80)  # Made the separator line longer
        print(table_string)
        print("=" * 80 + "\n")

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
