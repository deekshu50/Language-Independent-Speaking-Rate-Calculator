# 🗣️ Language-Independent Speaking Rate Calculator

This project is a Python-based tool that calculates the speaking rate and average energy of audio files. Unlike traditional tools that rely on Speech-to-Text (ASR) transcription, this program uses **Signal Processing** to detect syllable nuclei (energy peaks) in the audio waveform.

This makes the tool **language-independent**, faster, and capable of running without heavy machine learning models.

## 📂 Project Structure

Ensure your directory is organized as follows before running the program:

```text
SpeakingRateProject/
├── wav/                     # 📂 PLACE YOUR .WAV FILES HERE
│   ├── recording_1.wav
│   ├── interview_fr.wav
│   └── speech_test.wav
├── main.py                  # 🐍 The main Python script
├── requirements.txt         # 📦 List of dependencies
├── results.txt              # 📄 Output file (Generated automatically)
└── README.md                # 📖 This file
```

## 🧠 The Logic

The program performs two main analyses on the audio waveform:

### 1\. Speaking Rate (Syllables/Sec)

Instead of transcribing words, we calculate the rate in **Syllables Per Second (SPS)**:

1.  **Envelope Extraction:** Calculates the Root Mean Square (RMS) Energy to map "loudness" over time.
2.  **Peak Detection:** Uses `scipy.signal.find_peaks` to find vowels (syllable nuclei).
      * *Filters:* Applies a minimum height threshold to ignore background noise and a minimum distance threshold to prevent double-counting long vowels.
3.  **Formula:** $\text{Speaking Rate} = \frac{\text{Total Peaks}}{\text{Duration (sec)}}$

### 2\. Average Energy (Non-Silent)

Calculates how "energetic" or loud the speaker is, relative to their own peak volume.

1.  **Normalization:** The audio energy is scaled between 0.0 (silence) and 1.0 (loudest peak).
2.  **Silence Removal:** The program ignores any audio frames below the `MIN_PEAK_HEIGHT` threshold (silence or background hiss).
3.  **Averaging:** It calculates the mean of the remaining "active speech" frames.

## 🛠️ Installation

### 1\. Prerequisites

  * Python 3.8 or higher.

### 2\. Install Dependencies

Open your terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

*If you do not have a `requirements.txt` file yet, create one with the following content:*

```text
numpy
pandas
librosa
scipy
```

## 🚀 How to Run

1.  **Prepare Audio:** Place all your `.wav` files into the `wav` folder.
2.  **Run Script:** Execute the main script via terminal:
    ```bash
    python main.py
    ```
3.  **View Results:**
      * The results will be displayed in the console.
      * A file named **`results.txt`** will be generated (or overwritten) in the project folder containing the formatted table.

## ⚙️ Configuration (Tuning)

You can adjust the sensitivity of the analysis by modifying the constants at the top of `main.py`:

  * **`MIN_PEAK_HEIGHT` (Default: 0.02):**
      * The threshold for what counts as "sound" vs "silence."
      * Increase this (e.g., to 0.05) if your audio has background noise.
  * **`MIN_PEAK_DISTANCE_SEC` (Default: 0.1):**
      * The minimum time (100ms) required between two syllables.
      * Decrease this if the speaker talks extremely fast.

## 📄 Output Example

The content of `results.txt` will look like this:

| File Name | Duration (sec) | Speaking Rate (syllables/sec) | Avg Energy (Non-Silent) |
| :--- | :--- | :--- | :--- |
| `recording_1.wav` | 12.50 | 4.20 | 0.4521 |
| `interview_fr.wav` | 45.00 | 3.85 | 0.3810 |
| `speech_test.wav` | 5.20 | 0.00 | 0.0000 |

*Note: **Avg Energy** is normalized (0-1). A value of 0.45 means the average active speech volume is 45% of the maximum peak volume in that file.*

-----

### Next Step for you:

Would you like to automate this further by adding a feature to **bulk rename** the input files (e.g., `file1.wav`, `file2.wav`) before processing them, so your output table is cleaner?