#!/usr/bin/env python3

# Created by Bruno Costa
# Using graph-tools
# https://graph-tool.skewed.de
#
# call: loadGraph.py [vertices] [edges]


from graph_tool.all import *

import sys
import time 

from pylab import *
import random

# Timing script
start_time = time.time()


vertices=sys.argv[1]
edges=sys.argv[2]


#Start graph
g=Graph(directed=False)

v_id=dict()
#Add id property to vertex
vertex_id=g.new_vertex_property("int")


vertices=open(vertices,"r")
edges=open(edges,"r")

vertices=[line.strip().split("\t") for line in vertices]
for vertex in vertices[1:]:
  v=g.add_vertex()
  v_id[vertex[0]]=v
  vertex_id[v]=vertex[0]

#Random graph
#for vertex in range(1,100):
  #Save vertex in dict
  #v_id[vertex]=v
  #Add id property
  #vertex_id[v]=vertex

#for edge in range(1,50):
  #Save vertex in dict
  #v1=random.randint(1,50)
  #v2=random.randint(51,99)
  #e=g.add_edge(v_id[v1],v_id[v2])

edges=[line.strip().split("\t") for line in edges]
for edge in edges[1:]:

  e=g.add_edge(v_id[edge[0]],v_id[edge[1]])
  #Add id property
  

print(g)
pos=sfdp_layout(g)
graph_draw(g,pos,output_size=(1920,1080), vertex_size=1,edge_pen_width=1.2, vcmap=matplotlib.cm.gist_heat_r,output="graph.png")

print("--- %s seconds ---" % (time.time() - start_time))
