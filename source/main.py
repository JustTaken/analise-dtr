import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import regression
import scipy as sp

class Converter:
	def __init__(self, a, b):
		self.a = a
		self.b = b

	def convert(self, data):
		C = self.a * data + self.b
		return C

def rd(x):
	return round(x, 2)

def calculate_E(y, t):
	A = sp.integrate.trapezoid(y, t)
	E = y / A
	return E

def calculate_tau(E, t):
	tau = sp.integrate.trapezoid(t * E, t)
	return tau

def calculate_theta(t, tau):
	return t / tau

def calculate_Etheta(E, tau):
	return tau * E

def calculate_var(E, t, tau):
	t = np.array(t)
	return sp.integrate.trapezoid(t**2 * E) - tau**2

def calculate_n(tau, var):
	return tau**2 / var

def remove_trail(y):
	length = len(y)
	return y - np.mean(y[length - int(length * 0.01):length - 1])

def transform_curve(y):
	C = remove_tail(y)
	t = range(0, length)

	E = calculate_E(C, t)
	tau = calculate_tau(E, t)
	theta = calculate_theta(t, tau)
	Etheta = calculate_Etheta(E, tau)

	#theta = t / tau
	#Etheta = tau * E

	return t, theta, Etheta

plt.rcParams.update({
	"text.usetex": True,
	"font.family": "serif",
	"font.size": 26,
	"axes.labelsize": 26,
	"legend.fontsize": 20,
	"xtick.labelsize": 14,
	"ytick.labelsize": 14,
})

class Render:
	def __init__(self, cols):
		self.cols = cols

	def make_fig(self, data):
		dpi = 100
		fig = plt.figure(figsize=(12, 8), dpi=dpi, constrained_layout=True)

		rows = int(np.ceil(len(data.output) / self.cols))

		for i in range(0, len(data.output)):
			y = data.output[i]
			theta = data.theta[i]
			y_hat = data.fit[i]

			tm = data.tm[i]
			n = data.n[i]

			ax = fig.add_subplot(rows, self.cols, i + 1)
			ax.scatter(theta, y, color='red', s = 3, label="Experimental")
			ax.scatter(theta, y_hat, color='blue', s = 3, label=f"N = {n}, tm = {tm}")

			ax.set_xlabel(r"$\theta$")
			ax.set_ylabel(r"$E(\theta)$")

			ax.legend()

		return fig

	def plot(self, data):
		fig = self.make_fig(data)
		plt.show()
		plt.close(fig)

	def save_fig(self, data, path):
		fig = self.make_fig(data)
		fig.savefig(path)
		plt.close(fig)

	def save_data(self, data, path):
		data_frame = pd.DataFrame({
			'n': data.n,
			'tm': data.tm,
			'var': data.tm,
		})

		data_frame.to_csv(path, index=False)

	def save_raw(self, path, out_path, col_name, start, end, converter):
		data = pd.read_csv(path, index_col=False)
		x, theta, y = transform_curve(converter.convert(data[col_name].values)[start:end])

		dpi = 200
		fig = plt.figure(figsize=(12, 8), dpi=dpi, constrained_layout=True)

		ax = fig.add_subplot(1, 1, 1)
		ax.scatter(theta, y, c="red")

		ax.set_xlabel(r"$\theta$")
		ax.set_ylabel(r"$E(\theta)$")

		plt.savefig(out_path)
		plt.close(fig)

	def plot_raw(self, path, col_name):
		print("plotando", path)
		data = pd.read_csv(path, index_col=False)

		y = converter.convert(data[col_name].values)
		x = range(0, len(y))

		fig = plt.figure()

		ax = fig.add_subplot(1, 1, 1)
		ax.scatter(x, y, color='red', s = 3)

		plt.show()
		plt.close(fig)

	def save(self, path, data):
		self.save_fig(data, path + ".png")
		self.save_data(data, path + ".csv")

class SimpleData:
	def __init__(self, path, col_name, init_v, converter):
		print(path)
		dpi = 100

		data = pd.read_csv(path, index_col=False)
		y = converter.convert(data[col_name].values)
		fig = plt.figure(figsize=(12, 8), dpi=dpi, constrained_layout=True)

		self.y = y
		self.tm = []
		self.var = []
		self.n = []
		self.theta = []

		for i in range(0, len(init_v) - 1):
			start = init_v[i]
			end = init_v[i + 1]
			C = remove_trail(y[start:end])
			t = range(0, len(C))

			E = calculate_E(C, t)
			tau = calculate_tau(E, t)
			theta = calculate_theta(t, tau)
			Etheta = calculate_Etheta(E, tau)

			ax = fig.add_subplot(3, 2, i + 1)
			var = calculate_var(E, t, tau)
			n = calculate_n(tau, var)
			ax.scatter(theta, Etheta, label = f"N = {n}, tau = {tau}")
			plt.legend()
		plt.show()
		plt.close(fig)

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
		self.theta = []

		for i in range(0, len(init_v) - 1):
			self.add_range(init_v[i], init_v[i + 1])

	def add_range(self, start, end):
		x, theta, y = transform_curve(self.y[start:end])
		fit_len = int(len(y) * 0.8)

		fit = regression.CustomCurve(x[0:fit_len], y[0:fit_len])
		self.output.append(y)
		self.theta.append(theta)

		tm, var, n = fit.values()

		self.tm.append(rd(tm))
		self.var.append(rd(var))
		self.n.append(rd(n))
		self.fit.append(fit.fit(x))

#converter = Converter(0.0001, -0.072)
converter = Converter(0.0001, -0.072)
render = Render(2)

SimpleData("data/plan_plate/09_06_26_01.csv", "AM1", [ 933, 1815, 2693, 3571, 4448, 5323 ], converter)
# render.save("data/plan_plate/01_best", Data("data/plan_plate/09_06_26_01.csv", "AM1", [ 2693, 3571 ], converter)) # [ 933, 1815, 2693, 3571, 4448, 5323 ] - 3
# render.save("data/plan_down/01_best", Data("data/plan_down/14_06_26_01.csv", "AM1", [ 3578, 4456 ], converter)) # [ 937, 1823, 2701, 3578, 4456, 5330 ] - 4
# render.save("data/plan_up/01_best", Data("data/plan_up/20_06_26_01.csv", "AM1", [ 1120, 2000 ], converter)) # [ 1120, 2000, 2875, 3756, 4632, 5512, 6390 ] - 1

# render.save("data/plan_plate/01", Data("data/plan_plate/09_06_26_01.csv", "AM1", [ 933, 1815, 2693, 3571, 4448, 5323 ], converter))
# render.save("data/plan_plate/02", Data("data/plan_plate/10_06_26_02.csv", "AM1", [909, 1784, 2663, 3544, 4423, 5300], converter))
# render.save("data/plan_plate/03", Data("data/plan_plate/10_06_26_03.csv", "AM1", [434, 1309, 2190, 3069, 3949, 4828, 5676], converter))
# render.save("data/plan_plate/04", Data("data/plan_plate/10_06_26_04.csv", "AM1", [1155, 2033, 2909, 3793, 4671, 5432], converter))
# render.save("data/plan_plate/06", Data("data/plan_plate/11_06_26_06.csv", "AM1", [917, 1792, 2668, 3549, 4431, 5290], converter))
# render.save("data/plan_plate/08", Data("data/plan_plate/11_06_26_08.csv", "AM1", [966, 1843, 2722, 3600, 4479, 5347], converter))
# render.save("data/plan_plate/10", Data("data/plan_plate/30_03_26_10.csv", "AM1", [49, 461, 873, 1287, 1705, 2115], converter))
# render.save("data/plan_plate/13", Data("data/plan_plate/30_03_26_13.csv", "AM1", [386, 802, 1218, 1635, 2054, 2471, 2880], converter))
# render.save("data/plan_plate/14", Data("data/plan_plate/02_04_26_14.csv", "AM1", [352, 766, 1184, 1598, 2018, 2433, 2847, 3255], converter))

# render.save("data/plan_down/01", Data("data/plan_down/14_06_26_01.csv", "AM1", [ 937, 1823, 2701, 3578, 4456, 5330 ], converter))
# render.save("data/plan_down/02", Data("data/plan_down/14_06_26_02.csv", "AM1", [ 931, 1810, 2692, 3570, 4442, 5320 ], converter))
# render.save("data/plan_down/03", Data("data/plan_down/14_06_26_03.csv", "AM1", [ 942, 1824, 2714, 3588, 4474, 5344 ], converter))
# render.save("data/plan_down/04", Data("data/plan_down/14_06_26_04.csv", "AM1", [ 957, 1839, 2717, 3594, 4468, 5350 ], converter))
# render.save("data/plan_down/06", Data("data/plan_down/14_06_26_06.csv", "AM1", [ 902, 1776, 2658, 3535, 4417, 5286 ], converter))
# render.save("data/plan_down/08", Data("data/plan_down/14_06_26_08.csv", "AM1", [ 996, 1880, 2753, 3625, 4505, 5389 ], converter))
# render.save("data/plan_down/05", Data("data/plan_down/19_06_26_05.csv", "AM1", [ 878, 1768, 2646, 3520, 4394, 5276 ], converter))
# render.save("data/plan_down/10", Data("data/plan_down/19_06_26_10.csv", "AM1", [ 921, 1795, 2676, 3566, 4447, 5320], converter))
# render.save("data/plan_down/13", Data("data/plan_down/19_06_26_13.csv", "AM1", [ 895, 1774, 2650, 3533, 4412, 5288 ], converter))
# render.save("data/plan_down/14", Data("data/plan_down/19_06_26_14.csv", "AM1", [ 928, 1802, 2687, 3564, 4441, 5310 ], converter))

# render.save("data/plan_up/01", Data("data/plan_up/20_06_26_01.csv", "AM1", [ 1120, 2000, 2875, 3756, 4632, 5512, 6390 ], converter))
# render.save("data/plan_up/02", Data("data/plan_up/20_06_26_02.csv", "AM1", [ 890, 1769, 2636, 3531, 4402, 5277 ], converter))
# render.save("data/plan_up/03", Data("data/plan_up/20_06_26_03.csv", "AM1", [ 895, 1771, 2643, 3519, 4403, 5283 ], converter))
# render.save("data/plan_up/04", Data("data/plan_up/20_06_26_04.csv", "AM1", [ 866, 1749, 2631, 3498, 4380, 5263 ], converter))
# render.save("data/plan_up/06", Data("data/plan_up/20_06_26_06.csv", "AM1", [ 885, 1763, 2641, 3519, 4401, 5267 ], converter))
# render.save("data/plan_up/08", Data("data/plan_up/21_06_26_08.csv", "AM1", [ 944, 1829, 2702, 3587, 4468, 5345 ], converter))
# render.save("data/plan_up/10", Data("data/plan_up/21_06_26_10.csv", "AM1", [ 938, 1816, 2694, 3572, 4451, 5329 ], converter))
# render.save("data/plan_up/13", Data("data/plan_up/21_06_26_13.csv", "AM1", [ 881, 1755, 2637, 3519, 4392, 5282 ], converter))
# render.save("data/plan_up/14", Data("data/plan_up/21_06_26_14.csv", "AM1", [ 887, 1771, 2647, 3527, 4406, 5290 ], converter))

# render.plot(Data("data/plan_plate/09_06_26_01.csv", "AM1", [ 933, 1815, 2693, 3571, 4448, 5323 ], converter))
# render.plot(Data("data/plan_down/14_06_26_01.csv", "AM1", [ 937, 1823, 2701, 3578, 4456, 5330 ], converter))
# render.plot(Data("data/plan_up/20_06_26_01.csv", "AM1", [ 1120, 2000, 2875, 3756, 4632, 5512, 6390 ], converter))

# render.plot(Data("data/plan_plate/10_06_26_02.csv", "AM1", [909, 1784, 2663, 3544, 4423, 5300], converter))
# render.plot(Data("data/plan_down/14_06_26_02.csv", "AM1", [ 931, 1810, 2692, 3570, 4442, 5320 ], converter))
# render.plot(Data("data/plan_up/20_06_26_02.csv", "AM1", [ 890, 1769, 2636, 3531, 4402, 5277 ], converter))

# render.plot(Data("data/plan_plate/10_06_26_03.csv", "AM1", [434, 1309, 2190, 3069, 3949, 4828, 5676], converter))
# render.plot(Data("data/plan_down/14_06_26_03.csv", "AM1", [ 942, 1824, 2714, 3588, 4474, 5344 ], converter))
# render.plot(Data("data/plan_up/20_06_26_03.csv", "AM1", [ 895, 1771, 2643, 3519, 4403, 5283 ], converter))

# render.plot(Data("data/plan_plate/10_06_26_04.csv", "AM1", [1155, 2033, 2909, 3793, 4671, 5432], converter))
# render.plot(Data("data/plan_down/14_06_26_04.csv", "AM1", [ 957, 1839, 2717, 3594, 4468, 5350 ], converter))
# render.plot(Data("data/plan_up/20_06_26_04.csv", "AM1", [ 866, 1749, 2631, 3498, 4380, 5263 ], converter))

# render.plot(Data("data/plan_down/19_06_26_05.csv", "AM1", [ 878, 1768, 2646, 3520, 4394, 5276 ], converter))

# render.plot(Data("data/plan_plate/11_06_26_06.csv", "AM1", [917, 1792, 2668, 3549, 4431, 5290], converter))
# render.plot(Data("data/plan_down/14_06_26_06.csv", "AM1", [ 902, 1776, 2658, 3535, 4417, 5286 ], converter))
# render.plot(Data("data/plan_up/20_06_26_06.csv", "AM1", [ 885, 1763, 2641, 3519, 4401, 5267 ], converter))

# render.plot(Data("data/plan_plate/11_06_26_08.csv", "AM1", [966, 1843, 2722, 3600, 4479, 5347], converter))
# render.plot(Data("data/plan_down/14_06_26_08.csv", "AM1", [ 996, 1880, 2753, 3625, 4505, 5389 ], converter))
# render.plot(Data("data/plan_up/21_06_26_08.csv", "AM1", [ 944, 1829, 2702, 3587, 4468, 5345 ], converter))

# render.plot(Data("data/plan_plate/30_03_26_10.csv", "AM1", [49, 461, 873, 1287, 1705, 2115], converter))
# render.plot(Data("data/plan_down/19_06_26_10.csv", "AM1", [ 921, 1795, 2676, 3566, 4447, 5320], converter))
# render.plot(Data("data/plan_up/21_06_26_10.csv", "AM1", [ 938, 1816, 2694, 3572, 4451, 5329 ], converter))

# render.plot(Data("data/plan_plate/30_03_26_13.csv", "AM1", [386, 802, 1218, 1635, 2054, 2471, 2880], converter))
# render.plot(Data("data/plan_down/19_06_26_13.csv", "AM1", [ 895, 1774, 2650, 3533, 4412, 5288 ], converter))
# render.plot(Data("data/plan_up/21_06_26_13.csv", "AM1", [ 881, 1755, 2637, 3519, 4392, 5282 ], converter))

#render.plot(Data("data/plan_plate/02_04_26_14.csv", "AM1", [352, 766, 1184, 1598, 2018, 2433, 2847, 3255], converter))
#render.plot(Data("data/plan_down/19_06_26_14.csv", "AM1", [ 928, 1802, 2687, 3564, 4441, 5310 ], converter))
#render.plot(Data("data/plan_up/21_06_26_14.csv", "AM1", [ 887, 1771, 2647, 3527, 4406, 5290 ], converter))

