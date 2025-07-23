import matplotlib.pyplot as plt
import numpy as np

# ---------- Step 1: Function to read .xvg ----------
def read_xvg(filename):
    x, y = [], []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith(('#', '@')):
                continue
            parts = line.strip().split()
            if len(parts) >= 2:
                x.append(int(float(parts[0])))
                y.append(float(parts[1]))
    return np.array(x), np.array(y)

# ---------- Step 2: Load RMSF data ----------
wt_file = r"C:\Users\Shami\OneDrive\Desktop\4th_sem_project\vav2\7msd_vav2_w\charmm-gui-5092896201\gromacs\analysis\rmsf1.xvg"
mut_file = r"C:\Users\Shami\OneDrive\Desktop\4th_sem_project\vav2\8mds_vav2_m_M@818\charmm-gui-5092896260\gromacs\analysis_c\rmsf1.xvg"
x_wt, wt_rmsf = read_xvg(wt_file)
x_mut, mut_rmsf = read_xvg(mut_file)

# ---------- Step 3: Domain Regions ----------
domains = [
    (1, 20, 'red', 'CH'),
    (198, 376, 'gray', 'DH'),
    (405, 512, 'cyan', 'PH'),
    (523, 572, 'lightgray', 'DAG-type'),
    (586, 652, 'green', 'SH3 1'),
    (673, 767, 'blue', 'SH2'),
    (816, 877, 'purple', 'SH3 2'),
]

# ---------- Step 4: Plot Setup ----------
fig, ax = plt.subplots(figsize=(14, 6))

# Plot RMSF lines
ax.plot(x_wt, wt_rmsf, label='Wild Type', color='blue')
ax.plot(x_mut, mut_rmsf, label='Mutant', color='red')

# Plot domain bars just below the x-axis (y=-0.15 level)
for start, end, color, label in domains:
    ax.axvspan(start, end, ymin=+0.01, ymax=+0.001, color=color, zorder=-1, clip_on=False)
    ax.text((start + end) // 2, 0.04, label, ha='center', va='center', fontsize=9, color='black')
    #ax.text(start, -0.18, str(start), ha='center', va='top', fontsize=8, color='black')
    #ax.text(end, -0.18, str(end), ha='center', va='top', fontsize=8, color='black')

# Annotate important residues
highlight_residues = {
    818: '818M'
}
for res, label in highlight_residues.items():
    try:
        idx = list(x_mut).index(res)
        y_val = mut_rmsf[idx]
        ax.annotate(label, xy=(res, y_val), xytext=(res, y_val + 0.9),
                    arrowprops=dict(arrowstyle='->', color='black'),
                    ha='center', fontsize=9)
    except ValueError:
        continue

# Axis labels, limits, and formatting
ax.set_xlabel("Residue Number")
ax.set_ylabel("RMSF (Å)")
ax.set_title("RMSF Comparison: Wild Type vs Mutant")
ax.legend()
ax.set_xlim(0, 900)
ax.set_ylim(0, 2.0)

# Extend space below axis for domain labels
ax.set_ylim(bottom=0, top=2.0)
#ax.spines['bottom'].set_position(('outward', 0))
ax.tick_params(axis='x', pad=0)
plt.tight_layout()
plt.savefig(r"C:\Users\Shami\OneDrive\Desktop\New folder\comp_W_M.png", dpi=350, bbox_inches='tight')
plt.show()
