#!/usr/bin/env python3

#
# Created by Bruno Costa @INESC 2017
# Description: This is the main file used to generated gephi graph input files from 
#              Genome annotation mapping and sRNA data.
#
# Call: ./gemgraph.py [gff_file] [precursors] [samFile] [targetFile]
#
#          Precursors come from miRPursuit
#          sam file mapping of transcriptome on genome
#          targetFile from psRNAtarget 
#
#

##Imports
# System modules
import sys
import time

# Package modules
from genome import Genome
from lookupRegion import LookupRegion
from precursors import Precursors
from mapping import Sam
from target import Targets

# Timing script
start_time = time.time()

# Declaring inputs
gff = sys.argv[1]
precursors = sys.argv[2]
samFile = sys.argv[3]
targetFile = sys.argv[4]


class Main:

    def __init__(self, gffFile):
        #Constructor function starts by building genome

        print("Started parsing genome annotation")
        self.genome = Genome(gffFile)
        self.node = self.genome.node
        print("Finished parsing genome annotation")

    def generate_gene_graph(self, close=True):
        # Generate the genome graph
        nodesFile = "nodes.tsv"
        edgeFile = "edges.tsv"
        writeNode = open(nodesFile, "w")
        writeEdge = open(edgeFile, "w")

        #Write headers#
        writeNode.write("id\tLabel\tType\tType Code\n")
        writeEdge.write("Source\tTarget\tType\tType Code\n")

        # !!!!!!!!!!!!Start building edges in genes here    
        for seqname in self.genome.genome:
            geneList = self.genome.genome[seqname]
            for geneIndex in range(0, len(self.genome.genome[seqname])-1):

                node = str(geneList[geneIndex].gene['id']) + "\t" + \
                    geneList[geneIndex].gene['name'] + "\tGene\t1\n"
                writeNode.write(node)

                edge = str(geneList[geneIndex].gene['id']) + "\t" + \
                    str(geneList[geneIndex + 1].gene['id']) + "\tGene Neighbour\t0\n"
                writeEdge.write(edge)
            #adding the last gene node
            node = str(geneList[len(self.genome.genome[seqname])-1].gene['id']) + "\t" + \
                geneList[len(self.genome.genome[seqname])-1].gene['name'] + "\tGene\t1\n"
            writeNode.write(node)

            writeNode.flush()
            writeEdge.flush()

        writeNode.flush()
        writeEdge.flush()
        if close:
            writeNode.close()
            writeEdge.close()
        else:
            return [writeNode, writeEdge]

    def generate_gene_n_precursor_graph(self, precursorsFile, close=True):
        # Runs generate_gene_graph and adds the current number to star listing precursors as nodes.
        # Updated precursor.id to account for nodes in genome
        # Searches for surrounding gene and adds edges to them if in gene adds
        # three edges

        self.precursors = Precursors(precursorsFile)
        writeNode, writeEdge = self.generate_gene_graph(close=False)
        self.edges_3=0  #Have 3 edges (Might be pointing to none though)
        self.edges_2=0  #Have 2 edges
        self.egdes_1=0  #Have 1 edges (This means scaffold/contig doesn't have annotation, for now.)
        nodeCount=0
        for precursor in self.precursors.precursors:
            if precursor.name.startswith("mir"):
                type_ = "pre_Conserved"
                type_code = 2
            else:
                type_ = "pre_Novel"
                type_code = 3
            precursor.id+=self.genome.node
            node = "%s\t%s\t%s\t%s\n" % (
                precursor.id, precursor.name, type_, type_code)
            writeNode.write(node)
            nodeCount+=1
            surrounding_genes = LookupRegion(
                self.genome, precursor.region).get_surrounding_genes()
            if len(surrounding_genes)==3:
                self.edges_3+=1
            if len(surrounding_genes)==2:
                self.edges_2+=1
            if len(surrounding_genes)==1:
                self.egdes_1+=1
            #print(surrounding_genes)
            geneCounter=0
            for gene in surrounding_genes:
                #print(gene)
                if len(surrounding_genes)==3 and geneCounter==1:
                    Type="Inside"
                    TypeCode=2
                else:
                    Type="Pre-Gene Neighbour"
                    TypeCode=1
                if gene is not None:
                    edge = "%s\t%s\t%s\t%s\n" % (
                        precursor.id, gene.gene['id'],Type,TypeCode)
                    writeEdge.write(edge)
                geneCounter+=1
            writeNode.flush()
            writeEdge.flush()
        #Sum the number of unique nodes added in this process    
        self.node+=nodeCount
        if close:
            writeNode.close()
            writeEdge.close()
        else:
            return [writeNode, writeEdge]
    

    def generate_g_p_n_target_graph(self,precursorsFile,samFile,targetFile):
        #Runs other graph generators and add targets
        #This is implemented for transcripts
        #This function only adds edges not nodes




        print("Loading .sam file")
        sam = Sam(samFile)
        print(".sam File loaded")
        print("Loading targets")
        targets = Targets(targetFile)  
        print("Targets loaded")

 

        self.add_gene_annotations_to_mappings(sam)             
        
        #Done here so est are added do node name
        writeNode, writeEdge = self.generate_gene_n_precursor_graph(precursorsFile,close=False)
        
        #Should happen after genes are added to mappings
        targets.add_mapping(sam)
        #Adds mappings to targets if they have a gene annotation

        targetWithOutPrecursor=0
        for seqname in targets.mappedWithAnnotation:
            #Go through seqnames
            for target in targets.mappedWithAnnotation[seqname]:
                #Add targeting edges to genes.
                gene=target.mapping.gene
                try:
                    #Try to add target to miRNA but for that they must have a precursor
                    miRNA=self.precursors.miRNA[target.miRseq.split("-")[0]]
                    gene.targeted=miRNA
                    edge = "%s\t%s\tTarget\t3\n" % (miRNA.id, gene.gene['id'])
                    writeEdge.write(edge)
                except:
                    targetWithOutPrecursor+=1

            writeEdge.flush()
        writeEdge.close()
        print("Number of targets without precursor: "+str(targetWithOutPrecursor))

    def add_gene_annotations_to_mappings(self,sam):
        #Checks if mapping belongs to any gene annotation and adds it.

        self.isInGene=dict([[True,0],[False,0],["across",0]])
        for seqname in sam.sam:
            for mapping in sam.sam[seqname]:
                #Initiates the lookup class
                lookup = LookupRegion(self.genome, mapping.region)

                #If mapping is inside gene or across gene boundary add the gene to the mapping  
                isInGene=lookup.is_inside_gene() or lookup.is_across_gene_boundries()
                self.isInGene[isInGene]+=1
                if isInGene:
                    gene=lookup.get_outermost_gene()
                    print(gene)
                    lookup.get_outermost_gene().gene['name']=gene.name+" "+mapping.QNAME
                    mapping.gene=gene

                #Statistics    
                if lookup.is_across_gene_boundries():
                    self.isInGene['across']+=1
                    #Make a plot with frequency per quartile
                    #print(lookup.percentagem_of_region_outside_gene())        

    def stats(self):
    #Prints stats already calculated for graphs

        print("Number of precursor mappings")
        print(" 3:"+str(self.edges_3))
        print(" 2:"+str(self.edges_2))
        print(" 1:"+str(self.egdes_1))    
        print(self.isInGene)



# print(Genome(gff).stats())



#Main(gff).generate_gene_graph()
#Main(gff).generate_gene_n_precursor_graph(precursors)
Main(gff).generate_g_p_n_target_graph(precursors,samFile,targetFile)


#Timing script
print("--- %s seconds ---" % (time.time() - start_time))
