[README.md](https://github.com/user-attachments/files/24093199/README.md)
# PhonPhon Squib

A Python tool for extracting and analyzing vowel formants (F1 and F2) from audio recordings using Praat's formant analysis algorithms.

## Overview

This project extracts F1 and F2 formant frequencies from audio files with corresponding TextGrid annotations. It processes multiple participants' speech data and generates aggregated statistics showing average formant values for each vowel type per participant.

## Features

- Extract F1 and F2 formants at the midpoint of each vowel interval
- Process multiple audio files and TextGrid pairs automatically
- Aggregate formant data by participant and vowel label
- Export results to CSV for further analysis

## Requirements

- Python 3.7+
- pandas >= 1.3.0
- parselmouth >= 0.3.0 (Python wrapper for Praat)

## Installation

1. Clone or download this repository

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
.
├── data/                          # Audio and TextGrid files
│   ├── *.wav                      # Audio recordings
│   └── *.TextGrid                 # Praat TextGrid annotations
├── extract_formants.py           # Main script for formant extraction
├── aggregate_formants.py          # Script to aggregate formant data
├── formants_all_participants.csv  # Output: aggregated formant data
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Usage

### Step 1: Prepare Your Data

1. Place your audio files (`.wav`) in the `data/` directory
2. Place corresponding TextGrid files (`.TextGrid`) in the same directory
3. Ensure TextGrid files have a tier named `"vowels"` containing vowel interval labels
4. Name files consistently (e.g., `participant_speech - Name.wav` and `participant_speech - Name.TextGrid`)

### Step 2: Extract Formants

Run the main extraction script:

```bash
python extract_formants.py
```

This will:
- Process all `.wav` files in the `data/` directory
- Extract F1 and F2 formants at the midpoint of each vowel interval
- Save individual measurements to `formants_all_participants.csv`

### Step 3: Aggregate Data (Optional)

If you want to see average formants per participant and vowel label:

```bash
python aggregate_formants.py
```

This will update `formants_all_participants.csv` with aggregated averages.

## Configuration

You can modify the following parameters in `extract_formants.py`:

- `DATA_DIR`: Directory containing audio and TextGrid files (default: `"data"`)
- `VOWEL_TIER`: Name of the TextGrid tier containing vowels (default: `"vowels"`)
- `MAX_FORMANT`: Maximum formant frequency in Hz (default: `5500` for female/mixed speakers, use `5000` for male speakers)
- `NUM_FORMANTS`: Number of formants to track (default: `5`)

## Output Format

The `formants_all_participants.csv` file contains:

### Individual Measurements (after extraction)
- `file`: Source audio file name
- `vowel_label`: Vowel label from TextGrid
- `t_mid_s`: Midpoint time of vowel interval (seconds)
- `F1_Hz`: First formant frequency (Hz)
- `F2_Hz`: Second formant frequency (Hz)

### Aggregated Data (after aggregation)
- `participant`: Participant identifier (extracted from filename)
- `vowel_label`: Vowel label
- `F1_Hz`: Average first formant frequency (Hz)
- `F2_Hz`: Average second formant frequency (Hz)

## Example Output

After aggregation, the CSV will look like:

```
participant,vowel_label,F1_Hz,F2_Hz
anjali,æ,935.74,1578.22
anjali,ɛ,800.52,1835.35
ariana,æ,885.35,1748.21
ariana,ɛ,743.29,1860.23
```

## Notes

- Formant extraction uses Praat's "To Formant (burg)" algorithm
- Values are extracted at the temporal midpoint of each vowel interval
- Missing or failed formant measurements are automatically skipped
- The aggregation script extracts participant names from filenames using the pattern `participant_speech - ...`

## Troubleshooting

- **FileNotFoundError**: Ensure your audio and TextGrid files are in the correct directory
- **Tier not found**: Verify your TextGrid files have a tier named `"vowels"` (or update `VOWEL_TIER` in the script)
- **No formants extracted**: Check that your TextGrid intervals are properly labeled (non-empty)

## License

This project is provided as-is for research and educational purposes.

