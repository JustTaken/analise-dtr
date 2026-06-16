import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

A = 1.0
B = 0.5
C = 0.5
Delta = 0.5
ERR = 1000000

def convert_current(in_current):
	return in_current * 1.4 + 0.5

def load_data(file):
	data = pd.read_csv(file, index_col=False)

	y = convert_current(data["AI1"].values)
	return y

def f(p, x):
	a, b, c = p

	return a * np.exp(-b * x) - a * np.exp(-c * x)

def data_integral(x, y):
	total = 0.0
	for i in range(1, len(x)):
		total += (y[i] + y[i - 1]) * (x[i] - x[i - 1]) * 0.5
	return total

def rest(y_hat, y):
	return (y - y_hat) ** 2

def test_interval(b, c, delta, length):
	b_vec = np.linspace(b - delta, b + delta, length)
	c_vec = np.linspace(c - delta, c + delta, length)

	return b_vec, c_vec

def integral(a, b, c, s, e):
	return a * ((np.exp(-b * s) - np.exp(-b * e)) / b + (np.exp(-c * e) - np.exp(-c * s)) / c)

def get_integral_ratio(b, c, s, e, data):
	parameterized = integral(1.0, b, c, s, e)
	return data / parameterized

def find_min_sse_coeficients(x, y):
	data_val = data_integral(x, y)
	base_length = 100

	minimum = ERR
	min_b = B
	min_c = C
	min_a = A
	delta = Delta

	for _ in range(4):
		b_vec, c_vec = test_interval(min_b, min_c, delta, base_length)
		delta = delta / base_length

		for b in b_vec:
			for c in c_vec:
				if b < 1e-8 or c < 1e-8 or abs(b - c) < 1e-8:
					continue

				a = get_integral_ratio(b, c, x[0], x[-1], data_val)
				y_hat = f([a, b, c], x)
				sse = np.sum(rest(y_hat, y))

				if sse < minimum:
					minimum = sse
					min_b = b
					min_c = c
					min_a = a

	if minimum >= ERR or min_b == min_c:
		return Exception("not ideal")

	return minimum, min_a, min_b, min_c

def find_fit(x, y):
	m, A_, B_, C_ = find_min_sse_coeficients(x, y)
	p = [A_, B_, C_]
	return f(p, x), p, m

def t_mean(a, b, c):
	return (b * c) / (b - c) * (1 / c**2 - 1 / b**2)

def parameters(a, b, c):
	tm = t_mean(a, b, c)

	fac1 = (b * c) / (b - c)
	fac2 = (tm**2 / c - (2 * tm) / c**2 + 2 / c**3 - tm**2 / b + (2 * tm) / b**2 - 2 / b**3)

	return tm, fac1 * fac2

def rd(x):
	return round(x, 2)

def add_data_to_figure(y, fig, rows, cols, idx):
	x = range(len(y))
	l = len(y)

	m = np.mean(y[l - int(round(l / 10)):l])
	y = y - m
	x = np.arange(0, l)

	fit, param, r = find_fit(x, y)

	a, b, c, = param

	tm, var = parameters(a, b, c)
	n = tm**2 / var

	print(f"{idx} := A({rd(a)}), B({rd(b)}), C({rd(c)}), tm({rd(tm)}), var({rd(var)}), n({rd(n)}), resto({rd(r)})")

	ax = fig.add_subplot(rows, cols, idx)
	ax.scatter(x, y, color='orange', s=3)
	ax.scatter(x, fit, color='red', s=3)

def add_path_to_figure(path, fig, rows, cols, idx):
	y = load_data(path)

	add_data_to_figure(y, fig, rows, cols, idx)

def plot_dir(path, cols):
	files = os.listdir(path)
	n_files = len(files)

	rows = int(np.ceil(n_files / cols))
	fig = plt.figure(figsize=(5 * cols, 4 * rows))

	for idx, f_name in enumerate(files):
		full_path = os.path.join(path, f_name)
		add_path_to_figure(full_path, fig, rows, cols, idx + 1)

	plt.tight_layout()
	plt.show()

	return fig

def plot_multiple_data(path, s):
	fig = plt.figure()
	y = load_data(path)
	print(f"ploting: {path}")

	ys = []
	for i in range(len(s) - 1):
		ys.append(y[s[i]:s[i + 1]])

	cols = 2
	rows = int(np.ceil(len(ys) / cols))

	i = 1
	for y in ys:
		try:
			add_data_to_figure(y, fig, rows, cols, i)
			i += 1
		except:
			continue

	if i == 1:
		print("no data to show")
	else:
		plt.show()

	return fig

# plot_multiple_data("data/plan/28_03_26_02.csv", [ 0, 450, 865, 1270, 1680, 2090, 2515, 2930 ])
plot_multiple_data("data/plan/09_06_26_01.csv", [ 917, 1801, 2681, 3561, 4437, 5323 ])
# plot_multiple_data("data/plan/10_06_26_02.csv", [ 878, 1754, 2631, 3523, 4384, 5300 ])
# plot_multiple_data("data/plan/10_06_26_03.csv", [ 407, 1302, 2172, 3050, 3936, 4806, 5676 ])
# plot_multiple_data("data/plan/10_06_26_04.csv", [ 1093, 1995, 2898, 3793, 4629, 5432 ])
# plot_multiple_data("data/plan/11_06_26_06.csv", [ 886, 1770, 2638, 3538, 4398, 5290 ])
# plot_multiple_data("data/plan/11_06_26_08.csv", [ 941, 1818, 2710, 3578, 4455, 5347 ])

# plot_dir("data/plan/", 2)

