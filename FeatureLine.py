#!/usr/bin/env python3
class FeatureLine:
	def __init__(self,gffLine):
	#Converts a gff featureLine into a named dictionary object
		self.featureLine=dict([["seqname",gffLine[0].strip()], # name of the chromosome or scaffold; chromosome names can be given with or without the 'chr' prefix. Important note: the seqname must be one used within Ensembl, i.e. a standard chromosome name or an Ensembl identifier such as a scaffold ID, without any additional content such as species or assembly. See the example GFF output below.
		["source",gffLine[1].strip()], # name of the program that generated this feature, or the data source (database or project name)
		["feature",gffLine[2].strip()], # feature type name, e.g. Gene, Variation, Similarity
		["start",int(gffLine[3].strip())], # Start position of the feature, with sequence numbering starting at 1.
		["end",int(gffLine[4].strip())], # End position of the feature, with sequence numbering starting at 1.
		["score",gffLine[5].strip()], # A floating point value.
		["strand",gffLine[6].strip()], # defined as + (forward) or - (reverse).
		["frame",gffLine[7].strip()], # One of '0', '1' or '2'. '0' indicates that the first base of the feature is the first base of a codon, '1' that the second base is the first base of a codon, and so on..
		["attribute",gffLine[8].strip()] # A semicolon-separated list of tag-value pairs, providing additional information about each feature.		
		])
	def feature(self):
		return self.featureLine["feature"]
	def seqname(self):
		return self.featureLine["seqname"]	
	def get(self):
		return self.featureLine	