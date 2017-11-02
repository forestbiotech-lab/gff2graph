#!/usr/bin/env python3

#
# Created by Bruno Costa @ITQB
# 25/10/2017
#
# Parse psRNAtarget files
#
#


class Targets:

    def __init__(self, targetsFile):
        targets = open(targetsFile, "r").readlines()
        self.targets = [Target(targets[index].strip().split("\t"), index)
                        for index in range(2, len(targets))]
        
    def add_mapping(self,sam):
    		# sam is a sam object that contains mappings     
        # organize them by seqname
        # Important for transcripts. 
        # If the targets are directly mapped to the genome this is not necessary
        # Some other function should be implemented so that they are arranged by seq name if Target_acc is genome seqname
        
        self.mappedWithAnnotation=dict()
        for target in self.targets:
        	try:
        		#Retrieve the mapping for the target
        		mapping=sam.est[target.target_Acc]
        		if mapping.RNAME is not "*":
        		#is it mapped to genome
        			if mapping.gene is not None: 
        			#if mapping is in gene
        				target.mapping=mapping
	        			try:
		        			self.mappedWithAnnotation[mapping.RNAME].append(target)
		        		except KeyError:
		        			self.mappedWithAnnotation[mapping.RNAME]=[target]
        	except KeyError:
        		print(target.target_Acc+"doesn't exist")
        # self.miRNA=MiRNA(self.precursors).get()



class Target:

    def __init__(self,targetLine,id_):
        self.miRNA_Acc = targetLine[0]   									# This is the miRNA sequence
        self.target_Acc = targetLine[1]  									# This is the target accession
        self.expectation = targetLine[2]									# Score? lower better Must check
        self.UPE = targetLine[3]													# Energy
        self.miRNA_start = targetLine[4]									#
        self.miRNA_end = targetLine[5]										#
        self.target_start = targetLine[6]									#
        self.target_end = targetLine[7]										#
        self.miRNA_aligned_fragment = targetLine[8]				#
        self.target_aligned_fragment = targetLine[9]			# 
        self.inhibition = targetLine[10]									# Type of inhibition: Cleavage or Inhibition
        self.target_Desc = targetLine[11]									#
        self.multiplicity = targetLine[12]								# This would be the abundance it seq aren't collapsed
        self.id=id_
        self.mapping=None 																# This is the mapping
        self.miRseq=self.miRNA_Acc											# This is the miRNA sequence. Unifies naming throughout classes 