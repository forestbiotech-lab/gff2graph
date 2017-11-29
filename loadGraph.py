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

#load graph
g = load_graph("my_graph.xml.gz")
  

print(g)
pos=sfdp_layout(g)
graph_draw(g,pos,output_size=(1920,1080), vertex_size=1,edge_pen_width=1.2, vcmap=matplotlib.cm.gist_heat_r,output="graph.png")

print("--- %s seconds ---" % (time.time() - start_time))
