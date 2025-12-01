# 🗣️ Language-Independent Speaking Rate Calculator

This project is a Python-based tool that calculates the speaking rate of audio files. Unlike traditional tools that rely on Speech-to-Text (ASR) transcription, this program uses **Signal Processing** to detect syllable nuclei (energy peaks) in the audio waveform.

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

## 🧠 The Logic: Syllable Nuclei Counting

Since we are not transcribing words, we calculate the rate in **Syllables Per Second (SPS)** using the following acoustic approach:

1.  **Audio Loading:** The program loads the `.wav` file at its native sampling rate.
2.  **Envelope Extraction:** It calculates the **Root Mean Square (RMS) Energy** of the waveform. This creates a smooth curve representing the "loudness" or intensity over time.
3.  **Peak Detection:**
      * Speech is rhythmic. Syllables typically correspond to peaks in the energy envelope (vowels are louder than consonants).
      * The program uses `scipy.signal.find_peaks` to identify these local maxima.
      * **Filters:** It applies a minimum height threshold (to ignore background noise) and a minimum distance threshold (to prevent counting one long vowel as multiple syllables).
4.  **Calculation:**
    $$\text{Speaking Rate} = \frac{\text{Total Detected Peaks}}{\text{Duration (seconds)}}$$

## 🛠️ Installation

### 1\. Prerequisites

  * Python 3.8 or higher.

### 2\. Install Dependencies

Open your terminal or command prompt in the project folder and run:

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

If you find the detection is too sensitive (counting noise) or not sensitive enough (missing soft speech), you can adjust the constants at the top of `main.py`:

  * **`MIN_PEAK_HEIGHT` (Default: 0.02):**
      * Increase this value (e.g., to 0.05) if your audio has background noise.
      * Decrease it if the speakers are very quiet.
  * **`MIN_PEAK_DISTANCE_SEC` (Default: 0.1):**
      * This represents the minimum time (100ms) between syllables.
      * Decrease this if the speaker talks extremely fast.

## 📄 Output Example

The content of `results.txt` will look like this:

```text
File Name         Duration (sec)  Speaking Rate (syllables/sec)
recording_1.wav            12.50                           4.20
interview_fr.wav           45.00                           3.85
speech_test.wav             5.20                           0.00
```