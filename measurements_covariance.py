#!/usr/bin/python3
import numpy as np
from math import hypot
from collections import defaultdict
mean_algo = np.zeros(7)
mean_aspect = np.zeros(10)
covariance = np.zeros((mean_algo.size, mean_aspect.size))

n = 0
algo_map = dict()
algo_list = defaultdict(list)
enabled = False
dirname = "instagram/"
while 1:
	try:
		row = input().split(",")
	except EOFError:
		row = None
	if row and row[0][0] == " ":
		#calculate average hypot of each algorithm
		name = row[0][1:]
		index = algo_map.setdefault(name, len(algo_map))
		value = hypot(*(float(v) for v in row[1:])) #/ radius
		#print("got algo:", name, "->", index, value)
		algo[index] += value
		algo_list[name].append(value)
	else:
		#add d_algo * d_aspect.t() to the covariance
		if enabled and aspect is not None:
			diff_algo, diff_aspect = algo - mean_algo, aspect - mean_aspect;
			mean_algo += diff_algo / (n + 1);
			mean_aspect += diff_aspect / (n + 1);
			covariance += np.outer(diff_algo, diff_aspect) * n / (n + 1);
			n += 1
		if not row:
			#print("empty row, exit.")
			break
		img_name = row[0]
		enabled = img_name.startswith(dirname)
		aspect = np.array([float(v) for v in row[3:]])
		algo = np.zeros(7)
		#print("got block:", aspect)

print("algo mean over", dirname)
for name, index in algo_map.items():
	print(name, mean_algo[index])

print()
print("algo quartiles", dirname)
for name, l in algo_list.items():
	l.sort()
	print(name, *("{:.2f}".format(v) for v in (l[len(l)//4], l[len(l)//2], l[3*len(l)//4])), sep = " & ")
	
print(*algo_list.keys())
with open("performance.tab", "w") as table:
	for i, vals in enumerate(zip(*algo_list.values())):
		print(i, *vals, file=table, sep="\t")

print()
print("covariance:")
columns = ["Radius", "Iris brightness","Iris boundary","Image contrast","Image size","Occlusion or closed eyelids","Glare","Makeup","Shadow","Dark skin"]
indices = [i for i in range(len(columns)) if covariance[:,i].any()]
print("\\begin{tabular}{l@{\hspace{1.5cm}}", "D{.}{.}{3.2}" * len(indices), "}", sep="")
print("\\toprule")
print("\\textbf{Algorithm}", *("\\mc{\\textbf{%s}}" % columns[i] for i in indices), end = "\\\\\n", sep=" & ")
print("\\midrule")
for name, index in algo_map.items():
	r = covariance[index,:] / (n - 1)
	print(name, *("{:.2f}".format(r[i]) for i in indices), end = "\\\\\n", sep=" & ")
