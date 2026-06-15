import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

AM1 = 165
NORMAL = 1
RAW = 0

def read(path):
	data = pd.read_csv(path)
	am1 = data["AM1"]

	return am1

def plot(path):
	try:
		y = [i for i in range(10)]#read(path)
		x = range(len(y))


		fig, ax = plt.subplots(1, 1)
		ax.scatter(x, y)
		print("Plot:", path)
		plt.show()
		print("Plot End:", path)

	except:
		print("Failed to open:", path)

def dir(path):
	folder = Path(path)
	cwd = Path(Path.cwd())

	for file in folder.iterdir():
		if file.is_file() and file.suffix == ".csv":
			plot(file)

fig, ax = plt.subplots()
ax.plot(range(10), range(10))
plt.show()

