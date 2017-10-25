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
                        for index in range(2, len(targets) - 1)]
        
    def add_mapping(self,sam):
    		# sam is a sam object that contains mappings     
        # organize them by seqname
        # Important for transcripts. 
        # If the targets are directly mapped to the genome this is not necessary
        # Some other function should be implemented so that they are arranged by seq name if Target_acc is genome seqname
        
        self.mapped=dict()
        for target in self.targets:
        	try:
        		#Retrieve the mapping for the target
        		mapping=sam.est[target.target_Acc]
        		#is it mapped to genome
        		if mapping.RNAME is not "*":
        			try:
	        			self.mapped[mapping.RNAME].append((target,mapping))
	        		except KeyError:
	        			self.mapped[mapping.RNAME]=[(target,mapping)]
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
