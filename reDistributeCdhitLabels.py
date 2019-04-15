#re distribute the labels after performing hierarchial clustering on the labels obtained from cdhit
import numpy as np
import optimalClust as oc
from collections import Counter
from sklearn.metrics.cluster import normalized_mutual_info_score
import time
def getLabelsWithCentroids():
	#parse the cdHit output file and gives tuple containing (centroid, seqid) 
	f = open('clusters.clstr','r')
	cid = ''
	labels = []
	for line in f:
	    if line.find('Cluster') != -1:
	        temp, cid  = line.strip().split(' ')
	    else:
	        temp, y = line.split('>seq')
	        sid, temp = y.split('...')
	        if temp.find('*') != -1:
	        	centroid = sid
	        labels.append((int(centroid) , int(sid)))
	#labels.sort()
	return labels



def getLabelsWithCentroidsMod():
	#parse the cdHit output file and gives tuple containing (centroid, seqid) 
	f = open('clusters.clstr','r')
	cid = ''
	labels = []
	for line in f:
	    if line.find('Cluster') != -1:
	    	tempSid = []
	    	centroid = None
	    	temp, cid  = line.strip().split(' ')
	    else:
	    	temp, y = line.split('>seq')
	        sid, temp = y.split('...')
	        tempSid.append(sid)
	        if temp.find('*') != -1:
	        	centroid = sid
	        	for ids in tempSid:
	        		labels.append((int(centroid) , int(ids)))
	        	tempSid =[]
	        #print centroid
	        if centroid != None and len(tempSid) != 0:		
				labels.append((int(centroid) , int(sid)))
				del tempSid[:]
	#labels.sort()
	return labels
def getNewLabels(centroidFile,kRange):
	#perform hierarchial clustering in centroid and get new labels (centroid,newLabel)
	f = open(centroidFile , 'r')
	(labels,t) = oc.getOptimalLabels(centroidFile,kRange)
	i =0
	idLabels = []
	for line in f:
		if line.find('>') != -1:
			temp, y = line.split('>seq')
			idLabels.append((int(y),labels[i]))
			i = i+1
	return idLabels,t

	


def redistributeLabels(kRange):
	#re distribute the labels after getting labels from hierarchical algorithm
	finalLP = []
	labels = []
	(l,t)=getNewLabels('clusters',kRange) #(centroid,newLabel)
	c = getLabelsWithCentroidsMod() #(centroid,seqid)
	t0= time.time()
	for (x,y) in l:
		for (a,b) in c:
			if int(x) == int(a) :
				finalLP.append((b,y))

	t1 = time.time()

	print "time: " ,(t1-t0)

	finalLP.sort()
	i=0
	for (x,y) in finalLP:
		labels.append(y)

	return labels,t


#propagating original labels without performing optimal k on cdHit centroids( consider k from baseline labels)
def getNewLabelsKmax(centroidFile,kMax):
	#perform hierarchial clustering in centroid and get new labels (centroid,newLabel)
	f = open(centroidFile , 'r')
	(labels,t) = oc.getOptimalLabelsWithMaxK(centroidFile,kMax)
	i =0
	#print "centroid labels (new labels) :", labels
	idLabels = []
	for line in f:
		if line.find('>') != -1:
			temp, y = line.split('>seq')
			idLabels.append((int(y),labels[i]))
			i = i+1
	return idLabels,t

	


def redistributeLabelsKmax(kMax):
	#re distribute the labels after getting labels from hierarchical algorithm
	finalLP = []
	labels = []
	(l,t)=getNewLabelsKmax('clusters',kMax) #(centroid,newLabel)
	#print "centroid,newlabel : " ,l
	c = getLabelsWithCentroidsMod() #(centroid,seqid)
	#print "centroid, seqid :", c
	t0= time.time()
	for (x,y) in l:
		for (a,b) in c:
			if int(x) == int(a) :
				finalLP.append((b,y))

	t1 = time.time()

	print "time: " ,(t1-t0)

	finalLP.sort()
	i=0
	for (x,y) in finalLP:
		labels.append(y)

	return labels,t

# trueL = oc.getOptimalLabels('top10.txt')
# predL = redistributeLabels()
# tlabel = [ int(t) for t in trueL]
# clabel = [ int(t) for t in predL]
# print "true :" ,tlabel
# print "predicted :", clabel
# print 'NMI score2 : ', normalized_mutual_info_score(tlabel, clabel) 
	

print redistributeLabels(10)
print getLabelsWithCentroidsMod()






