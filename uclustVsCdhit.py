from matplotlib import pyplot as plt

cdhitT = [55,94,61,52,62]
uclustT = [1.5,.54,1.9,2.6,2.4]
nCdhit = [7983,27673,40115,73067,118037]
nUclust = [9669,30460,48463,93925,138037]

Id = [85,90,92,95,97]

plt.scatter(Id,cdhitT)
plt.plot(Id,cdhitT,label="CdHit")
plt.scatter(Id,uclustT)
plt.plot(Id,uclustT,label="uclust")
plt.xlabel("identity in %")
plt.ylabel("execution time(in minutes)")
plt.legend(loc = 'upper left')
plt.show()

plt.scatter(Id,nCdhit)
plt.plot(Id,nCdhit,label="CdHit")
plt.scatter(Id,nUclust)
plt.plot(Id,nUclust,label="uclust")
plt.xlabel("identity in %")
plt.ylabel("No of clusters")
plt.legend(loc = 'upper left')
plt.show()
