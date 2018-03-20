import numpy as np
import pylab as Plot
import re
from scipy.cluster.hierarchy import fclusterdata,linkage,dendrogram,fcluster
from matplotlib import pyplot as plt
from sklearn import metrics
import Levenshtein
import scipy
import scipy.spatial
import time
from random import shuffle
def getMatrix(InputFile):
	Seqs=[]
	f= open(InputFile,'r')
	for line in f:
		
		if re.search('>', line):
			pass
		else:
			Seqs.append(line.strip())

	n = len(Seqs)
	#print Seqs
	#print Seqs
	#shuffle(Seqs)

	#print Seqs
	my_array = np.zeros((n,n))
	
	for i, ele_1 in enumerate(Seqs):
	    for j, ele_2 in enumerate(Seqs):
	        if j >= i:
	            break # Since the matrix is symmetrical we don't need to
	                  # calculate everything
	        #difference = EditDistance(ele_1, ele_2) 
	        #difference = editDistDP(ele_1, ele_2,len(ele_1),len(ele_2)) 
	        difference = Levenshtein.distance(ele_1, ele_2) /float(min(len(ele_1),len(ele_2)))
	        my_array[i, j] = difference
	        my_array[j, i] = difference
	# print my_array


	# matrix = scipy.spatial.distance.pdist(Seqs[0:n], lambda u,v: Levenshtein.distance(u,v))
	# print matrix
	return my_array

# A Dynamic Programming based Python program for edit
# distance problem
def shuffleFile(infile):
    Seqs=[]
    f= open(infile,'r')
    for line in f:
       
        if re.search('>', line):
            pass
        else:
            Seqs.append(line.strip())

    n = len(Seqs)
    f1 = open(infile , 'w')
    shuffle(Seqs)
    count=1
    for seq in Seqs:
        f1.write(">seq%i"%(count))
        f1.write("\n")
        f1.write(seq)
        f1.write("\n")
        count+=1
    f1.close()
def editDistDP(str1, str2, m, n):
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n+1)] for x in range(m+1)]
 
    # Fill d[][] in bottom up manner
    for i in range(m+1):
        for j in range(n+1):
 
            # If first string is empty, only option is to
            # isnert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace
 
    return dp[m][n]

def EditDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]


def getOptimalLabels(infileName,kRange):
	#get the optimal labels after performing silhoutte method to find optimal k
	t0= time.time()
	X= getMatrix(infileName)
	#print X
	Z = linkage(X, 'single')
	t1 = time.time()
	kvsSil = []
	idx = 0
	t2 = time.time()
	for i in range(kRange):
		i = i+2
		clusters =fcluster(Z, i, criterion='maxclust')
		silhoutte = metrics.silhouette_score(X, clusters, metric='precomputed')
		#print "for k = ",i ,", silhoutte coeff = ", silhoutte
		kvsSil.append((i,silhoutte))


	maxk = max(kvsSil , key = lambda item:item[1])
	print "optimal k = ",maxk[0]
	
	labelsOptimal = fcluster(Z, maxk[0], criterion='maxclust')
	t3 = time.time()
	timeH = (t2-t0)+(t3-t2)/float(kRange+1)
	print timeH
	return labelsOptimal,timeH

#####################
#printing cluster with different height
#print [fcluster(Z, height, criterion='maxclust') for height in range(5)]
def getOptimalLabelsWithMaxK(infileName , k):
	t0= time.time()
	X= getMatrix(infileName)
	#print X
	Z = linkage(X, 'single')
	
	labelsOptimal = fcluster(Z, k, criterion='maxclust')
	t3 = time.time()
	timeH =(t3-t0)
	#print timeH
	return labelsOptimal,timeH

def plotDendrogramAndSilhoutteCurve(infileName,kI):
	X= getMatrix(infileName)
	print X
	Z = linkage(X, 'single')
	#print Z
	fig = plt.figure(figsize=(25, 10))
	dn = dendrogram( Z
    #leaf_rotation=90.,  # rotates the x axis labels
    #leaf_font_size=7.,  # font size for the x axis labels
    )
	plt.show()
	max_d = 0.02
	#clusters = fcluster(Z, max_d, criterion='distance')
	# clusters1 =fcluster(Z, 10, criterion='maxclust')
	# silhoutte1 = metrics.silhouette_score(X, clusters1, metric='euclidean')
	# print silhoutte1

	#calculating silhoutte coefficent
	lisK =[]
	lisSilhoutte = []
	kvsSil = []
	idx = 0
	for i in range(kI):
		i = i+2
		clusters =fcluster(Z, i, criterion='maxclust')
		silhoutte = metrics.silhouette_score(X, clusters, metric='precomputed')
		print "for k = ",i ,", silhoutte coeff = ", silhoutte
		lisK.append(i)
		lisSilhoutte.append(silhoutte)
		kvsSil.append((i,silhoutte))


	maxk = max(kvsSil , key = lambda item:item[1])
	print "optimal k = ",maxk[0]
	labelsOptimal = fcluster(Z, maxk[0], criterion='maxclust')
	print "labels :",labelsOptimal
	plt.xticks(lisK)
	plt.scatter(lisK,lisSilhoutte)
	plt.plot(lisK,lisSilhoutte)
	plt.axvline(x=maxk[0], color = 'red', linestyle = '--')
	plt.xlabel('k value')
	plt.ylabel('Silhoutte Coefficent')
	plt.show()

def returnSilhoutteValues(inFile,kRange):
	#identify the silhoutte value for different k range
	X= getMatrix(inFile)
	Z = linkage(X, 'single')
	#dn = dendrogram(Z)
	#calculating silhoutte coefficent
	lisSilhoutte = []
	idx = 0
	for i in range(2,kRange+1):
		clusters =fcluster(Z, i, criterion='maxclust')
		silhoutte = metrics.silhouette_score(X, clusters, metric='precomputed')
		#print "for k = ",i ,", silhoutte coeff = ", silhoutte
		lisSilhoutte.append(silhoutte)

	return lisSilhoutte
	
#print returnSilhoutteValues('top10.fasta',10)
#plotDendrogramAndSilhoutteCurve('clusters')
#print getOptimalLabels('top10.fasta',10)
#print getMatrix('test.fasta')