import os,sys,re
import subprocess
import optimalClust as oc
import reDistributeCdhitLabels as relabels
from sklearn.metrics.cluster import normalized_mutual_info_score
from matplotlib import pyplot as plt
import time

inFile = sys.argv[1]
#inFile is input fasta file
#Id = float(sys.argv[2])

#parsing output to find no of clusters
# cmd = "./cd-hit -i "+inFile+" -o clusters -c "+str(Id)+" -n 5"
# p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
# (output, err) = p.communicate()
# match = re.search('(\d+)\s*clusters', output)
# if match:
# 	print match.group(1)
################
def plotGraph():
	NMI = []
	Clusters = []
	kCentroid = []
	identity = [85,90,95,98]
	cdTime = []
	hierarchyTime = []

	(trueL,tH)= oc.getOptimalLabels(inFile,15)
	tlabel = [ int(t) for t in trueL]
	maxk = max(tlabel)
	#for i in range(90,100):
	for i in identity:
		#identity.append(i)
		i = float(i)/100
		print i
		t0 = time.time()
		cmd = "./cd-hit -i "+inFile+" -o clusters -c "+str(i)+" -n 5"
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
		t1 = time.time()
		nClust = re.findall(r"(\d+)\s*clusters", output)
		nMax = max(nClust , key = lambda item:int(item[0]))
		Clusters.append(nMax)

		(predL,tHierarchy) = relabels.redistributeLabels(15)

		clabel = [ int(t) for t in predL]
		maxc = max(clabel)
		kCentroid.append(maxc)
		NMI.append(normalized_mutual_info_score(tlabel, clabel))
		cdTime.append((t1-t0))
		hierarchyTime.append(tHierarchy)
		#NMIscore = normalized_mutual_info_score(tlabel, clabel)
	#print Clusters
	#print cdTime
	#print hierarchyTime
	print NMI
	#no of items for second stage
	plt.scatter(identity,Clusters)
	plt.plot(identity,Clusters)
	plt.xlabel('Distance Threshold for CD-HIT in %')
	plt.ylabel('Number of CD-HIT Centroids')
	plt.grid(True)
	plt.show()

	#plot k values
	#print kCentroid
	plt.scatter(identity,kCentroid)
	plt.plot(identity,kCentroid)
	plt.axhline(y=maxk, color='r', linestyle='--')
	plt.legend(loc='lower right')
	plt.xlabel('iDistance Threshold for CD-HIT in %')
	plt.ylabel('optimal k value')
	plt.grid(True)
	plt.show()

	#plot NMI score 
	plt.scatter(identity,NMI)
	plt.plot(identity,NMI)
	plt.xlabel('Distance Threshold for CD-HIT in %')
	plt.ylabel('NMI score ')
	plt.xticks(identity, identity)
	plt.grid(True)
	plt.show()

	#plot stacked bar
	width = 0.4 
	p1 = plt.bar(identity, cdTime, width ,color = 'g')
	p2 = plt.bar(identity, hierarchyTime,width , color = 'r', bottom = cdTime)
	plt.xticks(identity, identity)
	plt.legend((p1[0], p2[0]), ('cdHit', 'hierarchial'),loc='upper left')
	plt.xlabel('Distance Threshold for CD-HIT in %')
	plt.ylabel('time in seconds')
	plt.grid(True)
	plt.show()

def plotGraphWithMaxk():
	NMI = []
	Clusters = []
	identity = [85,90,95,98]
	cdTime = []
	hierarchyTime = []

	(trueL,tH)= oc.getOptimalLabels(inFile,10)
	tlabel = [ int(t) for t in trueL]
	#kMax = max(tlabel)
	kMax = 9
	#for i in range(90,100):
	for i in identity:
		#identity.append(i)
		i = float(i)/100
		print i
		t0 = time.time()
		cmd = "./cd-hit -i "+inFile+" -o clusters -c "+str(i)+" -n 5"
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
		t1 = time.time()
		nClust = re.findall(r"(\d+)\s*clusters", output)
		nMax = max(nClust , key = lambda item:int(item[0]))
		Clusters.append(nMax)

		(predL,tHierarchy) = relabels.redistributeLabelsKmax(kMax)

		clabel = [ int(t) for t in predL]
		NMI.append(normalized_mutual_info_score(tlabel, clabel))
		cdTime.append((t1-t0))
		hierarchyTime.append(tHierarchy)
		#NMIscore = normalized_mutual_info_score(tlabel, clabel)
	print Clusters
	print cdTime
	print hierarchyTime
	#no of items for second stage
	plt.scatter(identity,Clusters)
	plt.plot(identity,Clusters)
	plt.xlabel('Distance Threshold for CD-HIT in %')
	plt.ylabel('Number of CD-HIT Centroids')
	plt.xticks(identity, identity)
	plt.grid(True)
	plt.show()

	#plot NMI score 
	plt.scatter(identity,NMI)
	plt.plot(identity,NMI)
	plt.xlabel('Distance Threshold for CD-HIT in %')
	plt.ylabel('NMI score ')
	plt.xticks(identity, identity)
	plt.grid(True)
	plt.show()

	#plot stacked bar
	width = 0.4 
	p1 = plt.bar(identity, cdTime, width ,color = 'g')
	p2 = plt.bar(identity, hierarchyTime,width , color = 'r', bottom = cdTime)
	plt.axhline(y=tH, color='r', linestyle='--')
	plt.xticks(identity, identity)
	plt.legend((p1[0], p2[0]), ('cdHit', 'hierarchial'),loc='upper left')
	plt.xlabel('Distance Threshold for CD-HIT in %')
	plt.ylabel('time in seconds')
	plt.grid(True)
	plt.show()


def plotForDatasets():
	dataset = ['1000R.fasta','1500R.fasta','2000R.fasta']
	time = []
	for data in dataset:
		(trueL,tH)= oc.getOptimalLabels(data,20)
		time.append(tH) 
	plt.bar(dataset, time, 0.4 ,color = 'g')
	plt.xlabel('datasets')
	plt.ylabel('time in seconds')
	plt.grid(True)
	plt.show()

def plotSilCurve():
	i = [.90,.95,.98]
	originalSil = oc.returnSilhoutteValues(inFile,20)
	silAll = []
	for idx in i:
		cmd = "./cd-hit -i "+inFile+" -o clusters -c "+str(idx)+" -n 5"
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
		sil = oc.returnSilhoutteValues('clusters',20)
		silAll.append(sil)
	#print silAll
	xlabel = list(range(2, 21))
	plt.scatter(xlabel,originalSil)
	plt.plot(xlabel,originalSil, linewidth =1.5, label="SLINK",color = 'red')
	kMaxO = originalSil.index(max(originalSil)) +2
	#print kMaxO 
	plt.axvline(x=kMaxO, color = 'red', linestyle = '--')
	#print silAll[0]
	plt.scatter(xlabel,silAll[0])
	plt.plot(xlabel,silAll[0], linewidth =1.5, label="90% threshold",color = 'green')
	kMax90 = silAll[0].index(max(silAll[0])) +2
	plt.axvline(x=kMax90, color = 'green', linestyle = '--')

	plt.scatter(xlabel,silAll[1])
	plt.plot(xlabel,silAll[1], linewidth =1.5, label="95% threshold",color = 'blue')
	kMax95 = silAll[1].index(max(silAll[1])) +2
	plt.axvline(x=kMax95, color = 'blue', linestyle = '--')

	plt.scatter(xlabel,silAll[2])
	plt.plot(xlabel,silAll[2], linewidth =1.5, label="98% threshold",color = 'black')
	kMax98 = silAll[2].index(max(silAll[2])) +2
	plt.axvline(x=kMax98, color = 'black', linestyle = '--')

	plt.legend(loc = 'upper right')
	plt.xticks(xlabel, xlabel)
	plt.xlabel("value of k")
	plt.ylabel("silhoutte coefficent")

	plt.show()




plotGraph()
#plotSilCurve()
#plotGraphWithMaxk()


