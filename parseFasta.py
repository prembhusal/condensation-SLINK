import os, sys
count =1
for line in sys.stdin:
	if line.find('>') != -1:
		print ">seq%i"%(count)
		count += 1
	else:
		print line,
