import csv
import matplotlib.pyplot as plt
from pathlib import Path

AM1 = 165
NORMAL = 1
RAW = 0

def convert(n, vec):
    try:
        i = float(n)
        vec.append(i)
    except:
        vec.clear()

def finite_difference(vec):
    diff = []

    for i in range(len(vec)):
        if i == 0:
            diff.append(vec[i + 2] - vec[i])
        elif i + 1 == len(vec):
            diff.append(vec[i] - vec[i - 2])
        else:
            diff.append(vec[i + 1] - vec[i - 1])

    return diff

def read(path, col):
    vec = []

    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter=",")

        for row in reader:
            if len(row) < col + 1:
                vec.clear()
                continue

            convert(row[col], vec)

    return (vec, finite_difference(vec))

def plot(path, col):
    try:
        (y, diff) = read(path, col)
        x = range(len(y))

        print("Plot:", path)

        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.scatter(x, y)
        ax2.scatter(x, diff)
        plt.show()

    except:
        print("Failed to open:", path)

def dir(path, col):
    folder = Path(path)
    cwd = Path(Path.cwd())

    for file in folder.iterdir():
        if file.is_file() and file.suffix == ".csv":
            plot(file, col)

dir("plan", AM1)
