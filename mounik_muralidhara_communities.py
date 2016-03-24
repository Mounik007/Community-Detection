# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 23:34:51 2015

@author: mounik
"""

from networkx import networkx
import community
import sys
import matplotlib.pyplot as plt
from matplotlib.cm import gist_rainbow
import csv

def ComputeClusterGirvanNewMan(lstInputData, fileName):
    lstAllStagesGraph = []
    communityGraph = networkx.Graph()
    communityGraph.add_edges_from(lstInputData)
    permGraphCopy = communityGraph.copy()
    #Generate Edges from CommunityGraph
    lstEdgesFromGraph = networkx.edges(communityGraph)
    while(len(lstEdgesFromGraph)>0):
        dictBetweenessOfEdge = {}
        dictBetweenessOfEdge = networkx.edge_betweenness(communityGraph)
        lstSetOfCommunities = []
        for item in sorted(networkx.connected_components(communityGraph)):
            lstSetOfCommunities.append(list(item))
        dictModularityCluster = {}
        for index in range(len(lstSetOfCommunities)):
            for element in lstSetOfCommunities[index]:
                dictModularityCluster[element]= index
        modularityValue = community.modularity(dictModularityCluster, communityGraph)
        lstTempStorage = []
        lstTempStorage.append(modularityValue)
        lstTempStorage.append(lstSetOfCommunities)
        lstTempStorage.append(dictModularityCluster)
        lstAllStagesGraph.append(lstTempStorage)
        maxTupleValue = max(dictBetweenessOfEdge.values())
        lstMaxValueList = []
        for component in dictBetweenessOfEdge:
            if(dictBetweenessOfEdge[component] == maxTupleValue):
                lstMaxValueList.append(component)
        communityGraph.remove_edges_from(lstMaxValueList)
        lstEdgesFromGraph = networkx.edges(communityGraph)
    
    maxList = []
    maxList=max(lstAllStagesGraph)
    for aList in maxList[1]:
        print(aList)
    networkx.draw(permGraphCopy, node_color = maxList[2].values(), with_labels = True, cmap= gist_rainbow, node_size =200, width=1, alpha=1.0, edge_vmin=1000, edge_vmax=1500.0)
    plt.savefig(fileName)
    #plt.show()
    plt.clf()

if __name__ == '__main__':
    lstInputData = []
    fileName = str(sys.argv[2])
    with open(sys.argv[1]) as tsvfile:
        tsvReader = csv.reader(tsvfile, delimiter="\n")
        for line in tsvReader:
            tempStr = (str(line)).replace("[", "").replace("]","").replace("'","")
            lstTempItem = tempStr.split(" ")
            lstTempItem2 = []
            for item in lstTempItem:
                lstTempItem2.append(int(item))
            lstInputData.append(lstTempItem2)
    ComputeClusterGirvanNewMan(lstInputData, fileName)