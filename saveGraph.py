#! /usr/bin/env python3

from graph_tool.all import *

vertices="nodes.tsv"
edges="edges.tsv"

#Start graph
g=Graph(directed=False)

v_id=dict()
#Add property to vertex
vertex_id=g.new_vertex_property("int")
vertex_type=g.new_vertex_property("string")
vertex_label=g.new_vertex_property("string")
vertex_color=g.new_vertex_property("string")
#https://xkcd.com/color/rgb/
vertex_type_code=g.new_vertex_property("float")

vertices=open(vertices,"r")
edges=open(edges,"r")

#Loading vertices
print("Starting to load vertices")
vertices=[line.strip().split("\t") for line in vertices]
for vertex in vertices[1:]:
  v=g.add_vertex()
  v_id[vertex[0]]=v
  vertex_id[v]=vertex[0]
  vertex_label[v]=vertex[1]
  vertex_type[v]=vertex[2]
  if vertex[3]=="0": #-
    vertex_color[v]="#acc2d9"
    #cloudy blue
    vertex_type_code[v]=0.0
  elif vertex[3]=="1": #Genes
    vertex_color[v]="#5cac2d" #grass  
    vertex_type_code[v]=0.25
  elif vertex[3]=="2": #Conserved
    vertex_color[v]="#fd8d49" #orangeish   
    vertex_type_code[v]=0.5
  elif vertex[3]=="3": #Novel
    vertex_color[v]="#1d5dec" #azul
    vertex_type_code[v]=0.75
  #vertex_type_code[v]=vertex[3]

print("Finished loading vertices")

#Make them internal properties
g.vertex_properties["type"] = vertex_type
g.vertex_properties["color"] = vertex_color
g.vertex_properties["label"] = vertex_label
g.vertex_properties["type_code"] = vertex_type_code

edge_type_code=g.new_edge_property("int")
edge_color=g.new_edge_property("string")

#Loading edges
print("Loading edges")
edges=[line.strip().split("\t") for line in edges]
for edge in edges[1:]:
  #Add id property
  e=g.add_edge(v_id[edge[0]],v_id[edge[1]])
  #Type code 0-3
  if edge[3]=="0": #-
    edge_color[e]="#343837" #Charcoal
    edge_type_code[e]=0
  elif edge[3]=="1": #Gene neighbour
    edge_color[e]="#98eff9" #Robin egg
    edge_type_code[e]=1
  elif edge[3]=="2": #Inside Gene
    edge_color[e]="#98eff9" #Robin egg  
    edge_type_code[e]=2
  elif edge[3]=="3": #Target
    edge_color[e]="#ff000d" #Bright red
    edge_type_code[e]=3
  edge_type_code[e]=edge[3]

print("Finished loading edges")  

g.edge_properties["type_code"] = edge_type_code
g.edge_properties["color"] = edge_color


out_file="my_graph.xml.gz"
g.save(out_file)
print("Graph saved to: "+out_file)