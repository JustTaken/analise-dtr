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

	def make_fig(self, data):
		fig = plt.figure()

		rows = int(np.ceil(len(data.output) / self.cols))

		for i in range(0, len(data.output)):
			y = data.output[i]
			x = np.arange(0, len(y))
			y_hat = data.fit[i]

			ax = fig.add_subplot(rows, self.cols, i + 1)
			ax.scatter(x, y, color='red', s = 3)
			ax.scatter(x, y_hat, color='blue', s = 3)

			tm = data.tm[i]
			n = data.n[i]

			ax.legend(["Experimental", f"n = {n}, tm = {tm}"])
		return fig
		
	def plot(self, data):
		fig = self.make_fig(data)
		plt.show()

	def save_fig(self, data, path):
		fig = self.make_fig(data)
		fig.savefig(path)

	def save_data(self, data, path):
		data_frame = pd.DataFrame({
			'n': data.n,
			'tm': data.tm,
			'var': data.tm,
		})

		data_frame.to_csv(path, index=False)
	
	def plot_raw(self, path, col_name):
		print("plotando", path)
		data = pd.read_csv(path, index_col=False)
		y = converter.convert(data[col_name].values)
		x = range(0, len(y))
		fig = plt.figure()

		ax = fig.add_subplot(1, 1, 1)
		ax.scatter(x, y, color='red', s = 3)

		plt.show()
		
	def save(self, path_csv, path_plot, data):
		self.save_fig(data, path_plot)
		self.save_data(data, path_csv)

class Data:
	def __init__(self, path, col_name, init_v, converter):
		print(path)
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
		y_full = self.y[start:end]
		length = len(y_full)
		y_full = y_full - np.mean(y_full[length - int(length * 0.01):length - 1])
		x_full = range(0, length)

		y = y_full[0:int(length*0.5)]
		length = len(y)
		x = range(0, length)

		fit = regression.CustomCurve(x, y)
		self.output.append(y_full)

		tm, var, n = fit.values()

		self.tm.append(rd(tm))
		self.var.append(rd(var))
		self.n.append(rd(n))
		self.fit.append(fit.fit(x_full))

converter = Converter(1.5, 0.5)
render = Render(2)

render.save("data/plan_plate/01.csv", "data/plan_plate/01.png", Data("data/plan_plate/09_06_26_01.csv", "AM1", [ 933, 1815, 2693, 3571, 4448, 5323 ], converter))
render.save("data/plan_plate/02.csv", "data/plan_plate/02.png", Data("data/plan_plate/10_06_26_02.csv", "AM1", [ 878, 1754, 2631, 3523, 4384, 5300 ], converter))
render.save("data/plan_plate/03.csv", "data/plan_plate/03.png", Data("data/plan_plate/10_06_26_03.csv", "AM1", [ 407, 1302, 2172, 3050, 3936, 4806, 5676 ], converter))
render.save("data/plan_plate/04.csv", "data/plan_plate/04.png", Data("data/plan_plate/10_06_26_04.csv", "AM1", [ 1152, 2025, 2903, 3793, 4669, 5432 ], converter))
render.save("data/plan_plate/06.csv", "data/plan_plate/06.png", Data("data/plan_plate/11_06_26_06.csv", "AM1", [ 917, 1791, 2668, 3549, 4431, 5290 ], converter))
render.save("data/plan_plate/08.csv", "data/plan_plate/08.png", Data("data/plan_plate/11_06_26_08.csv", "AM1", [ 941, 1818, 2710, 3578, 4463, 5347 ], converter))
render.save("data/plan_plate/10.csv", "data/plan_plate/10.png", Data("data/plan_plate/30_03_26_10.csv", "AM1", [ 43, 461, 871, 1285, 1705, 2115], converter))
render.save("data/plan_plate/13.csv", "data/plan_plate/13.png", Data("data/plan_plate/30_03_26_13.csv", "AM1", [ 383, 800, 1215, 1632, 2052, 2471, 2880 ], converter))
render.save("data/plan_plate/14.csv", "data/plan_plate/14.png", Data("data/plan_plate/02_04_26_14.csv", "AM1", [ 347, 763, 1179, 1595, 2018, 2433, 2844, 3255 ], converter))

render.save("data/plan_down/01.csv", "data/plan_down/01.png", Data("data/plan_down/14_06_26_01.csv", "AM1", [ 937, 1823, 2701, 3578, 4456, 5330 ], converter))
render.save("data/plan_down/02.csv", "data/plan_down/02.png", Data("data/plan_down/14_06_26_02.csv", "AM1", [ 931, 1810, 2692, 3570, 4442, 5320 ], converter))
render.save("data/plan_down/03.csv", "data/plan_down/03.png", Data("data/plan_down/14_06_26_03.csv", "AM1", [ 942, 1824, 2714, 3588, 4474, 5344 ], converter))
render.save("data/plan_down/04.csv", "data/plan_down/04.png", Data("data/plan_down/14_06_26_04.csv", "AM1", [ 957, 1839, 2717, 3594, 4468, 5350 ], converter))
render.save("data/plan_down/06.csv", "data/plan_down/06.png", Data("data/plan_down/14_06_26_06.csv", "AM1", [ 902, 1776, 2658, 3535, 4417, 5286 ], converter))
render.save("data/plan_down/08.csv", "data/plan_down/08.png", Data("data/plan_down/14_06_26_08.csv", "AM1", [ 996, 1880, 2753, 3625, 4505, 5389 ], converter))
render.save("data/plan_down/05.csv", "data/plan_down/05.png", Data("data/plan_down/19_06_26_05.csv", "AM1", [ 878, 1768, 2646, 3520, 4394, 5276 ], converter))
render.save("data/plan_down/10.csv", "data/plan_down/10.png", Data("data/plan_down/19_06_26_10.csv", "AM1", [ 921, 1795, 2676, 3566, 4447, 5320], converter))
render.save("data/plan_down/13.csv", "data/plan_down/13.png", Data("data/plan_down/19_06_26_13.csv", "AM1", [ 895, 1774, 2650, 3533, 4412, 5288 ], converter))
render.save("data/plan_down/14.csv", "data/plan_down/14.png", Data("data/plan_down/19_06_26_14.csv", "AM1", [ 928, 1802, 2687, 3564, 4441, 5310 ], converter))

render.save("data/plan_up/01.csv", "data/plan_up/01.png", Data("data/plan_up/20_06_26_01.csv", "AM1", [ 1120, 2000, 2875, 3756, 4632, 5512, 6390 ], converter))
render.save("data/plan_up/02.csv", "data/plan_up/02.png", Data("data/plan_up/20_06_26_02.csv", "AM1", [ 890, 1769, 2636, 3531, 4402, 5277 ], converter))
render.save("data/plan_up/03.csv", "data/plan_up/03.png", Data("data/plan_up/20_06_26_03.csv", "AM1", [ 895, 1771, 2643, 3519, 4403, 5283 ], converter))
render.save("data/plan_up/04.csv", "data/plan_up/04.png", Data("data/plan_up/20_06_26_04.csv", "AM1", [ 866, 1749, 2631, 3498, 4380, 5263 ], converter))
render.save("data/plan_up/06.csv", "data/plan_up/06.png", Data("data/plan_up/20_06_26_06.csv", "AM1", [ 885, 1763, 2641, 3519, 4401, 5267 ], converter))
render.save("data/plan_up/08.csv", "data/plan_up/08.png", Data("data/plan_up/21_06_26_08.csv", "AM1", [ 944, 1829, 2702, 3587, 4468, 5345 ], converter))
render.save("data/plan_up/10.csv", "data/plan_up/10.png", Data("data/plan_up/21_06_26_10.csv", "AM1", [ 938, 1816, 2694, 3572, 4451, 5329 ], converter))
render.save("data/plan_up/13.csv", "data/plan_up/13.png", Data("data/plan_up/21_06_26_13.csv", "AM1", [ 881, 1755, 2637, 3519, 4392, 5282 ], converter))
render.save("data/plan_up/14.csv", "data/plan_up/14.png", Data("data/plan_up/21_06_26_14.csv", "AM1", [ 887, 1771, 2647, 3527, 4406, 5290 ], converter))


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


#n = 1.5
#t = 100
#a = 1000
#data = pd.DataFrame({
#	"AM1": [a * (x / t) ** (n - 1) * n ** n * np.exp(-(x * n) / t) for x in range(0, 1000)]
#})

#data.to_csv("testing.csv")

