import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import Patch

df = pd.read_csv("vowel_data_wide.csv")
# print(df.columns)


def add_confidence_ellipse(ax, x, y, n_std=2.0, **kwargs):
    """
    Add a covariance-based ellipse for points (x, y) to the given axes.
    n_std = number of standard deviations (2 ≈ 95% region).
    """
    x = np.asarray(x)
    y = np.asarray(y)
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    # Covariance matrix and eigen-decomposition
    cov = np.cov(x, y)
    vals, vecs = np.linalg.eigh(cov)

    # Sort eigenvalues/vecs from largest to smallest
    order = vals.argsort()[::-1]
    vals = vals[order]
    vecs = vecs[:, order]

    # Angle of ellipse in degrees
    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))

    # Width, height of ellipse (2*n_std*sqrt(eigenvalue))
    width, height = 2 * n_std * np.sqrt(vals)

    # Center of ellipse = mean of data
    mean_x = np.mean(x)
    mean_y = np.mean(y)

    # Enable fill if facecolor is provided in kwargs
    fill = "facecolor" in kwargs or kwargs.get("fill", False)

    ell = Ellipse(
        (mean_x, mean_y),
        width=width,
        height=height,
        angle=theta,
        fill=fill,
        **kwargs,
    )
    ax.add_patch(ell)
    return ell


conditions = [
    # name, sex, vowel, F1 series, F2 series
    ("Straight men", "men", "æ", df["Straight_M_æ_F1Bark"], df["Straight_M_æ_F2Bark"]),
    ("Gay men", "men", "æ", df["Gay_M_æ_F1Bark"], df["Gay_M_æ_F2Bark"]),
    (
        "Straight women",
        "women",
        "æ",
        df["Straight_W_æ_F1Bark"],
        df["Straight_W_æ_F2Bark"],
    ),
    ("Gay women", "women", "æ", df["Gay_W_æ_F1Bark"], df["Gay_W_æ_F2Bark"]),
    ("Straight men", "men", "ɛ", df["Straight_M_ɛ_F1Bark"], df["Straight_M_ɛ_F2Bark"]),
    ("Gay men", "men", "ɛ", df["Gay_M_ɛ_F1Bark"], df["Gay_M_ɛ_F2Bark"]),
    (
        "Straight women",
        "women",
        "ɛ",
        df["Straight_W_ɛ_F1Bark"],
        df["Straight_W_ɛ_F2Bark"],
    ),
    ("Gay women", "women", "ɛ", df["Gay_W_ɛ_F1Bark"], df["Gay_W_ɛ_F2Bark"]),
]

ellipse_colors = {
    ("men", "Straight men"): "red",
    ("men", "Gay men"): "yellow",
    ("women", "Straight women"): "blue",
    ("women", "Gay women"): "purple",
}
linestyle_map = {
    "Straight men": "-",
    "Gay men": "--",
    "Straight women": "-",
    "Gay women": "--",
}
# Color map for ellipses
ellipse_colors = {
    ("men", "Straight men"): "red",
    ("men", "Gay men"): "yellow",
    ("women", "Straight women"): "blue",
    ("women", "Gay women"): "purple",
}

# ========= 4. Plot: men vs women panels =========
fig, (ax_men, ax_women) = plt.subplots(1, 2, figsize=(10, 5), sharex=True, sharey=True)

for name, sex, vowel, F1, F2 in conditions:
    ax = ax_men if sex == "men" else ax_women

    f1 = np.array(F1)
    f2 = np.array(F2)

    mean_f1 = f1.mean()
    mean_f2 = f2.mean()

    color = ellipse_colors[(sex, name)]

    # Shaded ellipse
    add_confidence_ellipse(
        ax,
        f2,  # x = F2
        f1,  # y = F1
        n_std=2.0,
        facecolor=color,
        edgecolor="black",
        alpha=0.25,
        linewidth=1.0,
    )

    # Determine font style based on straight vs gay
    # Bold for straight, italic for gay
    is_straight = "Straight" in name
    fontweight = "bold" if is_straight else "normal"
    fontstyle = "normal" if is_straight else "italic"

    # Use a darker version of the ellipse color for better readability
    # For yellow, use a darker color since yellow on light background is hard to read
    text_color = color
    if color == "yellow":
        text_color = "darkorange"  # darker orange for better contrast
    elif color == "purple":
        text_color = "darkviolet"  # darker purple for better contrast
    elif color == "red":
        text_color = "darkred"  # darker red for better contrast
    elif color == "blue":
        text_color = "darkblue"  # darker blue for better contrast

    # Vowel label at the mean point - color-coded and styled
    ax.text(
        mean_f2,
        mean_f1,
        vowel,
        fontsize=16,
        ha="center",
        va="center",
        color=text_color,
        fontweight=fontweight,
        fontstyle=fontstyle,
    )

# Axis orientation like a vowel plot (high F2 on left, high F1 on top)
for ax in (ax_men, ax_women):
    ax.set_xlabel("F2 (Bark)")
    ax.set_ylabel("F1 (Bark)")
    ax.set_aspect("equal", adjustable="box")

    # Tweak ranges if needed based on your data
    ax.set_xlim(13.5, 10.5)  # reversed F2 axis
    ax.set_ylim(8.5, 5.0)  # reversed F1 axis

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

ax_men.set_title("Men")
ax_women.set_title("Women")

# ========= 5. Legend =========
legend_patches = [
    Patch(facecolor="red", edgecolor="black", alpha=0.25, label="Straight men"),
    Patch(facecolor="yellow", edgecolor="black", alpha=0.25, label="Gay men"),
    Patch(facecolor="blue", edgecolor="black", alpha=0.25, label="Straight women"),
    Patch(facecolor="purple", edgecolor="black", alpha=0.25, label="Gay women"),
]
fig.legend(handles=legend_patches, loc="upper center", ncol=4)

plt.tight_layout(rect=[0, 0, 1, 0.9])  # leave room for legend at top
plt.show()
