import argparse
from datetime import datetime
from pathlib import Path

# Backend must be set before importing pyplot
_parser = argparse.ArgumentParser()
_parser.add_argument("--show", action="store_true", help="Show interactive plots")
_args_early, _ = _parser.parse_known_args()

import matplotlib
if _args_early.show:
    # GUI 백엔드 명시 (Agg는 show 불가)
    matplotlib.use("TkAgg", force=True)
else:
    matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
import pandas as pd


COLUMNS = [
    "index",
    "time",
    "base_rx",
    "base_ry",
    "base_rz",
    "base_roll",
    "base_pich",
    "base_yaw",
    "base_vx",
    "base_vy",
    "base_vz",
    "base_wx",
    "base_wy",
    "base_wz",
    "base_accx",
    "base_accy",
    "base_accz",
    "base_ax",
    "base_ay",
    "base_az",
    "sub_re_x",
    "sub_re_y",
    "sub_re_z",
    "sub_re_roll",
    "sub_re_pich",
    "sub_re_yaw",
    "sub_q1",
    "sub_q2",
    "sub_q3",
    "sub_q4",
    "sub_dq1",
    "sub_dq2",
    "sub_dq3",
    "sub_dq4",
    "sub_ddq1",
    "sub_ddq2",
    "sub_ddq3",
    "sub_ddq4",
    "sub_rsda1",
    "sub_rsda2",
    "sub_rsda3",
    "sub_rsda4",
]


def read_log_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, header=None)
    min_cols = 38  # index, time, base, sub (through sub_ddq4)
    if df.shape[1] < min_cols:
        raise ValueError(
            f"Unexpected column count in {path}: got {df.shape[1]}, expected at least {min_cols}"
        )
    # Assign column names from COLUMNS; extras if CSV has more columns than COLUMNS
    n = df.shape[1]
    if n <= len(COLUMNS):
        df.columns = COLUMNS[:n]
    else:
        extras = [f"extra_{i}" for i in range(1, n - len(COLUMNS) + 1)]
        df.columns = COLUMNS + extras
    return df


def _plot_subplots(
    ref: pd.DataFrame,
    sim: pd.DataFrame,
    plots: list[tuple[str, str, str]],
    xlim,
    ncols: int = 3,
) -> plt.Figure:
    n = len(plots)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(6 * ncols, 4 * nrows), constrained_layout=True)
    axes_flat = axes.flatten() if n > 1 else [axes]
    for ax, (col, title, ylabel) in zip(axes_flat, plots):
        ax.plot(ref["time"], ref[col], label="Ref", linewidth=2.0)
        ax.plot(sim["time"], sim[col], label="Sim", linewidth=2.0, linestyle="--")
        ax.set_title(title)
        ax.set_xlabel("time [s]")
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.35)
        ax.legend(loc="best")
        if xlim is not None:
            ax.set_xlim(*xlim)
    for ax in axes_flat[len(plots) :]:
        ax.set_visible(False)
    return fig


def main():
    repo_root = Path(__file__).resolve().parent.parent
    default_ref = repo_root / "data" / "ref_data_contact_rsda.csv"
    default_sim = repo_root / "data" / "sim_data.csv"
    default_out = repo_root / "figure"

    parser = argparse.ArgumentParser(
        description="Compare ref_data_contact_rsda.csv vs sim_data.csv (overlay plots)."
    )
    parser.add_argument("--ref", default=str(default_ref), help="Reference CSV path")
    parser.add_argument("--sim", default=str(default_sim), help="Simulation CSV path")
    parser.add_argument("--outdir", default=str(default_out), help="Output directory")
    parser.add_argument(
        "--tmin", type=float, default=None, help="Plot start time (seconds)"
    )
    parser.add_argument("--tmax", type=float, default=None, help="Plot end time (seconds)")
    parser.add_argument("--show", action="store_true", help="Show interactive plots (save as name.png, overwrite)")
    parser.add_argument("--save", action="store_true", help="Save with timestamp in filename (name_YYYYMMDD_HHMMSS.png)")
    args = parser.parse_args()

    ref = read_log_csv(args.ref)
    sim = read_log_csv(args.sim)

    xlim = None
    if args.tmin is not None or args.tmax is not None:
        tmin = ref["time"].min() if args.tmin is None else args.tmin
        tmax = ref["time"].max() if args.tmax is None else args.tmax
        xlim = (tmin, tmax)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    use_timestamp = args.save  # --save: timestamp in filename; --show only: overwrite with name.png

    if args.show:
        plt.rcParams["figure.max_open_warning"] = 0

    # Figure 1: Base x,y,z position, velocity, acceleration (3x3)
    base_plots = [
        ("base_rx", "Base position (x)", "position [m]"),
        ("base_ry", "Base position (y)", "position [m]"),
        ("base_rz", "Base position (z)", "position [m]"),
        ("base_vx", "Base velocity (x)", "velocity [m/s]"),
        ("base_vy", "Base velocity (y)", "velocity [m/s]"),
        ("base_vz", "Base velocity (z)", "velocity [m/s]"),
        ("base_accx", "Base acceleration (x)", "acceleration [m/s²]"),
        ("base_accy", "Base acceleration (y)", "acceleration [m/s²]"),
        ("base_accz", "Base acceleration (z)", "acceleration [m/s²]"),
    ]

    # Base orientation: roll/pitch/yaw, angular vel, angular acc (3x3)
    base_orientation_plots = [
        ("base_roll", "Base orientation (roll)", "angle [rad]"),
        ("base_pich", "Base orientation (pitch)", "angle [rad]"),
        ("base_yaw", "Base orientation (yaw)", "angle [rad]"),
        ("base_wx", "Base angular velocity (wx)", "rad/s"),
        ("base_wy", "Base angular velocity (wy)", "rad/s"),
        ("base_wz", "Base angular velocity (wz)", "rad/s"),
        ("base_ax", "Base angular acceleration (ax)", "rad/s²"),
        ("base_ay", "Base angular acceleration (ay)", "rad/s²"),
        ("base_az", "Base angular acceleration (az)", "rad/s²"),
    ]

    # Sub end position + orientation (2x3)
    sub_end_plots = [
        ("sub_re_x", "Sub end position (x)", "position [m]"),
        ("sub_re_y", "Sub end position (y)", "position [m]"),
        ("sub_re_z", "Sub end position (z)", "position [m]"),
        ("sub_re_roll", "Sub end orientation (roll)", "angle [rad]"),
        ("sub_re_pich", "Sub end orientation (pitch)", "angle [rad]"),
        ("sub_re_yaw", "Sub end orientation (yaw)", "angle [rad]"),
    ]

    # RSDA force (body 0~3) 2x2
    rsda_plots = [
        ("sub_rsda1", "RSDA body0 (Ti)", "torque [Nm]"),
        ("sub_rsda2", "RSDA body1 (Ti)", "torque [Nm]"),
        ("sub_rsda3", "RSDA body2 (Ti)", "torque [Nm]"),
        ("sub_rsda4", "RSDA body3 (Ti)", "torque [Nm]"),
    ]

    # Figure 4: Joint 3x4 - sub_q1, sub_q2, sub_q3, sub_q4 순서로
    joint_plots = [
        ("sub_q1", "sub_q1", "q [rad]"),
        ("sub_q2", "sub_q2", "q [rad]"),
        ("sub_q3", "sub_q3", "q [rad]"),
        ("sub_q4", "sub_q4", "q [rad]"),
        ("sub_dq1", "sub_dq1", "dq [rad/s]"),
        ("sub_dq2", "sub_dq2", "dq [rad/s]"),
        ("sub_dq3", "sub_dq3", "dq [rad/s]"),
        ("sub_dq4", "sub_dq4", "dq [rad/s]"),
        ("sub_ddq1", "sub_ddq1", "ddq [rad/s²]"),
        ("sub_ddq2", "sub_ddq2", "ddq [rad/s²]"),
        ("sub_ddq3", "sub_ddq3", "ddq [rad/s²]"),
        ("sub_ddq4", "sub_ddq4", "ddq [rad/s²]"),
    ]

    figure_groups = [
        ("sub1_base_result", base_plots, 3),
        ("sub1_base_orientation", base_orientation_plots, 3),
        ("sub1_sub_end_result", sub_end_plots, 3),
        ("sub1_joint_result", joint_plots, 4),
    ]
    # RSDA figure: only if both ref and sim have RSDA columns
    if "sub_rsda1" in ref.columns and "sub_rsda1" in sim.columns:
        figure_groups.append(("sub1_rsda_result", rsda_plots, 2))

    for name, plots, ncols in figure_groups:
        fig = _plot_subplots(ref, sim, plots, xlim, ncols=ncols)
        filename = f"{name}_{stamp}.png" if use_timestamp else f"{name}.png"
        out_path = outdir / filename
        fig.savefig(out_path, dpi=300)
        if not args.show:
            plt.close(fig)
        print(f"Saved: {out_path}")

    if args.show:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main()

