#! /usr/bin/env python3

from graph_tool.all import *
from pylab import *
import random

g=Graph(directed=False)

v_id=dict()

vertex_id=g.new_vertex_property("int")
vertex_type=g.new_vertex_property("string")
vertex_color=g.new_vertex_property("string")
vertex_type_code=g.new_vertex_property("float")

#Random graph
for vertex in range(1,100):
  print(vertex)
  v=g.add_vertex()
  #Save vertex in dict
  v_id[vertex]=v
  #Add id property
  vertex_id[v]=vertex
  if vertex<20:
    vertex_type[v]="#388004" #green
    vertex_type_code[v]=0.01
  elif vertex<40:
    vertex_type[v]="#ff0789" #sun yellow
    vertex_type_code[v]=0.001
  elif vertex<60:
    vertex_type[v]="#cb6843"
    vertex_type_code[v]=0.0001
  elif vertex<100:
    vertex_type[v]="#ff0789" #pink
    vertex_type_code[v]=0.00001

for edge in range(1,50):
  #Save vertex in dict
  v1=random.randint(1,99)
  v2=random.randint(1,99)
  e=g.add_edge(v_id[v1],v_id[v2])

vp, ep =betweenness(g)
pos = fruchterman_reingold_layout(g, n_iter=1000)
#graph_draw(g,pos,output_size=(1920,1080), vertex_size=1,edge_pen_width=1.2, vcmap=matplotlib.cm.gist_heat_r,output="graph"+str(cc)+".png")
graph_draw(g,pos,output_size=(1920,1080),vertex_fill_color=vertex_type,output="Random_graph-3.png")