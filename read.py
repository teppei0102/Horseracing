import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import readchar
import signal
import sys

def handler(signal, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, handler)

def plot():
    data = joblib.load("data.dat")


    x = data[data["着順"] == "1"]["単勝"].values.astype(np.float)
    print("Total Data:"+(str)(len(x)))

    # sns.distplot(x,axlabel="Odds",norm_hist=False,bins=200)

    xf = x[(x >= 0) & (x < 10)]
    sns.distplot(xf,axlabel="Odds",norm_hist=False,bins=200)
    plt.show()
    plt.cla()

plot()
