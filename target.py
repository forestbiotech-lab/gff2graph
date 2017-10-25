#!/usr/bin/env python3

#
# Created by Bruno Costa @ITQB 
# 25/10/2017
#
# Parse psRNAtarget files
# 
#

class Targets:
	def __init__(self,targetFile):
		sefl.target[]	
	precursors=open(precursorsFile,"r").readlines()
		self.precursors=[ Precursor(precursors[index].strip().split("\t"),index) for index in range(1,len(precursors)-1) ]
		#organize them by miRNAs
		self.miRNA=MiRNA(self.precursors).get()


class Target:
	def __init__(self):	
		self.miRNA_Acc=targetLine[] 									#This is the miRNA sequence
		self.Target_Acc=targetLine[]									#This is the target accession
		self.Expectation=targetLine[]									# Score? lower better Must check
		self.UPE=targetLine[]													# Energy 
		self.miRNA_start=targetLine[]									#	
		self.miRNA_end=targetLine[]										#
		self.Target_start=targetLine[]								#
		self.Target_end=targetLine[]									#
		self.miRNA_aligned_fragment=targetLine[]			#
		self.Target_aligned_fragment=targetLine[]			# 
		self.Inhibition=targetLine[]									# Type of inhibition: Cleavage or Inhibition 
		self.Target_Desc=targetLine[]									# 
		self.Multiplicity=targetLine[]								# This would be the abundance it seq aren't collapsed	