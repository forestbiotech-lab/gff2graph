# gff2graph
Transform a sorted .gff (genome feature file) into a graph with genes connected to their neighbour upstream gene  

The main file is genGraph.py 

	To run
	./genGraph.py [gff] [precursors] [samfile] [targetFile]

Classes described bellow

----------------------------------------------------------

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
