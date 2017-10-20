#!/usr/bin/env python3

#
# Created by Bruno Costa @ITQB 
# 19/10/2017
#
# Lookup functions to identify region in genome
#

class Precursors:
	#Collection of precursor 
	def __init__(self,precursorsFile):
	#Constructor for precursors, parses the precursors file
		precursors=open(precursorsFile,"r").readlines()
		self.precursors=[ Precursor(precursors[index].strip().split("\t"),index) for index in range(1,len(precursors)-1) ]

	def pop(self):
		return self.precursors.pop()

class Precursor:
	def __init__(self,precursorLine,id_):
	#Transform a precursor line into a precursor object	
		self.miRseq=precursorLine[0]                  	 
		self.abundance=precursorLine[1]   	 
		self.seqname=precursorLine[2]                         	 
		self.start=int(precursorLine[3].strip())   	 
		self.end=int(precursorLine[4].strip())     	 
		self.name=precursorLine[5]
		self.region=(self.seqname,self.start,self.end)
		self.miR=(self.miRseq,self.abundance)
		self.id=id_