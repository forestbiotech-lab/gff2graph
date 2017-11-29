#! /usr/bin/env python3

#Bruno Costa INESC
#Get what I understand is splice sites

import sys
from featureLine import FeatureLine


gtf=sys.argv[1]
gtf=open(gtf,"r")

previousLine=""
previousFLexon=None
previousFLcds=None
count=0
for line in gtf:
	count+=1
	if line.startswith("#"):
		continue
	try:
		fl=FeatureLine(line,False)
	except:
		print(count,file=sys.stderr)
	if fl.feature()=="CDS":
		previousLine="CDS"
		previousFLcds=fl
		continue

	if fl.feature()=="exon":
		if previousLine=="exon":
			#This is when there is another reading-frame for the exons
			if previousFLexon.end()==previousFLcds.end():
				previousFLexon=fl
				previousLine="CDS"
				continue
			else:
				output=fl.seqname()+"\t"+str(previousFLexon.end())+"\t"+str(fl.start())+"\t"+fl.featureLine['strand']
				print(output)
				previousFLexon=fl
				continue
		else:
			previousLine="exon"
			previousFLexon=fl
			continue
				

