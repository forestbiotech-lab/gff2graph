#!/usr/bin/env python3

#
# Created by Bruno Costa @ITQB 
# 19/10/2017
#
# Lookup functions to identify region in genome
#

class LookupRegion:
	def __init__(self,genome,region):
		self.genome=genome.genome
		self.region=region
		try:
			self.seqname=self.genome[self.region[0]]
			print("  --------")
			print("  |      |")
			print(str(self.region[1])+" "+str(self.region[2]))
		except KeyError:	
			print(region[0]+" not in genome annotation")
			self.seqname=None

	def get_surrounding_genes(self):
		#Get the downstream and upstream genes of the region
		if not self.is_across_gene_boundries() and not self.is_inside_gene():
			return [self.get_downstream_gene(),self.get_upstream_gene()]
		elif not self.is_across_gene_boundries() and self.is_inside_gene():
			return [self.get_downstream_gene(),self.get_outermost_gene(),self.get_upstream_gene()]	
		else:	
			print("Not implemented - Is inside gene or is across gene boundary")
			return [None]

	def is_inside_gene(self):
		#self.region if a tuple with start and end for a seqname (seqname,start,end)
		if self.seqname is not None:
			downstream=[ gene for gene in self.seqname if self.region[1]>gene.start and self.region[2]<gene.end ]
			return len(downstream)==1
		else:
			return False

	def get_outermost_gene(self):
		#self.region if a tuple with start and end for a seqname (seqname,start,end)
		if self.seqname is not None:
			downstream=[ gene for gene in self.seqname if self.region[1]>gene.start and self.region[2]<gene.end ]  #Change this variable
			if len(downstream)==1:
				return downstream[0]
			else:
				return None
		else:
			return False

	def is_across_left_gene_boundry(self,multiple):
	#Check if region crosses a left gene boundary	
		if self.seqname is None:
			return False
		else:
			acrossBoundry=[ gene for gene in self.seqname if self.region[1]<gene.start and self.region[2]>gene.start and self.region[2]<gene.end ]
			if multiple:
				return len(acrossBoundry)>1
			else:	
				return len(acrossBoundry)==1

	def is_across_right_gene_boundry(self,multiple):
	#Check if region crosses a right gene boundary	
		if self.seqname is None:
			return False
		else:
			acrossBoundry=[ gene for gene in self.seqname if self.region[1]>gene.start and self.region[1]<gene.end and self.region[2]>gene.end ]
			if multiple:
				return len(acrossBoundry)>1
			else:	
				return len(acrossBoundry)==1

	def is_across_gene_boundries(self):
		#Check if self.region is across gene 1 boundary
		return self.is_across_left_gene_boundry(multiple=False) or self.is_across_right_gene_boundry(multiple=False)

	def contains_serveral_genes(self):
		#Test if self.region crossed multiple gene boundaries  
		#Not implemented or maybe it is. | Didn't test the logic
		return self.is_across_left_gene_boundry(self,multiple=True) or self.is_across_right_gene_boundry(self,multiple=True) 

	def get_downstream_gene(self):
		if self.seqname is not None:
			downstream=[ gene for gene in self.seqname if self.region[1]>gene.start and self.region[2]>gene.end ]
			##print((downstream[-1].start,downstream[-1].end))
			if len(downstream)>0:
				print("  --------")
				print("  |      |")
				print(str(downstream[0].start)+" "+str(downstream[0].end))
				return downstream[-1]
			else: 
				return None
		else:
			return None

	def get_upstream_gene(self):	
		if self.seqname is not None:
			upstream=[ gene for gene in self.seqname if self.region[1]<gene.start and self.region[2]<gene.end ]
			#print((upstream[0].start,upstream[0].end))
			if len(upstream)>0:
				print("  --------")
				print("  |      |")
				print(str(upstream[0].start)+" "+str(upstream[0].end))
				return upstream[0]
			else:
				return None
		else:
			return None


