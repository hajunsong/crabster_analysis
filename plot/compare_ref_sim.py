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
]


def read_log_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, header=None)
    if df.shape[1] < len(COLUMNS):
        raise ValueError(
            f"Unexpected column count in {path}: got {df.shape[1]}, expected at least {len(COLUMNS)}"
        )
    if df.shape[1] == len(COLUMNS):
        df.columns = COLUMNS
    else:
        extras = [f"extra_{i}" for i in range(1, df.shape[1] - len(COLUMNS) + 1)]
        df.columns = COLUMNS + extras
    return df


def _plot_single(
    ref: pd.DataFrame,
    sim: pd.DataFrame,
    col: str,
    title: str,
    ylabel: str,
    xlim,
):
    fig, ax = plt.subplots(figsize=(8, 4), constrained_layout=True)
    ax.plot(ref["time"], ref[col], label="Ref", linewidth=2.0)
    ax.plot(sim["time"], sim[col], label="Sim", linewidth=2.0, linestyle="--")
    ax.set_title(title)
    ax.set_xlabel("time [s]")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.35)
    ax.legend(loc="best")
    if xlim is not None:
        ax.set_xlim(*xlim)
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
    parser.add_argument("--show", action="store_true", help="Show interactive plots")
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

    if args.show:
        plt.rcParams["figure.max_open_warning"] = 0

    plots = [
        # Base
        ("base_rz", "Base position (z)", "position [m]"),
        ("base_vz", "Base velocity (z)", "velocity [m/s]"),
        ("base_accz", "Base acceleration (z)", "acceleration [m/s²]"),
        # Sub end-effector
        ("sub_re_x", "Sub end position (x)", "position [m]"),
        ("sub_re_y", "Sub end position (y)", "position [m]"),
        ("sub_re_z", "Sub end position (z)", "position [m]"),
        ("sub_re_roll", "Sub end orientation (roll)", "angle [rad]"),
        ("sub_re_pich", "Sub end orientation (pitch)", "angle [rad]"),
        ("sub_re_yaw", "Sub end orientation (yaw)", "angle [rad]"),
        # Joint q
        ("sub_q1", "sub_q1", "q [rad]"),
        ("sub_q2", "sub_q2", "q [rad]"),
        ("sub_q3", "sub_q3", "q [rad]"),
        ("sub_q4", "sub_q4", "q [rad]"),
        # Joint dq
        ("sub_dq1", "sub_dq1", "dq [rad/s]"),
        ("sub_dq2", "sub_dq2", "dq [rad/s]"),
        ("sub_dq3", "sub_dq3", "dq [rad/s]"),
        ("sub_dq4", "sub_dq4", "dq [rad/s]"),
        # Joint ddq
        ("sub_ddq1", "sub_ddq1", "ddq [rad/s²]"),
        ("sub_ddq2", "sub_ddq2", "ddq [rad/s²]"),
        ("sub_ddq3", "sub_ddq3", "ddq [rad/s²]"),
        ("sub_ddq4", "sub_ddq4", "ddq [rad/s²]"),
    ]

    for col, title, ylabel in plots:
        fig = _plot_single(ref, sim, col, title, ylabel, xlim)
        out_path = outdir / f"compare_{col}_{stamp}.png"
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

