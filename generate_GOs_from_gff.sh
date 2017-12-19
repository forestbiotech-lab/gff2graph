#!/usr/bin/env python3

#Convert blocks into go terms
GFF="/home/source_data/2017-Qsu-corkoak-v0.2/New_Draft/Quercus_suber_draft-v.2_-annotationGFF_-_09-Nov-2017.gff"

for block in {00..15}; 
do 
  grep "Block:$block" block.tsv | awk -F "\t" '{print $3}' | grep "|" | awk -F "[:|]" '{print $2}' > block$block.tsv 
  for i in $(cat block$block.tsv | tr -s "\n" " ");do grep "$i" $GFF; done | grep mRNA | awk -F "\t" '{print $9}' | awk -F "GO=" '{print $2}' | awk -F ";" '{print $1}' > block$block-GOs.txt
  cat block$block-GOs.txt | tr -s "\n" " " | tr -s "|" " " | tr -s "," " " | tr -s " " "\n" | sort | uniq -c | sort -n > block$block-GO-collapsed.txt 
done

for block in {00..15}; 
do 
  block=$(printf "%02d\n" ${block})
  cat block$block-GOs.txt | tr -s "\n" " " | tr -s "|" " " | tr -s "," " " | tr -s " " "\n" > block$block-GO-terms.text
done

for block in {00..15};
do
  block=$(printf "%02d\n" ${block})
  mkdir -p block$block
  count=0
  for GO in $(awk -F " " '{print $2}' block$block-GO-collapsed.txt); do
    count=$(( $count + 1 ))
    curl -s https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/$GO/complete > block${block}/$(printf "%03d\n" ${count})-$GO 
  done
done

for block in {00..15};
do
  cd block${block}
  for i in  *-GO:*;do printf $(grep $(echo $i | awk -F "-" '{print $2}') ../block${block}-GO-collapsed.txt); printf "\t"$i"\t"; printf $(cat $i | tr -s "," "\n" | grep aspect)"\t";printf $(cat $i | tr -s "," "\n" | grep -m1 name);echo ;done > ../Block${block}-Summary.tsv
  cd ..
done