#!/usr/bin/env python3

#System modules
import sys
import time


#Package modules
from genome import Genome
from lookupRegion import LookupRegion
from precursors import Precursors

#Timing script
start_time = time.time()

#Declaring inputs
gff=sys.argv[1]
precursors=sys.argv[2]

class Main:

	def __init__(self,gffFile):
		print("Started parsing genome annotation")
		self.genome=Genome(gffFile)
		self.node=self.genome.node

		print("Finished parsing genome annotation")

	
	def generate_gene_graph(self,close=True):
		#Generate the genome graph
		nodesFile="nodes.tsv"	
		edgeFile="edges.tsv"
		writeNode=open(nodesFile,"w")
		writeEdge=open(edgeFile,"w")
		
		#Write headers#
		writeNode.write("id\tLabel\tType\tType Code\n")
		writeEdge.write("Source\tTarget\n")


		for seqname in self.genome.genome:
			for geneIndex in range(0,len(self.genome.genome[seqname])-1):
				geneList=self.genome.genome[seqname]
				
				node=str(geneList[geneIndex].gene['id'])+"\t"+geneList[geneIndex].gene['name']+"\tGene\t1\n"
				writeNode.write(node)
				
				edge=str(geneList[geneIndex].gene['id'])+"\t"+str(geneList[geneIndex+1].gene['id'])+"\n"
				writeEdge.write(edge)

			writeNode.flush()
			writeEdge.flush()

		writeNode.flush()
		writeEdge.flush()
		if close:	
			writeNode.close()
			writeEdge.close()
		else:
			return [writeNode,writeEdge]

	def generate_gene_n_precursor_graph(self,precursorsFile,close=True):
		#Runs generate_gene_graph and adds the current number to star listing precursors as nodes.
		#Searches for surrounding gene and adds edges to them if in gene adds three edges

		self.precursors=Precursors(precursorsFile).precursors
		writeNode,writeEdge=self.generate_gene_graph(close=False)
		for precursor in self.precursors:
			if precursor.name.startswith("mir"):
				type_="pre_Conserved"
				type_code=2
			else:
				type_="pre_Novel"
				type_code=3	
			node="%s\t%s\t%s\t%s\n" %(precursor.id+self.genome.node,precursor.name,type_,type_code)
			writeNode.write(node)
			surrounding_genes=LookupRegion(self.genome,precursor.region).get_surrounding_genes()
			print(surrounding_genes)
			for gene in surrounding_genes:
				print(gene)
				if gene is not None:
					edge="%s\t%s\n" %(precursor.id+self.genome.node,gene.gene['id']) 
					writeEdge.write(edge)	

			writeNode.flush()
			writeEdge.flush()
		if close:	
			writeNode.close()
			writeEdge.close()
		else:
			return [writeNode,writeEdge]	

#(gene        	 282167 	 289354)
#print(Genome(gff).isInsideGene(('scaffold_449',289356,289359)))
#print(Genome(gff).getDownstreamGene(('scaffold_449',289356,289359)))
#print(Genome(gff).getUpstreamGene(('scaffold_449',289356,289359)))
#print(Genome(gff).isAcrossRightGeneBoundry(('scaffold_449',289356,289359),False))
#print(Genome(gff).isAcrossGeneBoundries(('scaffold_449',289356,289359)))
#print(Genome(gff).stats())

Main(gff).generate_gene_n_precursor_graph(precursors)

#print([ LookupRegion(genome,precursor.region).is_inside_gene() for precursor in Precursors(precursors).precursors])
#lookupRegion=LookupRegion(genome,preRegion)
#print(lookupRegion.is_inside_gene())
#print(lookupRegion.is_across_gene_boundries())
#print(lookupRegion.get_surrounding_genes())



print("--- %s seconds ---" % (time.time() - start_time))