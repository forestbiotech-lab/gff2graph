#!/usr/bin/env python3

import sys
from Gene import Gene
from FeatureLine import FeatureLine


gff=sys.argv[1]
precursors=open(sys.argv[2],"r")



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

	def getGenome(self):	
		print(self.genome)
	
	def stats(self):
		#Generates the statistics for the genome. Tuple with seqname and respective number of genes.
		return [(seqname,len(self.genome[seqname])) for seqname in self.genome ]

	def genGraph(self):
		#Generate the genome graph
		nodesFile="nodes.tsv"	
		edgeFile="edges.tsv"
		writeNode=open(nodesFile,"w")
		writeEdge=open(edgeFile,"w")
		
		#Write headers#
		writeNode.write("id\tLabel\n")
		writeEdge.write("Source\tTarget\n")


		for seqname in self.genome:
			for geneIndex in range(0,len(self.genome[seqname])-1):
				geneList=self.genome[seqname]
				node=str(geneList[geneIndex].gene['id'])+"\t"+geneList[geneIndex].gene['name']+"\n"
				writeNode.write(node)
				edge=str(geneList[geneIndex].gene['id'])+"\t"+str(geneList[geneIndex+1].gene['id'])+"\n"
				writeEdge.write(edge)
			writeNode.flush()
			writeEdge.flush()

		writeNode.flush()
		writeEdge.flush()
		writeNode.close()
		writeEdge.close()
		
	def getSurroundingGenes(self,region):
		#region if a tuple with start and end for a seqname (seqname,start,end)
		seqname=self.genome[region[0]]
		print(region[1])
		downstream=[ gene for gene in seqname if region[1]>gene.start() and region[2]>gene.start() ]
		print([gene.start() for gene in downstream])

	def isInsideGene(self,region):
		#region if a tuple with start and end for a seqname (seqname,start,end)
		seqname=self.genome[region[0]]
		downstream=[ gene for gene in seqname if region[1]>gene.start() and region[2]<gene.end() ]
		return len(downstream)==1

	def isAcrossGeneBoundries(self,region):
		#Check if region is across gene 1 boundary
		return self.isAcrossLeftGeneBoundry(region,multiple=False) or self.isAcrossRightGeneBoundry(region,multiple=False)
		
	def isAcrossLeftGeneBoundry(self,region,multiple):
		seqname=self.genome[region[0]]
		acrossBoundry=[ gene for gene in seqname if region[1]<gene.start() and region[2]>gene.start() and region[2]<gene.end() ]
		if multiple:
			return len(acrossBoundry)>1
		else:	
			return len(acrossBoundry)==1

	def isAcrossRightGeneBoundry(self,region,multiple):
		seqname=self.genome[region[0]]
		acrossBoundry=[ gene for gene in seqname if region[1]>gene.start() and region[1]<gene.end() and region[2]>gene.end() ]
		if multiple:
			return len(acrossBoundry)>1
		else:	
			return len(acrossBoundry)==1

	def containsServeralGenes(self,region):
		#Test if region crossed multiple gene boundaries  
		#Not implemented or maybe it is. | Didn't test the logic
		return self.isAcrossLeftGeneBoundry(self,region,multiple=True) or self.isAcrossRightGeneBoundry(self,region,multiple=True) 

	def getDownstreamGene(self,region):
		seqname=self.genome[region[0]]
		print("  --------")
		print("  |      |")
		print(str(region[1])+" "+str(region[2]))
		downstream=[ gene for gene in seqname if region[1]>gene.start() and region[2]>gene.end() ]
		##print((downstream[-1].start(),downstream[-1].end()))
		if len(downstream)>0:
			return downstream[-1]
		else: 
			return []
	
	def getUpstreamGene(self,region):	
		seqname=self.genome[region[0]]
		print("  --------")
		print("  |      |")
		print(str(region[1])+" "+str(region[2]))
		upstream=[ gene for gene in seqname if region[1]<gene.start() and region[2]<gene.end() ]
		#print((upstream[0].start(),upstream[0].end()))
		if len(upstream)>0:
			return upstream[0]
		else:
			return []


class Exon:
	def __init__(self,featureLine):
		name=""

#(gene        	 282167 	 289354)
#print(Genome(gff).isInsideGene(('scaffold_449',289356,289359)))
#print(Genome(gff).getDownstreamGene(('scaffold_449',289356,289359)))
#print(Genome(gff).getUpstreamGene(('scaffold_449',289356,289359)))
#print(Genome(gff).isAcrossRightGeneBoundry(('scaffold_449',289356,289359),False))
#print(Genome(gff).isAcrossGeneBoundries(('scaffold_449',289356,289359)))

print(Genome(gff).genGraph())
print(Genome(gff).stats())



