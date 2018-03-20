import os,sys,re
import subprocess
import optimalClust as oc
import reDistributeCdhitLabels as relabels
from sklearn.metrics.cluster import normalized_mutual_info_score
from matplotlib import pyplot as plt
import time
import numpy as np

#this is same as plotGraphs.py but adds repetition of experiment for 10 times to get the standard deviation

inFile = sys.argv[1]
NMI = []
Clusters = []
kCentroid = []
identity = []
cdTime = []
hierarchyTime = []


for i in range(90,100):
	identity.append(i)
	i = float(i)/100
	print i
	NMI1 = []
	Clusters1 = []
	kCentroid1 = []
	identity1 = []
	cdTime1 = []
	hierarchyTime1 = []
	
	for x in range(10):
		
		oc.shuffleFile(inFile)
		(trueL,tH)= oc.getOptimalLabels(inFile,15)
		tlabel = [ int(t) for t in trueL]
		t0 = time.time()
		cmd = "./cd-hit -i "+inFile+" -o clusters -c "+str(i)+" -n 5"
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
		t1 = time.time()
		nClust = re.findall(r"(\d+)\s*clusters", output)
		nMax = max(nClust , key = lambda item:int(item[0]))
		Clusters1.append(int(nMax))

		(predL,tHierarchy) = relabels.redistributeLabels(15)

		clabel = [ int(t) for t in predL]
		maxc = max(clabel)
		kCentroid1.append(maxc)
		NMI1.append(normalized_mutual_info_score(tlabel, clabel))
		cdTime1.append((t1-t0))
		hierarchyTime1.append(tHierarchy)
	NMI.append(NMI1)
	Clusters.append(Clusters1)
	kCentroid.append(kCentroid1)
	cdTime.append(cdTime1)
	hierarchyTime.append(hierarchyTime1)
	#NMIscore = normalized_mutual_info_score(tlabel, clabel)
print Clusters
print cdTime
print hierarchyTime
print NMI
def findMeanStd(lis):
	m = []
	d = []
	for l in lis:
		m.append(np.mean(l))
		d.append(np.std(l))
	return m,d

#no of items for second stage
mC,dC = findMeanStd(Clusters)
plt.scatter(identity,mC)
plt.plot(identity,mC)
plt.errorbar(identity, mC, dC, linestyle='None', marker='^')
plt.xlabel('identity in %')
plt.ylabel('Items for second stage')
plt.grid(True)
plt.show()

#plot k values
#print kCentroid
mK,dK = findMeanStd(kCentroid)
plt.scatter(identity,mK)
plt.plot(identity,mK)
plt.errorbar(identity, mK, dK, linestyle='None', marker='^')
plt.legend(loc='lower right')
plt.xlabel('identity in %')
plt.ylabel('optimal k value')
plt.grid(True)
plt.show()

#plot NMI score 
mN,dN = findMeanStd(NMI)

plt.scatter(identity,mN)
plt.plot(identity,mN)
plt.errorbar(identity, mN, dN, linestyle='None', marker='^')
plt.xlabel('identity in %')
plt.ylabel('NMI score ')
plt.grid(True)
plt.show()

#plot stacked bar
width = 0.4 
mC,dC = findMeanStd(cdTime)
mH,dH = findMeanStd(hierarchyTime)

p1 = plt.bar(identity, mC, width ,color = 'g')
#plt.errorbar(identity, mC, dC, linestyle='None', marker='^')
p2 = plt.bar(identity, mH,width , color = 'r', bottom = mC)
plt.xticks(identity, identity)
plt.legend((p1[0], p2[0]), ('cdHit', 'hierarchial'),loc='upper left')
plt.xlabel('identity in %')
plt.ylabel('time in seconds')
plt.grid(True)
plt.show()







