import numpy as np
from scipy.special import gammainc, gamma
from scipy.integrate import quad, trapezoid

ERR = 100000000
BASE_LENGTH = 1000

class CustomCurve:
	def __init__(self, x, y):
		#data_integral = numeric_integral(x, y)
		data_integral = trapezoid(y, x)

		start = x[0]
		end = x[len(x) - 1]

		self.a = 1.0
		self.n = 1.0
		self.t = 100
		self.err = ERR

		n_vec = np.linspace(1.0, 2.0, 101)
		t_vec = np.linspace(100, 400, 301)

		for n in n_vec:
			for t in t_vec:
				a = data_integral / self.integral(1.0, n, t, 0, end)
				err = self.rest(a, n, t, x, y)

				if err < self.err:
					self.a = a
					self.n = n
					self.t = t
					self.err = err

		if self.err >= ERR:
			raise(Exception("NO PROGRESS HAS BEN MADE"))

		print(f"{self.err}, {self.n}, {self.t}, {self.a}")

	def on(self, a, n, t, x):
		return a * (x / t) ** (n - 1) * n ** n * np.exp(-(x * n) / t)

	def fit(self, x):
		return self.on(self.a, self.n, self.t, x)

	def rest(self, a, n, t, x, y):
		z = (x[len(x) - 1] - np.array(x)) / 50
		y_hat = self.on(a, n, t, x)
		return np.sum(((y - y_hat) * z) ** 2)

	def values(self):
		return self.t, 1, self.n

	def integral(self, a, n, t, start, end):
		return a * t * gamma(n) * gammainc(n, (end * n) / t)

class ExponentialCurve:
	def __init__(self, x, y):
		data_integral = numeric_integral(x, y)

		start = x[0]
		end = x[len(x) - 1]

		self.a = 1.0
		self.b = 0.5
		self.c = 0.5
		self.err = ERR
		delta = 0.5

		for _ in range(4):
			b_vec = np.linspace(self.b - delta, self.b + delta, BASE_LENGTH)
			c_vec = np.linspace(self.c - delta, self.c + delta, BASE_LENGTH)
			delta = delta / BASE_LENGTH

			for b in b_vec:
				for c in c_vec:
					if b < 1e-8 or c < 1e-8 or abs(b - c) < 1e-8:
						continue

					one_integral = self.integral(1.0, b, c, start, end)

					if one_integral < 1e-8:
						continue

					a = data_integral / one_integral
					err = self.rest(a, b, c, x, y)

					if err < self.err:
						self.a = a
						self.b = b
						self.c = c
						self.err = err

		if self.err >= ERR:
			raise(Exception("NO PROGRESS HAS BEN MADE"))

	def on(self, a, b, c, x):
		return a * np.exp(-b * x) - a * np.exp(-c * x)

	def fit(self, x):
		return self.on(self.a, self.b, self.c, x)

	def rest(self, a, b, c, x, y):
		y_hat = self.on(a, b, c, x)
		return np.sum((y - y_hat) ** 2)

	def integral(self, a, b, c, start, end):
		fac1 = (np.exp(-b * start) - np.exp(-b * end))
		fac2 = (np.exp(-c * end) - np.exp(-c * start))

		value = a * (fac1 / b + fac2 / c)

		return value

	def values(self):
		a = self.a
		b = self.b
		c = self.c

		fac1 = (b * c) / (b - c)
		tm = fac1 * (1 / c**2 - 1 / b**2)
		fac2 = (tm**2 / c - (2 * tm) / c**2 + 2 / c**3 - tm**2 / b + (2 * tm) / b**2 - 2 / b**3)
		var = fac1 * fac2

		n = tm ** 2 / var

		return tm, var, n

def numeric_integral(x, y):
	total = 0.0

	for i in range(1, len(x)):
		total += (y[i] + y[i - 1]) * (x[i] - x[i - 1]) * 0.5

	return total

def numeric_testing(a, n, t, start, end):
	x = np.linspace(start, end, 100000)
	return trapezoid(a * (x / t) ** (n - 1) * n ** n * np.exp(-(x / t) * n), x)
	#return trapezoid(a * x ** (n - 1) * n ** n * np.exp(-x * n), x)

def integral_testing(a, n, t, start, end):
	return a * t * gamma(n) * gammainc(n, (end * n) / t)
	#end = (end * n) / t
	#return (a * t * n) * gammainc(n, end) * gamma(n)

def factorial(x):
	if x <= 1:
		return 1

	x * factorial(x - 1)

def test(a, n, tm, end):
	f = lambda t: a * (t / tm) ** (n - 1) * n ** n * np.exp(-(t / tm) * n)

	I, err = quad(f, 0, end)
	lower = a * tm * gamma(n) * gammainc(n, (end * n) / tm)
	num = numeric_testing(a, n, tm, 0, end)

	print(I)
	print(lower)
	print(num)

