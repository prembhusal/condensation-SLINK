
import sys
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage,fcluster
from matplotlib import pyplot as plt

infile = open(sys.argv[1]) # input vector file with comma seperated values
k = int(sys.argv[2]) # input k value to get max k cluster
X = []
for line in infile:
	line = line.strip().split(",")
	X.append([float(line[0]),float(line[1])])

Z = linkage(X, 'single') 
fig = plt.figure(figsize=(25,10))
dn = dendrogram(Z)
plt.show()



clusters = fcluster(Z, k, criterion='maxclust')
for i in clusters:
	print i
