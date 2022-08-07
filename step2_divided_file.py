#!/usr/bin/python
### Split variant information by gene into separate vcf files.

import sys

t = []

header = open(sys.argv[2],'r').readlines()[0]

for l in open(sys.argv[1],'r'):

	m = l.split('\t')
	gene = m[0]
	out_file = open(gene+'.indel.vcf','a')
	if gene not in t:
		t.append(gene)
		print(header,file = out_file,end = '')
		#print('\t'.join(m[1:]),file = out_file,end = '')
		print('\t'.join(m),file = out_file,end = '')
	else:
		#print('\t'.join(m[1:]),file = out_file,end = '')
		print('\t'.join(m),file = out_file,end = '')
		
	
