#! /usr/bin/env python3

from graph_tool.all import *
from pylab import *

g = load_graph("my_graph.xml.gz")


#Labelling the components in the graph 
clabels=graph_tool.topology.label_components(g, vprop=None, directed=None, attractors=False)
verticesCC=clabels[0].get_array().tolist()
freq=dict()
for component in verticesCC:
  try:
    freq[component]+=1
  except KeyError:
    freq[component]=1
freqInv=dict()


#Filter [freq] dictionary for values greater than [filter]
def filter_freq(freq,filter):
  res=dict()
  for key in freq.keys():
    if freq[key]>filter:
      res[key]=freq[key]
  return res

#Draw the graph of the specified CC
def showCC(cc,type=None):
  pos=None
  #list of vertexes that belong to cc
  #find_vertex(g,clabels[0],cc)
  clusterFilter=[]
  for vertice in range(0,len(verticesCC)):  
    if verticesCC[vertice]==int(cc):
      clusterFilter.append(1)
    else:
      clusterFilter.append(0)
  g.clear_filters()
  vpClusterFilter=g.new_vertex_property("bool",clusterFilter)
  g.set_vertex_filter(vpClusterFilter)
  if type=="sfdp":
    pos=sfdp_layout(g)
  if type=="arf":
    pos=arf_layout(g, max_iter=0)
  if type=="fr":  
    pos = fruchterman_reingold_layout(g, n_iter=1000)
  if type=="radial": #Doesn't work because that node isn't there  
    pos=radial_tree_layout(g, g.vertex(0))
  if type=="planar":
    pos=planar_layout(g)
  #graph_draw(g,pos,output_size=(1920,1080), vertex_size=1,edge_pen_width=1.2, vcmap=matplotlib.cm.gist_heat_r,output="graph"+str(cc)+".png")
  graph_draw(g,pos,output_size=(1920,1080),vertex_fill_color=g.vertex_properties["color"],vertex_size=10,edge_color=g.edge_properties["color"],edge_pen_width=1,output="graph-colored_vertices-"+str(type)+"-"+str(cc)+".png")
  graph_draw(g,pos,output_size=(1920,1080),vertex_text=g.vertex_properties["label"],vertex_text_position=1,vertex_fill_color=g.vertex_properties["color"],vertex_size=10,edge_color=g.edge_properties["color"],edge_pen_width=1,output="graph-colored_vertices-TextNodes-"+str(type)+"-"+str(cc)+".png")

#Draw graph for components with the biggest number of nodes
## cclist=[2699,1595,2503,2900,2313,2363,3721,2050,2905,2,4136]
## #cclist=[2699]
## for cc in cclist:
##   print(cc)
##   g.clear_filters()
##   showCC(cc)
##   print("graph-colored_vertices-"+str(cc)+".png - Finished")
## 

#import matplotlib.pyplot as plt
#plt.bar(range(len(freq)), freq.values(), align='center')
#plt.xticks(range(len(newFreq)), newFreq.keys())
#plt.show()

#Calculate the degree distribution #Filter it for degrees bigger than 3?
def degreeFiltered(min):
  res=dict()
  for cc in freq.keys():
    degree=g.get_out_degrees(find_vertex(g,clabels[0],cc)).tolist()
    degMax=max(degree)
    if len(degree)>1 and degMax>=min:
      res[cc]=degMax
      if cc==0:
        continue
      print(str(cc)+": "+str(degMax)+" "+str(degree))
  return res

def basicStats():
  print(g)
  print("Number of connected components: "+str(len(freq.keys())))
  MaxNodes=max(freq.values())
  bigComponent=filter_freq(freq,MaxNodes-1)
  print("Big component: "+str(list(bigComponent.keys())[0])+" "+str(MaxNodes)+"nodes.")
  #Show first quartile
  degrees=degreeFiltered(8)
  degreesList=list(degrees.values())
  degreesList.sort()
  degreesList.reverse()
  for cc in degrees.keys():
    if cc==0:
      continue
    g.clear_filters()
    showCC(cc,"sfdp")
      
  print("Top 10 max degrees: "+str(degreesList[0:10]))

basicStats()
