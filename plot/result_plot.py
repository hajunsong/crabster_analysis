import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from pathlib import Path
from datetime import datetime

def compare_csv(rec_csv="rec_data.csv", sim_csv="rec_data_fix_free_fall.csv"):
    # read both as raw numeric logs
    rec = pd.read_csv(rec_csv, header=None)
    sim = pd.read_csv(sim_csv, header=None)

    t_rec = rec.iloc[:, 1].to_numpy()
    t_sim = sim.iloc[:, 1].to_numpy()

    txt_title = ["FL", "ML", "RL", "FR", "MR", "RR"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for j in range(0, 1):
        fig_cart, axes_cart = plt.subplots(2, 3, figsize=(10, 6), constrained_layout=True)
        sub_title = ["x", "y", "z"]
        for i in range(0, 3):
            y_rec = rec.iloc[:, i + 2 + j * 18].to_numpy()
            y_sim = sim.iloc[:, i + 2 + j * 18].to_numpy()

            axes_cart[0][i].plot(t_rec, y_rec, label=f"Ref", linewidth=2.0)
            axes_cart[0][i].plot(t_sim, y_sim, label=f"Analysis", linewidth=2.0, linestyle="--")
            axes_cart[0][i].set_xlabel("time [s]")
            axes_cart[0][i].set_ylabel("Displacement [mm]")
            axes_cart[0][i].set_title(f"{txt_title[j]} {sub_title[i]} Position")
            axes_cart[0][i].grid()
            axes_cart[0][i].set_xlim(0,2)
            axes_cart[0][i].ticklabel_format(useOffset=False, axis='y')
            axes_cart[0][i].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

            if i == 3:
                axes_cart[0][i].legend()

        sub_title = ["roll", "pitch", "yaw"]
        for i in range(0, 3):
            y_rec = rec.iloc[:, i + 2 + 3 + j * 18].to_numpy()
            y_sim = sim.iloc[:, i + 2 + 3 + j * 18].to_numpy()

            axes_cart[1][i].plot(t_rec, y_rec, label=f"Ref", linewidth=2.0)
            axes_cart[1][i].plot(t_sim, y_sim, label=f"Analysis", linewidth=2.0, linestyle="--")
            axes_cart[1][i].set_xlabel("time [s]")
            axes_cart[1][i].set_ylabel("Displacement [rad]")
            axes_cart[1][i].set_title(f"{txt_title[j]} {sub_title[i]} Orientation")
            axes_cart[1][i].grid()
            axes_cart[1][i].set_xlim(0,2)
            axes_cart[1][i].ticklabel_format(useOffset=False, style='plain')
            axes_cart[1][i].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

        fig_cart_name = f"figure/sub{j+1}_cart_result.png"#_{timestamp}.png"
        fig_cart.savefig(fig_cart_name, dpi=300)
        print(f"Saved: {fig_cart_name}")

        fig_joint, axes_joint = plt.subplots(3, 4, figsize=(10, 6), constrained_layout=True)
        for i in range(0, 4):
            y_rec = rec.iloc[:, i + 2 + 6 + j * 18].to_numpy()
            y_sim = sim.iloc[:, i + 2 + 6 + j * 18].to_numpy()

            axes_joint[0][i].plot(t_rec, y_rec, label=f"Ref", linewidth=2.0)
            axes_joint[0][i].plot(t_sim, y_sim, label=f"Analysis", linewidth=2.0, linestyle="--")
            axes_joint[0][i].set_xlabel("time [s]")
            axes_joint[0][i].set_ylabel(f"Displacement [rad]")
            axes_joint[0][i].set_title(f"{txt_title[j]} q_{i + 1}")
            axes_joint[0][i].grid()
            axes_joint[0][i].set_xlim(0,2)
            axes_joint[0][i].ticklabel_format(useOffset=False, style='plain')
            axes_joint[0][i].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

            if i == 3:
                axes_joint[0][i].legend()

        for i in range(0, 4):
            y_rec = rec.iloc[:, i + 2 + 10 + j * 18].to_numpy()
            y_sim = sim.iloc[:, i + 2 + 10 + j * 18].to_numpy()

            axes_joint[1][i].plot(t_rec, y_rec, label=f"Ref", linewidth=2.0)
            axes_joint[1][i].plot(t_sim, y_sim, label=f"Analysis", linewidth=2.0, linestyle="--")
            axes_joint[1][i].set_xlabel("time [s]")
            axes_joint[1][i].set_ylabel(f"Velocity [rad/s]")
            axes_joint[1][i].set_title(f"{txt_title[j]} dq_{i + 1}")
            axes_joint[1][i].grid()
            axes_joint[1][i].set_xlim(0,2)
            axes_joint[1][i].ticklabel_format(useOffset=False, style='plain')
            axes_joint[1][i].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

        for i in range(0, 4):
            y_rec = rec.iloc[:, i + 2 + 14 + j * 18].to_numpy()
            y_sim = sim.iloc[:, i + 2 + 14 + j * 18].to_numpy()

            axes_joint[2][i].plot(t_rec, y_rec, label=f"Ref", linewidth=2.0)
            axes_joint[2][i].plot(t_sim, y_sim, label=f"Analysis", linewidth=2.0, linestyle="--")
            axes_joint[2][i].set_xlabel("time [s]")
            axes_joint[2][i].set_ylabel(f"Acceleration [rad/s^2]")
            axes_joint[2][i].set_title(f"{txt_title[j]} ddq_{i + 1}")
            axes_joint[2][i].grid()
            axes_joint[2][i].set_xlim(0,2)
            axes_joint[2][i].ticklabel_format(useOffset=False, style='plain')
            axes_joint[2][i].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

        fig_joint_name = f"figure/sub{j+1}_joint_result.png"#_{timestamp}.png"
        fig_joint.savefig(fig_joint_name, dpi=300)
        print(f"Saved: {fig_joint_name}")

    # plt.show()

if __name__ == "__main__":
    current_file_path = Path(__file__).resolve().parent.parent
    compare_csv(str(current_file_path) + "/data/ref_data_fix_free_fall.csv", 
                str(current_file_path) + "/data/sim_data.csv")
