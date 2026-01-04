import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compare_csv(rec_csv="rec_data.csv", sim_csv="sim_data.csv",
                cols_to_plot=None, max_rows=None):
    # read both as raw numeric logs
    rec = pd.read_csv(rec_csv, header=None)
    sim = pd.read_csv(sim_csv, header=None)

    if max_rows is not None:
        rec = rec.iloc[:max_rows]
        sim = sim.iloc[:max_rows]

    # time is assumed to be col=1 (step=0, time=1)
    t_rec = rec.iloc[:, 1].to_numpy()
    t_sim = sim.iloc[:, 1].to_numpy()

    if cols_to_plot is None:
        # default: plot first few signals after time
        # (col2~ are Y states in sim_data)
        cols_to_plot = [2, 3, 4, 5, 6]  # example

    for c in cols_to_plot:
        if c >= rec.shape[1] or c >= sim.shape[1]:
            print(f"[SKIP] col {c}: out of range (rec={rec.shape[1]}, sim={sim.shape[1]})")
            continue

        y_rec = rec.iloc[:, c].to_numpy()
        y_sim = sim.iloc[:, c].to_numpy()

        plt.figure()
        plt.plot(t_rec, y_rec, label=f"rec col{c}")
        plt.plot(t_sim, y_sim, label=f"sim col{c}", linestyle="--")
        plt.xlabel("time [s]")
        plt.ylabel(f"signal col{c}")
        plt.title(f"Compare column {c}")
        plt.grid(True)
        plt.legend()

    plt.show()


if __name__ == "__main__":
    compare_csv("rec_data.csv", "sim_data.csv",
                cols_to_plot=[2,3,4,5,6,7,8,9],  # 원하는 컬럼 번호로 바꿔도 됨
                max_rows=2000)
