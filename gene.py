#!/usr/bin/env python3

class Gene:
	def __init__(self,FeatureLine,id_):
	#Starts a gene object
		fl=FeatureLine.get()
		self.gene=dict([["name",fl["attribute"]],
			["start",int(fl["start"])],
			["end",int(fl["end"])],
			["exons",[]],
			["introns",[]],
			["cds",[]],
			["start_codon",[]],
			["stop_codon",[]],
			["score",fl["score"]],
			["frame",fl["frame"]],
			["strand",fl["strand"]],
			["id",id_]
			])
	
		self.name=self.gene["name"]	
		self.start=self.gene["start"]
		self.end=self.gene["end"]

	def get(self):
		return self.gene
	def name(self):
		return self.gene["name"]
	def start(self):
		return self.gene["start"]
	def end(self):
		return self.gene["end"]
	def addExon(self,featureLine):
		name=""

class Exon:
	#Not implemented
	def __init__(self,featureLine):
		name=""

