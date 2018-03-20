import os,sys,re
import subprocess
import optimalClust as oc
import reDistributeCdhitLabels as relabels
from sklearn.metrics.cluster import normalized_mutual_info_score

inFile = sys.argv[1]
Id = float(sys.argv[2])
k = int(sys.argv[3])

def compareNmi():
	cmd = "./cd-hit -i "+inFile+" -o clusters -c "+str(Id)+" -n 5"
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	# match = re.search('(\d+)\s*clusters', output)
	# if match:
	# 	print match.group(1)
	################
	#parse cdHit output and find no of clusters
	nClust = re.findall(r"(\d+)\s*clusters", output)
	nMax = max(nClust , key = lambda item:int(item[0]))
	#print nMax
	p_status = p.wait()
	(trueL,t) = oc.getOptimalLabels(inFile,k)
	oc.plotDendrogramAndSilhoutteCurve(inFile,k)
	oc.plotDendrogramAndSilhoutteCurve('clusters',k)
	(predL,t1) = relabels.redistributeLabels(k)
	tlabel = [ int(t) for t in trueL]
	clabel = [ int(t) for t in predL]
	print "true :" ,tlabel
	print "predicted :", clabel
	print 'NMI score : ', normalized_mutual_info_score(tlabel, clabel) 

def compareNmiKmax():
	cmd = "./cd-hit -i "+inFile+" -o clusters -c "+str(Id)+" -n 5"
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	# match = re.search('(\d+)\s*clusters', output)
	# if match:
	# 	print match.group(1)
	################
	#parse cdHit output and find no of clusters
	nClust = re.findall(r"(\d+)\s*clusters", output)
	nMax = max(nClust , key = lambda item:int(item[0]))
	#print nMax
	p_status = p.wait()
	(trueL,t) = oc.getOptimalLabels(inFile,k)
	tlabel = [ int(t) for t in trueL]
	kMax = max(tlabel)
	#oc.plotDendrogramAndSilhoutteCurve(inFile,k)
	#oc.plotDendrogramAndSilhoutteCurve('clusters',k)
	(predL,t1) = relabels.redistributeLabelsKmax(kMax)
	clabel = [ int(t) for t in predL]
	print "true :" ,tlabel
	print "predicted :", clabel
	print 'NMI score : ', normalized_mutual_info_score(tlabel, clabel) 

compareNmi()

# oc.plotDendrogramAndSilhoutteCurve(inFile)
# oc.plotDendrogramAndSilhoutteCurve('clusters')


