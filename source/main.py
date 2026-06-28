import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import regression

class Converter:
	def __init__(self, a, b):
		self.a = a
		self.b = b

	def convert(self, data):
		return self.a * data + self.b

def rd(x):
	return round(x, 2)

class Render:
	def __init__(self, cols):
		self.cols = cols

	def plot(self, data):
		fig = plt.figure()

		rows = int(np.ceil(len(data.output) / self.cols))

		for i in range(0, len(data.output)):
			y = data.output[i]
			x = np.arange(0, len(y))
			y_hat = data.fit[i]

			ax = fig.add_subplot(rows, self.cols, i + 1)
			ax.scatter(x, y, color='red')
			ax.scatter(x, y_hat, color='blue')

			tm = data.tm[i]
			n = data.n[i]

			ax.legend(["Experimental", f"n = {n}, tm = {tm}"])

		plt.show()

class Data:
	def __init__(self, path, col_name, init_v, converter):
		data = pd.read_csv(path, index_col=False)

		y = converter.convert(data[col_name].values)
		self.y = y

		self.tm = []
		self.var = []
		self.n = []
		self.fit = []
		self.output = []

		for i in range(0, len(init_v) - 1):
			self.add_range(init_v[i], init_v[i + 1])

	def add_range(self, start, end):
		y = self.y[start:end]
		length = len(y)
		y = y - np.mean(y[length - int(length * 0.01):length - 1])

		#y = y[0:int(len(y)*0.2)]
		#length = len(y)
		x = range(0, length)

		fit = regression.CustomCurve(x, y)
		self.output.append(y)

		tm, var, n = fit.values()

		self.tm.append(rd(tm))
		self.var.append(rd(var))
		self.n.append(rd(n))
		self.fit.append(fit.fit(x))


#n = 1.5
#t = 100
#a = 1000
#data = pd.DataFrame({
#	"AM1": [a * (x / t) ** (n - 1) * n ** n * np.exp(-(x * n) / t) for x in range(0, 1000)]
#})

#data.to_csv("testing.csv")

converter = Converter(1.5, 0.5)
render = Render(2)
#render.plot(Data("testing.csv", "AM1", [ 0, 1000 ], converter))
render.plot(Data("data/plan/09_06_26_01.csv", "AM1", [ 933, 1815, 2693, 3571, 4448, 5323 ], converter))

#########################################################################################################

#def add_to_figure(self, y, fig, rows, cols, idx):
#	x = range(len(y))
#	l = len(y)
# print(f"{idx} := A({rd(a)}), B({rd(b)}), C({rd(c)}), tm({rd(tm)}), var({rd(var)}), n({rd(n)}), resto({rd(r)})")

# ax = fig.add_subplot(rows, cols, idx + 1)
# ax.scatter(x, y, color='orange', s=3)
# ax.scatter(x, fit, color='red', s=3)

#def get_multiple_data(path, s):
#	fig = plt.figure()
#	y = load_data(path)
#
#	ys = []
#	for i in range(len(s) - 1):
#		ys.append(y[s[i]:s[i + 1]])
#
#	cols = 2
#	rows = int(np.ceil(len(ys) / cols))
#
#	i = 1
#	for y in ys:
#		try:
#			add_data_to_figure(y, fig, rows, cols, i, data)
#			i += 1
#		except Exception as e:
#			continue
#
#	if i == 1:
#		return Exception("Missing data")
#
#	return fig, data

#def save_multiple_data(path, s):
#	fig, data = get_multiple_data(path, s)
#	name, extension = os.path.splitext(path)
#	fig.savefig(name + ".png")
#	df = pd.DataFrame(data)
#	df.to_csv(name + "data.csv", index=False)

#def plot_multiple_data(path, s):
#	get_multiple_data(path, s)
#	plt.show()

# plot_multiple_data("data/plan/28_03_26_02.csv", [ 0, 450, 865, 1270, 1680, 2090, 2515, 2930 ])
#save_multiple_data("data/plan/09_06_26_01.csv", [ 917, 1801, 2681, 3561, 4437, 5323 ])
#save_multiple_data("data/plan/10_06_26_02.csv", [ 878, 1754, 2631, 3523, 4384, 5300 ])
#save_multiple_data("data/plan/10_06_26_03.csv", [ 407, 1302, 2172, 3050, 3936, 4806, 5676 ])
#save_multiple_data("data/plan/10_06_26_04.csv", [ 1093, 1995, 2898, 3793, 4629, 5432 ])
#save_multiple_data("data/plan/11_06_26_06.csv", [ 886, 1770, 2638, 3538, 4398, 5290 ])
#save_multiple_data("data/plan/11_06_26_08.csv", [ 941, 1818, 2710, 3578, 4455, 5347 ])

