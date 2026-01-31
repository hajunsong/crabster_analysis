import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def compare_csv(rec_csv="rec_data.csv", sim_csv="rec_data_fix_free_fall.csv"):
    # read both as raw numeric logs
    rec = pd.read_csv(rec_csv, header=None)
    sim = pd.read_csv(sim_csv, header=None)

    t_rec = rec.iloc[:, 1].to_numpy()
    t_sim = sim.iloc[:, 1].to_numpy()

    txt_title = ["FL", "ML", "RL", "FR", "MR", "RR"]

    for j in range(0, 1):
        fig2, axes2 = plt.subplots(2, 3, figsize=(10, 6), constrained_layout=True)
        sub_title = ["x", "y", "z"]
        for i in range(0, 3):
            y_rec = rec.iloc[:, i + 2 + j * 18].to_numpy()
            y_sim = sim.iloc[:, i + 2 + j * 18].to_numpy()

            axes2[0][i].plot(t_rec, y_rec, label=f"Ref", linewidth=2.0)
            axes2[0][i].plot(t_sim, y_sim, label=f"Analysis", linewidth=2.0, linestyle="--")
            axes2[0][i].set_xlabel("time [s]")
            axes2[0][i].set_ylabel("Displacement [mm]")
            axes2[0][i].set_title(f"{txt_title[j]} {sub_title[i]} Position")
            axes2[0][i].grid()
            axes[1][i].set_xlim(0,2)

            if i == 3:
                axes2[0][i].legend()

        sub_title = ["roll", "pitch", "yaw"]
        for i in range(0, 3):
            y_rec = rec.iloc[:, i + 2 + 3 + j * 18].to_numpy()
            y_sim = sim.iloc[:, i + 2 + 3 + j * 18].to_numpy()

            axes2[1][i].plot(t_rec, y_rec, label=f"Ref", linewidth=2.0)
            axes2[1][i].plot(t_sim, y_sim, label=f"Analysis", linewidth=2.0, linestyle="--")
            axes2[1][i].set_xlabel("time [s]")
            axes2[1][i].set_ylabel("Displacement [rad]")
            axes2[1][i].set_title(f"{txt_title[j]} {sub_title[i]} Orientation")
            axes2[1][i].grid()
            axes[1][i].set_xlim(0,2)

        fig, axes = plt.subplots(3, 4, figsize=(10, 6), constrained_layout=True)
        for i in range(0, 4):
            y_rec = rec.iloc[:, i + 2 + 6 + j * 18].to_numpy()
            y_sim = sim.iloc[:, i + 2 + 6 + j * 18].to_numpy()

            axes[0][i].plot(t_rec, y_rec, label=f"Ref", linewidth=2.0)
            axes[0][i].plot(t_sim, y_sim, label=f"Analysis", linewidth=2.0, linestyle="--")
            axes[0][i].set_xlabel("time [s]")
            axes[0][i].set_ylabel(f"Displacement [rad]")
            axes[0][i].set_title(f"{txt_title[j]} q_{i + 1}")
            axes[0][i].grid()
            axes[1][i].set_xlim(0,2)

            if i == 3:
                axes[0][i].legend()

        for i in range(0, 4):
            y_rec = rec.iloc[:, i + 2 + 10 + j * 18].to_numpy()
            y_sim = sim.iloc[:, i + 2 + 10 + j * 18].to_numpy()

            axes[1][i].plot(t_rec, y_rec, label=f"Ref", linewidth=2.0)
            axes[1][i].plot(t_sim, y_sim, label=f"Analysis", linewidth=2.0, linestyle="--")
            axes[1][i].set_xlabel("time [s]")
            axes[1][i].set_ylabel(f"Velocity [rad/s]")
            axes[1][i].set_title(f"{txt_title[j]} dq_{i + 1}")
            axes[1][i].grid()
            axes[1][i].set_xlim(0,2)

        for i in range(0, 4):
            y_rec = rec.iloc[:, i + 2 + 14 + j * 18].to_numpy()
            y_sim = sim.iloc[:, i + 2 + 14 + j * 18].to_numpy()

            axes[2][i].plot(t_rec, y_rec, label=f"Ref", linewidth=2.0)
            axes[2][i].plot(t_sim, y_sim, label=f"Analysis", linewidth=2.0, linestyle="--")
            axes[2][i].set_xlabel("time [s]")
            axes[2][i].set_ylabel(f"Acceleration [rad/s^2]")
            axes[2][i].set_title(f"{txt_title[j]} ddq_{i + 1}")
            axes[2][i].grid()
            axes[1][i].set_xlim(0,2)

    plt.show()


if __name__ == "__main__":
    current_file_path = Path(__file__).resolve().parent
    compare_csv(str(current_file_path) + "/../data/ref_data_fix_free_fall.csv", 
                str(current_file_path) + "/../data/sim_data.csv")
