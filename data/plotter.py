import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

#starts = [ 450, 865, 1270, 1680, 2090, 2515, 2930 ]
starts = [ 917, 1801, 2681, 3561, 4437 ]

def read(path):
	data = pd.read_csv(path)
	c4 = data["C4"]

	return c4

def plot(path):
	try:
		y = read(path)
		x = range(len(y))

		i = 0
		s = len(y)

		# for s in starts:
		fig, ax = plt.subplots(1, 1)
		ax.scatter(x[i:s], y[i:s], s = 3)
		plt.show()
		# i = s

	except:
		print("Failed to open:", path)

def dir(path):
	folder = Path(path)
	cwd = Path(Path.cwd())

	for file in folder.iterdir():
		if file.is_file() and file.suffix == ".csv":
			plot(file)

plot("data/plan/09_06_26_01.csv")
plot("data/plan/10_06_26_02.csv")
plot("data/plan/10_06_26_03.csv")
plot("data/plan/10_06_26_04.csv")
plot("data/plan/11_06_26_06.csv")
plot("data/plan/11_06_26_08.csv")
