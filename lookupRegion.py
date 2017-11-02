#!/usr/bin/env python3

#
# Created by Bruno Costa @ITQB 
# 19/10/2017
#
# Lookup functions to identify region in genome
#

class LookupRegion:
	#Lookup function to identify regions in genome

	def __init__(self,genome,region):
		#Loads genome and region. Checks if seqname in region exists on genome 

		self.genome=genome.genome
		self.region=region
		self.debug=False
		try:
			self.seqname=self.genome[self.region[0]]
			if self.debug:
				print("  --------")
				print("  |      |")
				print(str(self.region[1])+" "+str(self.region[2]))
		except KeyError:	
			if self.debug:
				print(region[0]+" not in genome annotation")
			self.seqname=None

	def get_surrounding_genes(self):
		#Get the downstream and upstream genes of the region
		if not self.is_across_gene_boundries() and not self.is_inside_gene():
			return [self.get_downstream_gene(),self.get_upstream_gene()]
		elif not self.is_across_gene_boundries() and self.is_inside_gene():
			return [self.get_downstream_gene(),self.get_outermost_gene(),self.get_upstream_gene()]	
		#elif self.is_across_gene_boundries:
		#	if self.is_across_left_gene_boundry() and not self.is_across_right_gene_boundry():
		#		return [self.get_downstream_gene(),,self.get_upstream_gene()]		
		#		return [None]
		#	elif: self.is_across_right_gene_boundry() and not self.is_across_left_gene_boundry():
		#		##Need to change the def to get more than one up down steam gene by choice.
		#		##return [self.get_downstream_gene(),,self.get_upstream_gene()]	
		#		return [None]
#
		else:	
			print("Not implemented - Is inside gene or is across both gene boundary")
			return [None]

	def is_inside_gene(self):
		#self.region if a tuple with start and end for a seqname (seqname,start,end)
		if self.seqname is not None:
			downstream=[ gene for gene in self.seqname if self.region[1]>gene.start and self.region[2]<gene.end ]
			return len(downstream)==1
		else:
			return False

	def get_outermost_gene(self):
		#This applies if strictly inside gene and if across one gene boundary

		if self.seqname is not None:
			if self.is_inside_gene():

				outermost_gene=[ gene for gene in self.seqname if self.region[1]>gene.start and self.region[2]<gene.end ]  #Change this variable
				if len(outermost_gene)==1:
					return outermost_gene[0]
				else:
					return None

			elif self.is_across_gene_boundries():
				if self.is_across_left_gene_boundry(multiple=False):
					#get upstream gene get u the current gene
					return self.get_upstream_gene()
				if self.is_across_right_gene_boundry(multiple=False):
					#get downstream gene get u the current gene
					return self.get_downstream_gene()

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

	def percentagem_of_region_outside_gene(self):
		if self.is_across_gene_boundries():
			regionSize=int(self.region[2])-int(self.region[1])
			if self.is_across_left_gene_boundry(multiple=False):
				#get upstream gene get u the current gene
				return round(float(( self.get_upstream_gene().start - self.region[1] )/regionSize),2)
			if self.is_across_right_gene_boundry(multiple=False):
				#get downstream gene get u the current gene
				return round(float(( self.region[2] - self.get_downstream_gene().end ) / regionSize),2)
		else:
			return -1		

	def contains_serveral_genes(self):
		#Test if self.region crossed multiple gene boundaries  
		#Not implemented or maybe it is. | Didn't test the logic
		return self.is_across_left_gene_boundry(multiple=True) or self.is_across_right_gene_boundry(multiple=True) 

	def get_downstream_gene(self):
		if self.seqname is not None:
			downstream=[ gene for gene in self.seqname if self.region[1]>gene.start and self.region[2]>gene.end ]
			##print((downstream[-1].start,downstream[-1].end))
			if len(downstream)>0:
				if self.debug:
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
				if self.debug:
					print("  --------")
					print("  |      |")
					print(str(upstream[0].start)+" "+str(upstream[0].end))
				return upstream[0]
			else:
				return None
		else:
			return None


