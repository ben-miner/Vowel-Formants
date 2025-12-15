import pandas as pd

# Load your exported sheet
df_wide = pd.read_csv("vowel_data_wide.csv")

# Keep only the 10 speaker rows, ignore p-value row if it’s there
df_wide = df_wide.iloc[:10]

df_wide.head()

# Pick out the four relevant columns for /æ/ F1
ae_f1_cols = [
    "Straight_M_æ_F1Bark",
    "Gay_M_æ_F1Bark",
    "Straight_W_æ_F1Bark",
    "Gay_W_æ_F1Bark",
]

ae_f1 = df_wide[ae_f1_cols].copy()

# Melt from wide → long
ae_f1_long = ae_f1.melt(var_name="GroupCol", value_name="F1_Bark")

ae_f1_long.head()

# Orientation: Straight vs LGBTQ+ (Gay)
ae_f1_long["Orientation"] = ae_f1_long["GroupCol"].apply(
    lambda s: "LGBTQ+" if "Gay" in s else "Straight"
)


# Sex: M vs W
def extract_sex(s):
    if "_M_" in s:
        return "men"
    elif "_W_" in s:
        return "women"
    else:
        return "unknown"


ae_f1_long["Sex"] = ae_f1_long["GroupCol"].apply(extract_sex)

ae_f1_long.head()

import statsmodels.api as sm
from statsmodels.formula.api import ols

# Fit the 2x2 ANOVA model for /æ/ F1
model_ae_f1 = ols("F1_Bark ~ C(Sex) * C(Orientation)", data=ae_f1_long).fit()

anova_ae_f1 = sm.stats.anova_lm(model_ae_f1, typ=2)
print(anova_ae_f1)


def make_long_anova(df, col_map, dv_name):
    """
    df: wide dataframe
    col_map: dict {"Straight_M": colname, "Gay_M": colname, "Straight_W": colname, "Gay_W": colname}
    dv_name: name for dependent variable, e.g. "F1_Bark"
    """
    cols = list(col_map.values())
    sub = df[cols].copy()
    long = sub.melt(var_name="GroupCol", value_name=dv_name)

    long["Orientation"] = long["GroupCol"].apply(
        lambda s: "LGBTQ+" if "Gay" in s else "Straight"
    )

    def extract_sex(s):
        if "_M_" in s:
            return "men"
        elif "_W_" in s:
            return "women"
        else:
            return "unknown"

    long["Sex"] = long["GroupCol"].apply(extract_sex)
    return long


# Example: /ɛ/ F1
eps_f1_cols = {
    "Straight_M": "Straight_M_ɛ_F1Bark",
    "Gay_M": "Gay_M_ɛ_F1Bark",
    "Straight_W": "Straight_W_ɛ_F1Bark",
    "Gay_W": "Gay_W_ɛ_F1Bark",
}

eps_f1_long = make_long_anova(df_wide, eps_f1_cols, "F1_Bark")

model_eps_f1 = ols("F1_Bark ~ C(Sex) * C(Orientation)", data=eps_f1_long).fit()
print(sm.stats.anova_lm(model_eps_f1, typ=2))
# You can repeat the above for F2 or other vowels as needed
# ---- Define column maps for each vowel × formant ----

ae_f1_cols = {
    "Straight_M": "Straight_M_æ_F1Bark",
    "Gay_M": "Gay_M_æ_F1Bark",
    "Straight_W": "Straight_W_æ_F1Bark",
    "Gay_W": "Gay_W_æ_F1Bark",
}

ae_f2_cols = {
    "Straight_M": "Straight_M_æ_F2Bark",
    "Gay_M": "Gay_M_æ_F2Bark",
    "Straight_W": "Straight_W_æ_F2Bark",
    "Gay_W": "Gay_W_æ_F2Bark",
}

eps_f1_cols = {
    "Straight_M": "Straight_M_ɛ_F1Bark",
    "Gay_M": "Gay_M_ɛ_F1Bark",
    "Straight_W": "Straight_W_ɛ_F1Bark",
    "Gay_W": "Gay_W_ɛ_F1Bark",
}

eps_f2_cols = {
    "Straight_M": "Straight_M_ɛ_F2Bark",
    "Gay_M": "Gay_M_ɛ_F2Bark",
    "Straight_W": "Straight_W_ɛ_F2Bark",
    "Gay_W": "Gay_W_ɛ_F2Bark",
}

# ---- Helper to run 2×2 ANOVA and reshape output ----


def run_anova_and_collect(df_wide, col_map, dv_name, vowel_label, formant_label):
    """
    df_wide: wide dataframe with columns for each group
    col_map: dict mapping group labels to column names
    dv_name: name to give the dependent variable (e.g. "F1_Bark", "F2_Bark")
    vowel_label: e.g. "æ" or "ɛ"
    formant_label: e.g. "F1" or "F2"
    """
    long_df = make_long_anova(df_wide, col_map, dv_name)
    model = ols(f"{dv_name} ~ C(Sex) * C(Orientation)", data=long_df).fit()
    anova_df = sm.stats.anova_lm(model, typ=2).reset_index()

    # Rename for consistency
    anova_df = anova_df.rename(
        columns={
            "index": "Effect",
            "sum_sq": "sum_sq",
            "df": "df",
            "F": "F",
            "PR(>F)": "p_value",
        }
    )

    # Add vowel + formant labels
    anova_df["Vowel"] = vowel_label
    anova_df["Formant"] = formant_label

    # Reorder columns
    anova_df = anova_df[["Vowel", "Formant", "Effect", "sum_sq", "df", "F", "p_value"]]
    return anova_df


# ---- Run for all 4 combos: æ/ɛ × F1/F2 ----

results_list = []

results_list.append(
    run_anova_and_collect(
        df_wide, ae_f1_cols, "F1_Bark", vowel_label="æ", formant_label="F1"
    )
)
results_list.append(
    run_anova_and_collect(
        df_wide, ae_f2_cols, "F2_Bark", vowel_label="æ", formant_label="F2"
    )
)
results_list.append(
    run_anova_and_collect(
        df_wide, eps_f1_cols, "F1_Bark", vowel_label="ɛ", formant_label="F1"
    )
)
results_list.append(
    run_anova_and_collect(
        df_wide, eps_f2_cols, "F2_Bark", vowel_label="ɛ", formant_label="F2"
    )
)

anova_summary = pd.concat(results_list, ignore_index=True)

print(anova_summary)

# Optionally, save to CSV so you can drop it into Sheets or your paper
anova_summary.to_csv("anova_summary_table.csv", index=False)
