import pathlib

import pandas as pd
import parselmouth
from parselmouth.praat import call


def extract_formants_for_file(
    wav_path,
    textgrid_path,
    vowel_tier_name="vowels",
    max_formant=5500,
    num_formants=5,
    time_step=0.01,
    window_length=0.025,
):
    """
    Extract F1 and F2 at the midpoint of each vowel interval in the given TextGrid.

    Parameters
    ----------
    wav_path : Path
        Path to the .wav file.
    textgrid_path : Path
        Path to the matching .TextGrid file.
    vowel_tier_name : str
        Name of the tier that contains vowel intervals.
    max_formant : float
        Maximum formant frequency (Praat setting).
        ~5500 Hz is typical for female/mixed; ~5000 for male-only data.
    num_formants : int
        Number of formants to track.
    time_step : float
        Time step for formant analysis (seconds).
    window_length : float
        Window length for formant analysis (seconds).

    Returns
    -------
    pandas.DataFrame
        Rows: one vowel token
        Columns: file, vowel_label, t_mid, F1_Hz, F2_Hz
    """
    # Convert to Path objects if strings
    wav_path = pathlib.Path(wav_path)
    textgrid_path = pathlib.Path(textgrid_path)

    # Check if files exist
    if not wav_path.exists():
        raise FileNotFoundError(f"WAV file not found: {wav_path}")
    if not textgrid_path.exists():
        raise FileNotFoundError(f"TextGrid file not found: {textgrid_path}")

    # Load sound
    sound = parselmouth.Sound(str(wav_path))

    # Make a Formant object using Praat's "To Formant (burg)..."
    formant = call(
        sound,
        "To Formant (burg)",
        0.0,  # time step (0 = auto)
        num_formants,  # number of formants
        max_formant,  # max formant (Hz)
        window_length,
        50.0,  # pre-emphasis from (Hz)
    )

    # Load TextGrid
    tg = parselmouth.read(str(textgrid_path))  # returns a TextGrid object

    # Find the tier by name using Praat commands
    num_tiers = call(tg, "Get number of tiers")
    tier_index = None
    for i in range(1, num_tiers + 1):
        tier_name = call(tg, "Get tier name", i)
        if tier_name == vowel_tier_name:
            tier_index = i
            break

    if tier_index is None:
        raise ValueError(f"Tier named '{vowel_tier_name}' not found in TextGrid.")

    rows = []

    # Get intervals using Praat commands directly on the TextGrid with tier number
    num_intervals = call(tg, "Get number of intervals", tier_index)
    for i in range(1, num_intervals + 1):
        label = call(tg, "Get label of interval", tier_index, i)
        label = label.strip() if label else ""
        # Skip empty or silence intervals
        if not label:
            continue

        # Get start and end times, then calculate midpoint
        t_start = call(tg, "Get start point", tier_index, i)
        t_end = call(tg, "Get end point", tier_index, i)
        t_mid = (t_start + t_end) / 2

        # Query Praat for F1 and F2
        f1 = call(formant, "Get value at time", 1, t_mid, "Hertz", "Linear")
        f2 = call(formant, "Get value at time", 2, t_mid, "Hertz", "Linear")

        # Praat returns NaN sometimes if formant tracking fails; you can skip those
        if f1 is None or f2 is None:
            continue

        rows.append(
            {
                "file": wav_path.name,
                "vowel_label": label,
                "t_mid_s": t_mid,
                "F1_Hz": f1,
                "F2_Hz": f2,
            }
        )

    return pd.DataFrame(rows)


def extract_formants_for_directory(
    data_dir="data",
    vowel_tier_name="vowels",
    max_formant=5500,
    num_formants=5,
):
    """
    Loop over all .wav files in a directory, look for matching .TextGrids,
    and combine all results in one DataFrame.
    """
    data_dir = pathlib.Path(data_dir)

    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    all_dfs = []

    for wav_path in sorted(data_dir.glob("*.wav")):
        textgrid_path = wav_path.with_suffix(".TextGrid")
        if not textgrid_path.exists():
            print(f"⚠️ No TextGrid for {wav_path.name}, skipping.")
            continue

        print(f"Processing {wav_path.name}...")
        df = extract_formants_for_file(
            wav_path,
            textgrid_path,
            vowel_tier_name=vowel_tier_name,
            max_formant=max_formant,
            num_formants=num_formants,
        )
        all_dfs.append(df)

    if not all_dfs:
        print("No data extracted. Check your paths and TextGrids.")
        return pd.DataFrame()

    big_df = pd.concat(all_dfs, ignore_index=True)
    return big_df


if __name__ == "__main__":
    # Adjust these if needed
    DATA_DIR = "data"  # folder with .wav and .TextGrid files
    VOWEL_TIER = "vowels"  # name of the tier in your TextGrids
    MAX_FORMANT = 5500  # tweak if your speakers are mostly male/female
    NUM_FORMANTS = 5

    df_all = extract_formants_for_directory(
        data_dir=DATA_DIR,
        vowel_tier_name=VOWEL_TIER,
        max_formant=MAX_FORMANT,
        num_formants=NUM_FORMANTS,
    )

    # Display table
    print(df_all)

    # Optionally, save to CSV for R/Python plotting
    df_all.to_csv("formants_all_participants.csv", index=False)
    print("\nSaved table to formants_all_participants.csv")
