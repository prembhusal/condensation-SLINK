import os,sys,re
import subprocess
import optimalClust as oc
import reDistributeCdhitLabels as relabels
from sklearn.metrics.cluster import normalized_mutual_info_score
from matplotlib import pyplot as plt
import optimalClust as oc
import numpy as np
def test():
	x = [1,2,3,4,5]
	identity = ['10k','20k','30k','40k','50k']
	# s10k = [3288,7316,9572]
	# s20k = [5888,13473,18628]
	# s30k = [8146,18925,27478]
	# s40k = [10010,23891,35856]
	# s50k = [11776,28528,43968]
	k85 = [1094,1939,2645,3116,3766]
	k90 = [3288,5888,8146,10010,11776]
	k95 = [7316,13473,18925,23891,28528]
	k98 = [9572,18628,27478,35856,43968]
	plt.scatter(x,k85)
	plt.plot(x,k85,linewidth=2,label='85% threshold')
	plt.scatter(x,k90)
	plt.plot(x,k90,linewidth=2,label='90% threshold')
	plt.scatter(x,k95)
	plt.plot(x,k95,linewidth=2,label='95% threshold')
	plt.scatter(x,k98)
	plt.plot(x,k98,linewidth=2,label='98% threshold')
	plt.xticks(x, identity)
	plt.ylim(100,50000)
	plt.xlabel("number of sequences")
	plt.ylabel("Number of cluster")
	plt.grid(True)
	plt.legend(loc = 'top left')
	plt.show()
def plotForDatasets():
	dataset = ['1000RU.fasta','1500RU.fasta','2000RU.fasta']
	time = []
	for fileN in dataset:
		(trueL,tH)= oc.getOptimalLabels(fileN,20)
		time.append(tH) 
	
	x = [1,2,3]
	plt.bar(x, time, 0.4 ,color = 'g')
	plt.xticks(x, dataset)

	plt.xlabel('datasets')
	plt.ylabel('time in seconds')
	plt.grid(True)
	plt.show()
#plotForDatasets()
test()