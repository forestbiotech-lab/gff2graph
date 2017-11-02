#!/usr/bin/env python3

#
# Created by Bruno Costa @ITQB 
# 19/10/2017
#
# The attributes of a precursor witch is by extension the miRNA entity
#

class Precursors:
	#Collection of precursor 
	def __init__(self,precursorsFile):
	#Constructor for precursors, parses the precursors file
	#O(2P)
		precursors=open(precursorsFile,"r").readlines()
		self.precursors=[ Precursor(precursors[index].strip().split("\t"),index) for index in range(1,len(precursors)) ]
		#organize them by miRNAs
		self.miRNA=MiRNA(self.precursors).get()
	def pop(self):
		return self.precursors.pop()

class MiRNA:
	def __init__(self,precursors):
		self.miRNA=dict()
		for precursor in precursors:
			self.miRNA[precursor.miRseq]=precursor
	def get(self):
		return self.miRNA	


class Precursor:
	def __init__(self,precursorLine,id_):
	#Transform a precursor line into a precursor object	
		self.miRseq=precursorLine[0]                  	 		#miRNA sequence
		self.abundance=precursorLine[1]   	 					#miRNA abundance 
		self.seqname=precursorLine[2]                         	#Genome seqname 
		self.start=int(precursorLine[3].strip())   	 			#Precursor start Coordinates
		self.end=int(precursorLine[4].strip())     	            #Precursor end Coordinates
		self.name=precursorLine[5]								#Precursor unique name 
		self.region=(self.seqname,self.start,self.end)			#Tuple (seqname,start,end)
		self.miR=(self.miRseq,self.abundance)					#NODE - miRNA Name novXXX, miRXXX
		self.id=id_ 											#NODE - Id
		self.geneNeighbours=[]								 	#EDGES - Neighbours Gene object
		self.gene=None 											#EDGES - Contained in Gene object
		self.target=None 										#EDGES - Targeted gene for regulation
