#!/usr/bin/env python

from numpy import linspace, meshgrid, vectorize, where, array, roll, sum, log, sqrt, exp
from matplotlib import pyplot as plt
from scipy.spatial import ConvexHull
from scipy.optimize import curve_fit

# a
def julia_set_pixel(z0, c, max_iter, r):
	z = z0
	for i in range(max_iter):
		if abs(z) > r:
			return i
		z = z**2 + c
	return max_iter
julia_set_pixel = vectorize(julia_set_pixel)

re_min = -1.5
re_max = 1.5
im_min = -1
im_max = 1
re_width = 800
im_width = 800
re, im = meshgrid(linspace(re_min, re_max, re_width), linspace(im_min, im_max, im_width))
z0 = re + 1j*im
c = -0.7+0.356j
max_iter = 256
r = 2
pixels = julia_set_pixel(z0, c, max_iter, r)
plt.pcolor(re, im, pixels, cmap='inferno')
plt.xlabel('Re')
plt.ylabel('Im')

# b
def plot_polygon(points):
	xs, ys = zip(*points)
	xs += xs[:1]
	ys += ys[:1]
	plt.plot(xs, ys, 'r-')

def area_of_polygon(polygon):
	xs, ys = array(polygon).T
	return 0.5*sum(roll(xs, 1)*ys - xs*roll(ys, 1))

julia_threshold = max_iter/2
pixels_bool = pixels > julia_threshold
points = list(zip(re[pixels_bool], im[pixels_bool]))
hull = [points[v] for v in ConvexHull(points).vertices]
print(f'Area of the convex hull: {area_of_polygon(hull)}')

plot_polygon(hull)
plt.show()

# c
def scale_down(arr, b):
	m, n = arr.shape
	if arr.dtype == bool:
		return arr.reshape(m//b, b, n//b, b).any(axis=(1, 3))
	elif arr.dtype == float:
		return arr.reshape(m//b, b, n//b, b).mean(axis=(1, 3))

def pixels_boundary(bool_array):
	up = roll(bool_array, 1, axis=0)
	down = roll(bool_array, -1, axis=0)
	left = roll(bool_array, 1, axis=1)
	right = roll(bool_array, -1, axis=1)
	return bool_array & ~(up & down & left & right)

b = 8
scale_down_pixels_bool = scale_down(pixels_bool, 8)
scale_down_re = scale_down(re, 8)
scale_down_im = scale_down(im, 8)
contour = pixels_boundary(scale_down_pixels_bool)
print(f'Area of contour: {sum(scale_down_pixels_bool) * (re_max - re_min) * (im_max - im_min) / (re_width/b * im_width/b)}')

plt.pcolor(re, im, pixels, cmap='inferno')
plt.xlabel('Re')
plt.ylabel('Im')
plt.scatter(scale_down_re[contour], scale_down_im[contour], s=3)
plt.show()

# d
b_values = array([32, 16, 8, 4, 2, 1])
box_area = (re_max - re_min) * (im_max - im_min) / (re_width/b_values * im_width/b_values)
num_boxes = array([sum(pixels_boundary(scale_down(pixels_bool, b))) for b in b_values])
x = 1/sqrt(box_area)
plt.plot(x, num_boxes, 'o-')
plt.xlabel(r'$1/\epsilon$')
plt.ylabel(r'$N(\epsilon)$')
plt.xscale('log')
plt.yscale('log')

def proportionality(x, a):
	return a*x

popt, _ = curve_fit(proportionality, log(x)[:4], log(num_boxes)[:4])
print(f'Fractal dimension: {popt[0]}')
plt.plot(x, exp(proportionality(log(x), *popt)))

plt.show()
