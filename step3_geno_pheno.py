#!/usr/bin/python
### Construct haplotypes of genes and calculate ttests between haplotypes and specific phenotypes.


import sys
import numpy as np
from scipy import stats

trait = sys.argv[1]
vcf = sys.argv[2]

pheno = {}
geno = {}
header = {}
sig = {}


def save_trait(trait):
 
     for p in open(trait,'r'):
 
         p_mes = p.replace('\n','').split('\t')
         individual = p_mes[0]
         trait_value = p_mes[1]
         pheno[individual] = trait_value
 
 
def save_header(num_header,g_mes):
 
     i_num_header = 9
     count_num_header = 1
     while i_num_header <= num_header-1:
         header[count_num_header] = g_mes[i_num_header]
         count_num_header += 1
         i_num_header += 1
 
 
def save_snp(num_header,ref,alt,snp_id,g_mes):
 
     i_num_snp = 9
     count_num_snp = 1
     geno[snp_id] = {}
     while i_num_snp <= num_header-1:
         sample_name = header[count_num_snp]
         if '0/0' in g_mes[i_num_snp]:
             genotype = ref
             geno[snp_id][sample_name] = {}
             geno[snp_id][sample_name][genotype] = pheno[sample_name]
         elif '1/1' in g_mes[i_num_snp]:
             genotype = alt
             geno[snp_id][sample_name] = {}
             geno[snp_id][sample_name][genotype] = pheno[sample_name]
         elif '0/1' in g_mes[i_num_snp]:
             pass
 #            genotype = ref+alt
 #            geno[snp_id][sample_name] = {}
 #            geno[snp_id][sample_name][genotype] = pheno[sample_name]
         else:
             pass
         count_num_snp += 1
         i_num_snp += 1
 
 
def save_geno(vcf):
 
     for g in open(vcf,'r'):
 
         g_mes = g.replace('\n','').split('\t')
         if g.startswith('##'):
             pass
         elif g.startswith('#CHROM'):
             num_header = len(g_mes)
             save_header(num_header,g_mes)
         else:
             snp_id = '_'.join(g_mes[0:5])
             ref = g_mes[3]
             alt = g_mes[4]
             save_snp(num_header,ref,alt,snp_id,g_mes)
 
  
def save_ttest():
 
     for k in geno.keys():
         for k2 in geno[k]:
             hap = ''.join(geno[k][k2])
             dict_id = k
             pheno_value = geno[k][k2][hap]
             if dict_id not in sig:
                 sig[dict_id] = {}
                 sig[dict_id][hap] = []
                 sig[dict_id][hap].append(pheno_value)
             elif dict_id in sig:
                 if hap not in sig[dict_id]:
                     sig[dict_id][hap] = []
                     sig[dict_id][hap].append(pheno_value)
                 else:
                     sig[dict_id][hap].append(pheno_value)            
 
def caculate_ttest():
 
     for s in sig.keys():
              x = [y for y in sig[s]]
              if len(x) > 1:
                  h1 = x[0]
                  h2 = x[1]
                  h1_list = [float(i) for i in sig[s][h1] if i != 'NaN']
                  h2_list = [float(i) for i in sig[s][h2] if i != 'NaN']
                  a = np.array(h1_list)
                  b = np.array(h2_list)
                  t,p = stats.ttest_ind(a,b)
                  a_mean = np.mean(h1_list)
                  b_mean = np.mean(h2_list)
                  print(s,h1,a_mean,h2,b_mean,p,sep = '\t')
  
             
save_trait(trait)
save_geno(vcf)
save_ttest()
caculate_ttest()

