import random
import os,sys
from Bio import SeqIO
from random import sample


infile = sys.argv[1]
n = int(sys.argv[2])
def get():
	with open(infile) as f:
	    data = f.read().splitlines()
	    for i in random.sample(range(0, len(data), n), n):
	        print data[i]
	        print data[i+1]

def get1():
	with open(infile) as f:
		    seqs = SeqIO.parse(f, "fasta")
		    samps = ((seq.name, seq.seq) for seq in  sample(list(seqs),n))
		    for samp in samps:
		        print(">{}\n{}".format(*samp))


get1()