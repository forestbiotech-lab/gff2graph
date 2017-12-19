#! /usr/bin/env python3

import sys
from graph_tool.all import *
from pylab import *

########Filtering edges if true will filter the edges type specified below in filter_edge_type
filter_edges=True
filter_edge_type=0

#Loads the graph
g = load_graph("my_graph.xml.gz")

##Remove edges that are gene-gene edges
#total_num of edges
edge_num=g.num_edges(ignore_filter=True)

#Edge property set to false
edgeFilter=g.new_edge_property("bool",[1]*edge_num)
gg_edges=find_edge(g, g.edge_properties["type_code"],filter_edge_type)
for e in gg_edges:
  #Set to false edege that match the above property
  edgeFilter[e]=0
if filter_edges:
  g.set_edge_filter(edgeFilter)g

def labelCC(g): 
  #Labelling the components in the graph
  clabels=graph_tool.topology.label_components(g, vprop=None, directed=None, attractors=False)
  return clabels[0].get_array().tolist()

#Is this necessary????
verticesCC=labelCC(g) 


#Describes the size of each Connected component
ccSize=dict()
for component in verticesCC:
  try:
    ccSize[component]+=1
  except KeyError:
    ccSize[component]=1



#Filter [ccSize] dictionary for values greater than [filter]
def filter_freq(ccSize,filter):
  res=dict()
  for key in ccSize.keys():
    if ccSize[key]>filter:
      res[key]=ccSize[key]
  return res


def cc_vertex_list(cc): 
  verticesCC=labelCC(g) 
  #list of vertexes that belong to cc
  clusterFilter=[]
  for vertice in range(0,len(verticesCC)):  
    if verticesCC[vertice]==int(cc):
      clusterFilter.append(1)
    else:
      clusterFilter.append(0)
  return clusterFilter

def cc_vertex_property(cc,g):
  #vertex_property with the CC
  clusterFilter=cc_vertex_list(cc)
  return g.new_vertex_property("bool",clusterFilter)


#Draws specified graphs to graphs/blocks/
#Draw the graph of the specified CC 
def drawCC(g,cc,type="sfdp",tt="label",top=False,edgeFilter=None,vertexFilter=None):
  print("Starting to print graph:"+str(cc),file=sys.stderr)
  print("Starting to print graph:"+str(cc))
  
  centrality=False
  pos=None
  vt=g.vertex_properties["label"]
  #Vertex_fill_color
  v_f_c=g.vertex_properties["color"]
  clusterFilter=cc_vertex_list(cc)    

  def labelTop(clusterFilter,values,percentage,labels,g,tt):
  ##Label only nodes that have the top 0.5% values 
  #clusterFilter: Boolean list identifying the components
    cc_values=[]
    for v in range(0,len(clusterFilter)):
      if clusterFilter[v]==1:
        cc_values.append(values[v])          
    cc_values.sort()
    cc_values.reverse()
    upper_limit=cc_values[int(ceil(len(cc_values)*percentage))]
    print("Upper limit:"+str(upper_limit)+" Max:"+str(max(cc_values))+" Min:"+str(min(cc_values)))
    important=[]
    for i in range(0,len(values)):
      if values[i] >= upper_limit and clusterFilter[i]==1:
        important.append(labels[g.vertex(i)])
        print(tt+"-"+'{:.2e}'.format(float(values[i]))+" : "+labels[g.vertex(i)],file=sys.stderr)
        print(tt+"-"+'{:.2e}'.format(float(values[i]))+" : "+labels[g.vertex(i)])
      else:
        important.append("")
    vt=g.new_vertex_property("string",important)
    return vt

  if tt is not "label":
    centrality=True
    print("Calculating "+tt+" for connected component.",file=sys.stderr)
    print("Calculating "+tt+" for connected component.")
    #########################################Page Rank###############################################################
    if tt=="pagerank":
      if filter_edges:
        g.set_edge_filter(edgeFilter)
      centrality=pagerank(g)
    ##################################################################################################
    
    ########################################Betweenness###############################################    
    if tt=="betweenness":
      if filter_edges:
        g.set_edge_filter(edgeFilter)
      print(g)
      vb,eb=betweenness(g)
      centrality=vb

    if tt=="closeness":
      if filter_edges:
        g.set_edge_filter(edgeFilter)
      print(g)
      centrality=closeness(g)
    
    sizeRange=centrality
    v_f_c=centrality
    vo=centrality      
    if top:
      vt=labelTop(clusterFilter,centrality.get_array().tolist(),0.005,vt,g,tt)
    else:
      ##Cast floats to string but only with 2 precision elements normalization
      normalized=[]
      for i in centrality.get_array().tolist():
        normalized.append('{:.2e}'.format(float(i)))
      vt=g.new_vertex_property("string",normalized)
      
    if tt=="llklklklk":  
      cpd=central_point_dominance(g,betweenness(g))
      eVal,eVec=eigenvector(g)
      k=katz(g)
      eig,x,y=hits(g) 
      et=eigentrust(g)
      tt=trust_transitivity(g)

  if filter_edges:
    g.set_edge_filter(edgeFilter)
  #Filter using a bool vertex_property : This requires iterating the vertexes in python
  #vpClusterFilter=g.new_vertex_property("bool",clusterFilter)
  #Remove a type of code
  if vertexFilter is not none:
    g.set_vertex_filter(vertexFilter)

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
  if cc==0:
    o_s=(4920,2080)
  else:
    o_s=(1920,1080)
  filtering=""
  if filter_edges:
    filtering+="-Filtered_"+filter_edge_type
  if centrality:
    graph_draw(g,pos,output_size=o_s,vorder=vo,vertex_fill_color=v_f_c,edge_color=g.edge_properties["color"],edge_pen_width=1,vertex_size=prop_to_size(sizeRange, mi=5, ma=15),vcmap=matplotlib.cm.gist_heat,output="graphs/distance/centralities/"+tt+"/graph-top_"+str(top)+filtering+"-heat-centralities_"+tt+"-"+str(type)+"-CC_"+str(cc)+".png")
  else:  
    graph_draw(g,pos,output_size=o_s,vertex_fill_color=v_f_c,edge_color=g.edge_properties["color"],edge_pen_width=1,vertex_size=10,output="graphs/distance/graph-top_"+str(top)+filtering+"-colored_vertices-"+str(type)+"-"+str(cc)+".png")  
  graph_draw(g,pos,output_size=o_s,vertex_text=vt,vertex_text_position=1,vertex_fill_color=g.vertex_properties["color"],vertex_size=10,edge_color=g.edge_properties["color"],edge_pen_width=1,output="graphs/distance/graph-top_"+str(top)+filtering+"-colored_vertices-TextNodes_"+tt+"-"+str(type)+"-"+str(cc)+".png")
  print("Graph-"+str(cc)+".png - Finished")

#Draws specified graphs to graphs/blocks/
def drawGraph(g,cc,type="sfdp",tt="label",top=False,vp=None,ep=None,edgeFilter=None,vertexFilter=None):
  print("Starting to print graph:"+str(cc),file=sys.stderr)
  print("Starting to print graph:"+str(cc))
  #  
  centrality=False
  if vp is None:
    vt=g.vertex_properties["label"]
  else:
    vt=vp
  # 
  #Vertex_fill_color
  v_f_c=g.vertex_properties["color"]
  clusterFilter=cc_vertex_list(cc)    
  #  
  def labelTop(clusterFilter,values,percentage,labels,g,tt):
  ##Label only nodes that have the top 0.5% values 
  #clusterFilter: Boolean list identifying the components
    cc_values=[]
    for v in range(0,len(clusterFilter)):
      if clusterFilter[v]==1:
        cc_values.append(values[v])          
    cc_values.sort()
    cc_values.reverse()
    upper_limit=cc_values[int(ceil(len(cc_values)*percentage))]
    print("Upper limit:"+str(upper_limit)+" Max:"+str(max(cc_values))+" Min:"+str(min(cc_values)))
    important=[]
    for i in range(0,len(values)):
      if values[i] >= upper_limit and clusterFilter[i]==1:
        important.append(labels[g.vertex(i)])
        print(tt+"-"+'{:.2e}'.format(float(values[i]))+" : "+labels[g.vertex(i)],file=sys.stderr)
        print(tt+"-"+'{:.2e}'.format(float(values[i]))+" : "+labels[g.vertex(i)])
      else:
        important.append("")
    vt=g.new_vertex_property("string",important)
    return vt

  if centrality:
    if top:
      vt=labelTop(clusterFilter,centrality.get_array().tolist(),0.005,vt,g,tt)
    else:
      ##Cast floats to string but only with 2 precision elements normalization
      normalized=[]
      for i in centrality.get_array().tolist():
        normalized.append('{:.2e}'.format(float(i)))
      vt=g.new_vertex_property("string",normalized)
      
  if edgeFilter is not None:
    g.set_edge_filter(edgeFilter)
  #Filter using a bool vertex_property : This requires iterating the vertexes in python
  #vpClusterFilter=g.new_vertex_property("bool",clusterFilter)
  #Remove a type of code
  if vertexFilter is not None:
    g.set_vertex_filter(vertexFilter)
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
  if cc==0:
    o_s=(4920,2080)
  else:
    o_s=(1920,1080)
  filtering=""
  if edgeFilter is not None:
    filtering+="-Filtered_"+str(filter_edge_type)
  if centrality:
    graph_draw(g,pos,output_size=o_s,vorder=vo,vertex_fill_color=v_f_c,edge_color=g.edge_properties["color"],edge_pen_width=1,vertex_size=prop_to_size(sizeRange, mi=5, ma=15),vcmap=matplotlib.cm.gist_heat,output="graphs/blocks/centralities/"+tt+"/graph-top_"+str(top)+filtering+"-heat-centralities_"+tt+"-"+str(type)+"-CC_"+str(cc)+".png")
  else:  
    graph_draw(g,pos,output_size=o_s,vertex_fill_color=v_f_c,edge_color=g.edge_properties["color"],edge_pen_width=1,vertex_size=40,output="graphs/blocks/graph-top_"+str(top)+filtering+"-colored_vertices-"+str(type)+"-"+str(cc)+".png")  
  graph_draw(g,pos,output_size=o_s,vertex_text=vt,vertex_text_color="#FFFFFF",vertex_fill_color=g.vertex_properties["color"],vertex_size=40,edge_color=g.edge_properties["color"],edge_pen_width=1,output="graphs/blocks/graph-top_"+str(top)+filtering+"-colored_vertices-TextNodes_"+tt+"-"+str(type)+"-"+str(cc)+".png")
  print("graph-"+str(cc)+".png - Finished")
  g.clear_filters()

#import matplotlib.pyplot as plt
#plt.bar(range(len(ccSize)), ccSize.values(), align='center')
#plt.xticks(range(len(newFreq)), newFreq.keys())
#plt.show()

#Calculate the degree distribution #Filter it for degrees bigger than 3?
def degreeFiltered(min):
  res=dict()
  for cc in ccSize.keys():
    if filter_edges:
      g.set_edge_filter(edgeFilter)
    degree=g.get_out_degrees(find_vertex(g,clabels[0],cc)).tolist()
    degMax=max(degree)
    if len(degree)>2 and degMax>=min:
      res[cc]=degMax
      if cc==0:
        continue
      print(str(cc)+": "+str(degMax)+" "+str(degree))
  return res

#Output basic statistics
def basicStats(centralities):
  print(g)
  print("Number of connected components: "+str(len(ccSize.keys())))
  MaxNodes=max(ccSize.values())
  bigComponent=filter_freq(ccSize,MaxNodes-1)
  print("Big component: "+str(list(bigComponent.keys())[0])+" "+str(MaxNodes)+"nodes.")
  #Show first quartile
  degrees=degreeFiltered(10)
  degreesList=list(degrees.values())
  degreesList.sort()
  degreesList.reverse()
  print("Top 10 max degrees: "+str(degreesList[0:10]))
  for centrality in centralities:
    for cc in degrees.keys():
      #if cc==0:
      #  continue
      g.clear_filters()
      drawCC(cc,"sfdp",centrality)
      drawCC(cc,"sfdp",centrality,top=True)
      
#basicStats(["label"])#["pagerank","closeness","betweenness"])
#drawCC(1106,"sfdp","betweenness",top=True)

#Plot the degree distibution (Requeires matlibpy to be installed)
def plotDegreeDist(g,title_str):
  degrees=g.get_out_degrees(g.get_vertices())
  maxDeg=max(degrees)
  degreeDist=dict([[x,0] for x in range(0,int(maxDeg)+1)])
  for degree in degrees:
    degreeDist[degree]+=1
  degreeDist=dict([[degree,degreeDist[degree]/g.num_vertices()] for degree in degreeDist.keys()])
  figure()
  plot(list(degreeDist.values()))
  ax=axes()
  ax.set_xscale("log")
  ax.set_yscale("log")
  title(title_str)
  ylabel("Pk")
  xlabel("k")
  savefig(title_str+".svg")
  return degreeDist 


def plotclusterDist(g,title_str):
  degrees=g.get_out_degrees(g.get_vertices())
  maxDeg=max(degrees)
  degreeDist=dict([[x,0] for x in range(0,int(maxDeg)+1)])
  for degree in degrees:
    degreeDist[degree]+=1
  degreeDist=dict([[degree,degreeDist[degree]/g.num_vertices()] for degree in degreeDist.keys()])
  figure()
  plot(list(degreeDist.values()))
  ax=axes()
  ax.set_xscale("log")
  ax.set_yscale("log")
  title(title_str)
  ylabel("Pk")
  xlabel("k")
  savefig(title_str+".svg")
  return degreeDist 

def alternativePathsForTergetVertices(g):
  #number of edges
  edge_num=g.num_edges(ignore_filter=True)
  #target edges
  target_edges=find_edge(g, g.edge_properties["type_code"],3)
  target_edgeFilter=g.new_edge_property("bool",[1]*edge_num)
  
  #Filter target edges  
  for e in target_edges:
    #Filter that edge
    target_edgeFilter[e]=0
    g.set_edge_filter(target_edgeFilter)
    sp=shortest_path(g,e.source(),e.target())
    sd=shortest_distance(g,e.source(),e.target())
    if len(sp[0]) is not 0: 
      cc=clabels[0][sp[0][0]]
      if cc is not 0:
        print(e)
        print(cc)
        print(sd)
        drawCC(cc,"sfdp","label",top=True)
    target_edgeFilter[e]=1 #add it back
    g.clear_filters()

#alternativePathsForTergetVertices(g)

def vpFilterByValue(g,vp,match):
  num_vertices=len(vp.get_array().tolist())
  res=g.new_vertex_property("bool",[0]*edge_num)
  for v in find_vertex(g,vp,match):
    res[v]=1    
  return res

###Partitioning into blocks using Monte carlo markov chains (Uncomment the line below)
#g.set_vertex_filter(cc_vertex_property(verticesCC,0,g))
#state = minimize_blockmodel_dl(g)
#b = state.get_blocks()
def printNodesPerBlock(b,g,verticesCC):
  for v in g.get_vertices():
    if verticesCC[v]==0:
      print("Block:"+str(b[g.vertex(v)])+"\tVertex:"+str(v)+"\tLabel:"+str(g.vertex_properties['label'][g.vertex(v)]))


#Calculate the average path length using a specified vertix property and or edge property
def averagePathLength(g,vp=None,ep=None):
  g.clear_filters()
  if vp is not None:
    g.set_vertex_filter(vp)
  if ep is not None:
    g.set_edge_filter(ep)
  sum=0
  for v1 in g.vertices():
    for v2 in g.vertices():
      sd=shortest_distance(g,g.vertex(v1),g.vertex(v2))
      if sd is not 2147483647:
        sum+=sd 
  print(sum)


def labelTopDegrees(g):
  count=0
  degrees=g.get_out_degrees(g.get_vertices())
  for deg in degrees:
    if deg > 30:
      print(str(deg)+"-> Idx"+str(count)+" : "+g.vertex_properties['label'][g.vertex(count)])
    count+=1

#Shows the k core levels up to 3 for the hardcoded vertex 90548 (can be changed to a variable)
def showSubGraph():
  #used to show biggest hub.
  g.clear_filters()
  vertexFilter=g.new_vertex_property("bool",[0]*g.num_vertices())
  kCoreVp=g.new_vertex_property("string",["0"]*g.num_vertices())
  source=g.vertex(90548)
  for v in bfs_iterator(g,source):
    if shortest_distance(g,source,v.source())<3: 
      kCoreVp[v.source()]=str(shortest_distance(g,source,v.source()))
      vertexFilter[v.source()]=1
    else:
      break

  drawGraph(g,90548,type="sfdp",tt="label",top=False,vp=kCoreVp,ep=None,edgeFilter=None,vertexFilter=vertexFilter)
#for block in range(1,16):
#  g.clear_filters()
#  vertexFilter=vpFilterByValue(g,b,block)
#  g.set_vertex_filter(vertexFilter)
#  g.set_edge_filter(edgeFilter)
#  print(g)
#  drawGraph(g,block,type="sfdp",tt="label",top=False,vp=None,ep=None,edgeFilter=edgeFilter,vertexFilter=vertexFilter)