#!/usr/bin/env python3

#
# Created by Bruno Costa @ITQB 
# 19/10/2017
#
# Extracts the mappings from sam file. 
# Didn't use pysam because of dependency hell
# Needed to upgrade python3 to 3.6
# And possibly the whole operating system to support the load of dependencies
#


class Sam:
	def __init__(self,samFile):
		self.sam=dict()
		self.est=dict()
		self.sam['*']=[] #Save unmapped for some reason yet to be determined for now
		for samLine in open(samFile,"r").readlines():
			samLine=samLine.strip().split('\t')
			if samLine[0].startswith("@"):
				if samLine[0].startswith("@SQ") and samLine[1].startswith("SN:"):
				#Get the mapped sequences names
					sn=samLine[1].split(":")[1]	
					self.sam[sn]=[]
			else:
				mapping=Mapping(samLine)
				self.sam[mapping.RNAME].append(mapping)
				self.est[mapping.QNAME]=mapping      	#Each accession should only have one mapping or else they will be overwritten

class Mapping:
	def __init__(self,mappingLine):
		self.QNAME=mappingLine[0] 	# String [!-?A-~]{1,254} Query template NAME
		self.FLAG=mappingLine[1] 		# Int [0,216-1] bitwise FLAG
		self.RNAME=mappingLine[2] 	# String \*|[!-()+-<>-~][!-~]* Reference sequence NAME
		self.POS=int(mappingLine[3]) 		# Int [0,231-1] 1-based leftmost mapping POSition
		self.MAPQ=mappingLine[4] 		# Int [0,28-1] MAPping Quality
		self.CIGAR=mappingLine[5] 	# String \*|([0-9]+[MIDNSHPX=])+ CIGAR string
		self.RNEXT=mappingLine[6] 	# String \*|=|[!-()+-<>-~][!-~]* Ref. name of the mate/next read
		self.PNEXT=mappingLine[7] 	# Int [0,231-1] Position of the mate/next read
		self.TLEN=mappingLine[8] 		# Int [-231+1,231-1] observed Template LENgth
		self.SEQ=mappingLine[9] 		# String \*|[A-Za-z=.]+ segment SEQuence
		self.QUAL=mappingLine[10] 		# String [!-~]+ ASCII of Phred-scaled base QUALity+33		
		self.region=(self.RNAME,self.POS,self.POS+len(self.SEQ))

