#!/usr/bin/env python3

#Package modules
from featureLine import FeatureLine
from gene import Gene


class Genome:
	
	def __init__(self,gffFile):
		#See gff http://www.ensembl.org/info/website/upload/gff.html

		gff=open(gffFile,"r")
		features=[FeatureLine(gffLine.strip().split("\t")) for gffLine in gff.readlines() if not gffLine.startswith("#") ]
		self.genome=dict()
		self.node=0
		for featureLine in features:
			seqname=featureLine.seqname()
			if featureLine.feature() == "gene":
				self.node+=1
				gene=Gene(featureLine,self.node)
				try:
					#Attempt to get gene list
					geneList=self.genome[seqname]
					geneList.append(gene)
					self.genome[seqname]=geneList
				except KeyError: 
					#Start genelist
					self.genome[seqname]=[gene]

	def get_genome(self):	
		print(self.genome)

	def stats(self):
		#Generates the statistics for the genome. Tuple with seqname and respective number of genes.
		return [(seqname,len(self.genome[seqname])) for seqname in self.genome ]


		
