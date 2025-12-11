import pandas as pd

# Read the CSV file
df = pd.read_csv("formants_all_participants.csv")

# Extract participant name from file column
# Pattern: "anjali_speech - Anjali Camilla Mignone.wav" -> "anjali"
df["participant"] = df["file"].str.extract(r"^(\w+)_speech")

# Group by participant and vowel_label, calculate mean F1 and F2
summary = (
    df.groupby(["participant", "vowel_label"])
    .agg({"F1_Hz": "mean", "F2_Hz": "mean"})
    .reset_index()
)

# Round to 2 decimal places
summary["F1_Hz"] = summary["F1_Hz"].round(2)
summary["F2_Hz"] = summary["F2_Hz"].round(2)

# Sort by participant and vowel_label for better readability
summary = summary.sort_values(["participant", "vowel_label"])

# Save to CSV
summary.to_csv("formants_all_participants.csv", index=False)

# Display the result
print(summary.to_string(index=False))
