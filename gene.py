#!/usr/bin/env python3

class Gene:
	def __init__(self,FeatureLine,id_):
	#Starts a gene object
		fl=FeatureLine.get()
		#This dictionary of futile change this to variables instead. Or is it better to store this way.
		self.gene=dict([["name",fl["attribute"]], 		#GFF
			["start",int(fl["start"])],   				#GFF						
			["end",int(fl["end"])],		  				#GFF				
			["exons",[]],				  				#GFF		
			["introns",[]],				  				#GFF		
			["cds",[]],					  				#GFF	
			["start_codon",[]],			  				#GFF			
			["stop_codon",[]], 			  				#GFF			           
			["score",fl["score"]],        				#GFF
			["frame",fl["frame"]],		  				#GFF	
			["strand",fl["strand"]],	  				#GFF	
			["id",id_],					  				#NODE - The unique node id - For gephi	
			["upstream",None],			  				#EDGE - The upstream gene object neighbour	
			["downstream", None],         				#EDGE - The downstream gene object neighbour
			["hasPrecursor",[]],          				#EDGE - The precursor object    
			["targeted",[]],             			    #EDGE - The miRNAs that target it
			["acc",None]                 			    #This is the EST accession
			])
	
		self.name=self.gene["name"]	
		self.start=self.gene["start"]
		self.end=self.gene["end"]
		self.targeted=self.gene["targeted"]

	def get(self):
		return self.gene
	def addExon(self,featureLine):
		name=""

class Exon:
	#Not implemented
	def __init__(self,featureLine):
		name=""

