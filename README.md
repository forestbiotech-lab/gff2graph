# gff2graph
Transform a sorted .gff (genome feature file) into a graph with genes connected to their neighbour upstream gene  

The main file is genGraph.py 

	To run
	./genGraph.py [gff] [precursors] [samfile] [targetFile]


Classes described below.

Save as graph-tools format (xml). Requires the nodes.tsv and edge.tsv to be in the same folder. (Sorry this is hard-coded for now):
	
	./saveGraph.py 


The exploreGraph.py file provides the methods to load the xml graph. (Requires graph-tools to be installed on your system.)
It also provides several functions to process the graph. Generate the degree distribution. Functions to print specific components. List the number of components.
To do so import exploreGraph into your project and use the function to explore the graphs. 
Documentation for this file is limited to the comments around the functions.

--------------------------------------------------------------------------------------------------------

Gene
====

|Attribute 		| Definition 									|
|---------------|-----------------------------------------------|
|start			| GFF											|
|name 			| GFF											|
|end			| GFF											|
|exons			| GFF											|
|introns		| GFF											|
|cds			| GFF											|
|start	 		| GFF											|
|stop	  		| GFF			           						|
|score	       	| GFF											|
|frame		  	| GFF											|
|strand		  	| GFF											|
|id				| NODE - The unique node id - For gephi			|
|upstream		| EDGE - The upstream gene object neighbour		|
|downstream	  	| EDGE - The downstream gene object neighbour	|
|has	        | EDGE - The precursor object    				|
|targeted	   	| EDGE - The miRNAs that target it				|
|acc	        | This is the EST accession						|

Target
======

| Attribute 					| Definition 													|
|-------------------------------|---------------------------------------------------------------|
| miRNA_Acc   					| This is the miRNA sequence									|
| target_Acc  					| This is the target accession									|
| expectation					| Score? lower better Must check								|
| UPE							| Energy														|
| miRNA_start					|																|
| miRNA_end						|																|
| target_start					|																|
| target_end					|																|
| miRNA_aligned_fragment		|																|
| target_aligned_fragment		| 																|
| inhibition					| Type of inhibition: Cleavage or inhibition					|
| target_Desc					|																|
| multiplicity					| This would be the abundance it seq aren't collapsed			|
| id 							|   -															|
| mapping						| This is the mapping											|
| miRseq						| This is the miRNA sequence. Unifies naming throughout classes |

Precursor
=========

|Attribute 			| 	Definition 								|
|-------------------|-------------------------------------------|
|miRseq		        |	miRNA sequence							|
|abundance			|	miRNA abundance 						|
|seqname			|	Genome seqname 							|
|start			   	|	Precursor start Coordinates				|
|end			    |	Precursor end Coordinates				|
|name				|	Precursor unique name 					|
|region				|	Tuple (seqname,start,end)				|
|miR				|	NODE - miRNA Name novXXX, miRXXX		|
|id					|	NODE - Id								|
|geneNeighbours		|	EDGES - Neighbours Gene object			|
|gene				|	EDGES - Contained in Gene object		|
|target				|	EDGES - Targeted gene for regulation	|


Mapping
=======

|Attribute 	| Definition 											|
|-----------|-------------------------------------------------------|
| QNAME		| String [!-?A-~]{1,254} Query template NAME			|
| FLAG		| Int [0,216-1] bitwise FLAG							|
| RNAME		| String \*|[!-()+-<>-~][!-~]* Reference sequence NAME	|
| POS		| Int [0,231-1] 1-based leftmost mapping POSition		|
| MAPQ		| Int [0,28-1] MAPping Quality							|
| CIGAR		| String \*|([0-9]+[MIDNSHPX=])+ CIGAR string			|
| RNEXT		| String \*|=|[!-()+-<>-~][!-~]* Ref. name of the mate/next read	|
| PNEXT		| Int [0,231-1] Position of the mate/next read			|
| TLEN		| Int [-231+1,231-1] observed Template LENgth			|
| SEQ		| String \*|[A-Za-z=.]+ segment SEQuence				|
| QUAL		| String [!-~]+ ASCII of Phred-scaled base QUALity+33	|
| region	|  -													|	
| gene		| Gene object used to filter targets based on existence of gene annotation on genome	|




	--------------------------------------------------------



genGraph.py:    def __init__(self, gffFile):
genGraph.py-        #Constructor function starts by building genome

genGraph.py:    def generate_gene_graph(self, close=True):
genGraph.py-        # Generate the genome graph

genGraph.py:    def generate_gene_n_precursor_graph(self, precursorsFile, close=True):
genGraph.py-        # Runs generate_gene_graph and adds the current number to star listing precursors as nodes.

genGraph.py:    def generate_g_p_n_target_graph(self,precursorsFile,samFile,targetFile):
genGraph.py-        #Runs other graph generators and add targets

genGraph.py:    def add_gene_annotations_to_mappings(self,sam):
genGraph.py-        #Checks if mapping belongs to any gene annotation and adds it.

genGraph.py:    def stats(self):
genGraph.py-    #Prints stats already calculated for graphs

----------------------------------------------------------

featureLine.py:	def __init__(self,gffLine):
featureLine.py-	#Converts a gff featureLine into a named dictionary object

featureLine.py:		["strand",gffLine[6].strip()], # defined as + (forward) or - (reverse).
featureLine.py-		["frame",gffLine[7].strip()], # One of '0', '1' or '2'. '0' indicates that the first base of the feature is the first base of a codon, '1' that the second base is the first base of a codon, and so on..

featureLine.py:	def feature(self):
featureLine.py-		return self.featureLine["feature"]
featureLine.py:	def seqname(self):
featureLine.py-		return self.featureLine["seqname"]	
featureLine.py:	def get(self):
featureLine.py-		return self.featureLine	

--------------------------------------------------------

gene.py:	def __init__(self,FeatureLine,id_):
gene.py-	#Starts a gene object

gene.py:	def get(self):
gene.py-		return self.gene
gene.py:	def addExon(self,featureLine):
gene.py-		name=""

gene.py:	def __init__(self,featureLine):
gene.py-		name=""


-------------------------------------------------------------

genome.py:	def __init__(self,gffFile):
genome.py-		#See gff http://www.ensembl.org/info/website/upload/gff.html

genome.py:	def get_genome(self):	
genome.py-		print(self.genome)

genome.py:	def stats(self):
genome.py-		#Generates the statistics for the genome. Tuple with seqname and respective number of genes.

---------------------------------------------------------------

lookupRegion.py:	def __init__(self,genome,region):
lookupRegion.py-		#Loads genome and region. Checks if seqname in region exists on genome 

lookupRegion.py:	def get_surrounding_genes(self):
lookupRegion.py-		#Get the downstream and upstream genes of the region

lookupRegion.py:		#		##Need to change the def to get more than one up down steam gene by choice.
lookupRegion.py-		#		##return [self.get_downstream_gene(),,self.get_upstream_gene()]	

lookupRegion.py:	def is_inside_gene(self):
lookupRegion.py-		#self.region if a tuple with start and end for a seqname (seqname,start,end)

lookupRegion.py:	def get_outermost_gene(self):
lookupRegion.py-		#This applies if strictly inside gene and if across one gene boundary

lookupRegion.py:	def is_across_left_gene_boundry(self,multiple):
lookupRegion.py-		#Check if region crosses a left gene boundary	

lookupRegion.py:	def is_across_right_gene_boundry(self,multiple):
lookupRegion.py-		#Check if region crosses a right gene boundary	

lookupRegion.py:	def is_across_gene_boundries(self):
lookupRegion.py-		#Check if self.region is across gene 1 boundary

lookupRegion.py:	def percentagem_of_region_outside_gene(self):
lookupRegion.py-		if self.is_across_gene_boundries():

lookupRegion.py:	def contains_serveral_genes(self):
lookupRegion.py-		#Test if self.region crossed multiple gene boundaries  

lookupRegion.py:	def get_downstream_gene(self):
lookupRegion.py-		if self.seqname is not None:

lookupRegion.py:	def get_upstream_gene(self):	
lookupRegion.py-		if self.seqname is not None:

--------------------------------------------------------------

mapping.py:	def __init__(self,samFile):
mapping.py-		self.sam=dict()

mapping.py:	def __init__(self,mappingLine):
mapping.py-		self.QNAME=mappingLine[0] 	# String [!-?A-~]{1,254} Query template NAME

-----------------------------------------------------

precursors.py:	def __init__(self,precursorsFile):
precursors.py-	#Constructor for precursors, parses the precursors file

precursors.py:	def pop(self):
precursors.py-		return self.precursors.pop()

precursors.py:	def __init__(self,precursors):
precursors.py-		self.miRNA=dict()

precursors.py:	def get(self):
precursors.py-		return self.miRNA	

precursors.py:	def __init__(self,precursorLine,id_):
precursors.py-	#Transform a precursor line into a precursor object	

--------------------------------------------------------

target.py:    def __init__(self, targetsFile):
target.py-        targets = open(targetsFile, "r").readlines()

target.py:    def add_mapping(self,sam):
target.py-    		# sam is a sam object that contains mappings     

target.py:    def __init__(self,targetLine,id_):
target.py-        self.miRNA_Acc = targetLine[0]   								# This is the miRNA sequence
