#!usr/bin/python
### Extract variation information within each gene from resequencing VCF files.

import sys 

signal = sys.argv[2]

t = {}

for l in open(sys.argv[1]):

	m = l.replace('\n','')
	t[m] = m


for line in open(signal,'r'):

	if line.startswith('#'):
		pass
	else:
		mes = line.split('\t')
		s = mes[7]
		gene = s.split('|')[3]
		region = s.split('|')[1]
		if '-' not in gene and 'intron' not in region:
			gene = gene.split('.')[0]
			if gene in t:
				print(gene,line,sep = '\t',end = '')
