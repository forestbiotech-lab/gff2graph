#!/usr/bin/env python3

class Gene:
	def __init__(self,FeatureLine,id):
	#Starts a gene object
		fl=FeatureLine.get()
		self.gene=dict([["name",fl["attribute"]],
			["start",fl["start"]],
			["end",fl["end"]],
			["exons",[]],
			["introns",[]],
			["cds",[]],
			["start_codon",[]],
			["stop_codon",[]],
			["score",fl["score"]],
			["frame",fl["frame"]],
			["strand",fl["strand"]],
			["id",id]
			])
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