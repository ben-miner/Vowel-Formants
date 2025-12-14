import matplotlib.pyplot as plt

# ====== Your data ======
# (F1 Bark, F2 Bark, Group, Vowel)
points = [
    (7.010529067, 11.53497861, "Straight Men", "æ"),
    (6.179257678, 11.86160591, "Straight Men", "ɛ"),
    (6.859468387, 11.37427894, "Gay Men", "æ"),
    (5.950894348, 11.64776647, "Gay Men", "ɛ"),
    (7.759514788, 11.79000083, "Straight Women", "æ"),
    (6.889718308, 12.24447086, "Straight Women", "ɛ"),
    (7.841668436, 11.90776583, "Gay Women", "æ"),
    (6.973588317, 12.37903993, "Gay Women", "ɛ"),
]

# Colors for straight vs gay within each sex
color_map = {
    "Straight Men": "black",
    "Gay Men": "dimgray",
    "Straight Women": "black",
    "Gay Women": "dimgray",
}

# Split data into men vs women
men_points = [p for p in points if "Men" in p[2]]
women_points = [p for p in points if "Women" in p[2]]

# ====== Two subplots: Men (left) and Women (right) ======
fig, (ax_men, ax_women) = plt.subplots(1, 2, figsize=(10, 5), sharex=True, sharey=True)

# --- Men plot ---
for f1, f2, group, vowel in men_points:
    ax_men.text(
        f2, f1, vowel, fontsize=18, ha="center", va="center", color=color_map[group]
    )

ax_men.set_title("Men")
ax_men.set_xlabel("F2 (Bark)")
ax_men.set_ylabel("F1 (Bark)")

# --- Women plot ---
for f1, f2, group, vowel in women_points:
    ax_women.text(
        f2, f1, vowel, fontsize=18, ha="center", va="center", color=color_map[group]
    )

ax_women.set_title("Women")
ax_women.set_xlabel("F2 (Bark)")

# Same vowel-plot orientation on both:
ax_men.set_xlim(13, 11)  # reverse F2 axis
ax_men.set_ylim(8, 5)  # reverse F1 axis

# Hide top/right spines to match your style
for ax in (ax_men, ax_women):
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.set_aspect("equal", adjustable="box")

plt.tight_layout()
plt.show()
plt.savefig("vowel_plot.png", dpi=800)
