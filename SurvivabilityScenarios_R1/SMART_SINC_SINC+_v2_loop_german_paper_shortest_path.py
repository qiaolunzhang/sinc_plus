# SMART ALGORITHM FOR SURVIVABILITY
import copy
import pickle

import networkx as nx
import random
import itertools
from collections import Counter
import time as time
import numpy as np
import sys
import os


# Function to read the number of virtual networks that is a value present in the data file
# The value with the number of VNs is read in a specific position in the data file
def read_number_of_VNs(file_name):
    datafile = file_name
    data = open(datafile, "r")
    data.readline()
    data.readline()
    line = data.readline()
    app = line.split("=")
    app2 = str(app[1]).split(";")
    num_vn = int(app2[0])
    data.close()
    return num_vn


#read physical topology from file
def read_physical_topology(file_name):
    #print(file_name)
    datafile = file_name
    num_physical_links = 0
    data = open(datafile, "r")
    data.readline()
    data.readline()
    line = data.readline()
    app = line.split("=")
    app2 = str(app[1]).split(";")
    num_vn = int(app2[0])
    #print("App:",app2[0])
    for l in range(4):
        data.readline()

    line = data.readline()
    app = line.split()

    app5 = line.split("(")
    for link in app5:
        num_physical_links += 1
    num_physical_links -= 1
    #print(num_physical_links)

    #read physical links and add these edges in the graph
    for l in range(num_physical_links):
        app2 = str(app[l + 3]).split()
        app3 = str(app2[0]).split(",")
        app4 = app3[0].split("(")
        n1 = int(app4[1])

        app4 = app3[1].split(")")
        n2 = int(app4[0])
        #print("App:",n1,n2)
        P.add_edge(n1, n2, weight=1)

    #print("Physical network loaded, edges:",P.edges())
    data.close()


#read the logical topology specified as input from file
def read_logical_topology(top, start_key, file_name, vn_index=-1):
    #datafile = 'Ring4Node-' + str(datfileinstance+1) + '.dat'
    datafile = file_name
    num_logical_links = 0

    data = open(datafile, "r")
    data.readline()
    data.readline()
    line = data.readline()
    num_vn_line = line.split("=")
    app2 = str(num_vn_line[1]).split(";")
    num_vn = int(app2[0])
    #print("App:",app2[0])
    for l in range(7 + num_vn + top):
        data.readline()

    line = data.readline()
    app = line.split()

    app5 = line.split("(")
    for link in app5:
        num_logical_links += 1
    num_logical_links -= 1
    #print(num_logical_links)

    #Keys database (each virtual link must have a key)
    list_of_keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
    list_of_keys2 = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp',
                     'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz', 'ab', 'b2', 'cb', 'db', 'eb', 'fb',
                     'gb', 'hb', 'ib', 'jb', 'kb', 'lb', 'mb', 'nb', 'ob', 'pb', 'qb', 'rb', 'sb', 'tb', 'ub', 'vb',
                     'wb', 'xb', 'yb', 'zb']
    list_of_keys_tmp_all = []
    for i in range(0, 100):
        list_of_keys_temp = [ele + str(i) for ele in list_of_keys]
        list_of_keys_tmp_all.extend(list_of_keys_temp)
    list_of_keys.extend(list_of_keys_tmp_all)

    for el in list_of_keys2:
        list_of_keys.append(el)

    #read logical links and add these edges in the graph
    for l in range(num_logical_links):
        app2 = str(app[l + 3]).split()
        app3 = str(app2[0]).split(",")
        app4 = app3[0].split("(")
        n1 = int(app4[1])

        app4 = app3[1].split(")")
        n2 = int(app4[0])
        #print("App:",n1,n2)
        L.add_edge(n1, n2, key=list_of_keys[l])
        #print("LOGICAL EDGE ADDED with key",list_of_keys[l],":",L.edges())
        #print("start key + l:",start_key,l)
        #Combined network (Union of all virtual networks)
        CB.add_edge(n1, n2, key=list_of_keys[start_key + l], vn=vn_index)
    #print("\n\nCombined network edges:",CB.edges())
    #print("Combined network nodes:\n\n",CB.nodes())

    data.close()


#Function that obtain all the double link failures combinations
def find_double_failures(DF):
    first = 1
    numEdges = 0
    comb = 0
    for ed in P.edges():
        numEdges += 1
    num_comb = int(numEdges * (numEdges - 1) / 2)
    #print("Num Comb:",num_comb)

    #For each couple of physical links
    for l1 in P.edges():
        for l2 in P.edges():
            newList = []
            if (l1 != l2):
                trovato = 0
                if (first == 0):
                    for k in range(comb):
                        #take links (s,t) with s<t
                        if (l1[0] < l1[1] and l2[0] < l2[1]):
                            l1a = l1
                            l2a = l2
                        elif (l1[0] < l1[1] and l2[0] > l2[1]):
                            l1a = l1
                            l2a = (l2[1], l2[0])
                        elif (l1[0] > l1[1] and l2[0] < l2[1]):
                            l1a = (l1[1], l1[0])
                            l2a = l2
                        else:
                            l1a = (l1[1], l1[0])
                            l2a = (l2[1], l2[0])
                        #check if the double failures is already present in DF
                        if (l1a in DF[k] and l2a in DF[k]):
                            trovato = 1

                    if (trovato == 0):
                        if (l1[0] < l1[1]):
                            newList.append(l1)
                        else:
                            newList.append((l1[1], l1[0]))

                        if (l2[0] < l2[1]):
                            newList.append(l2)
                        else:
                            newList.append((l2[1], l2[0]))

                        DF.append(newList)
                        comb = comb + 1
                else:
                    if (l1[0] < l1[1]):
                        newList.append(l1)
                    else:
                        newList.append((l1[1], l1[0]))

                    if (l2[0] < l2[1]):
                        newList.append(l2)
                    else:
                        newList.append((l2[1], l2[0]))

                    DF.append(newList)
                    first = 0
                    comb = comb + 1

    #print("\n\nDF:",DF,"\n\n")
    return comb


#function that returns the list of cut-sets of the virtual network
def get_cutsets(vn, totCut):
    fullset = set([i for i in L.nodes()])
    #fullset=set([1,2])
    #print("Fullset:",fullset)
    listrep = list(fullset)
    subsets = []
    for i in range(2 ** len(listrep)):
        subset = []
        for k in range(len(listrep)):
            if i & 1 << k:
                subset.append(listrep[k])
        subsets.append(subset)
        #print(subsets)

    cutsets = []
    cont = 0
    for sub in subsets:
        newList = []
        totList = []
        for el in sub:
            for nd in L.nodes():
                if (nd not in sub):
                    if ((el, nd) in L.edges() and (el, nd) not in newList and (nd, el) not in newList):
                        if (el < nd):
                            newList.append((el, nd))
                            totList.append((vn, el, nd))
                        else:
                            newList.append((nd, el))
                            totList.append((vn, nd, el))
                    elif ((nd, el) in L.edges() and (nd, el) not in newList and (el, nd) not in newList):
                        if (nd < el):
                            newList.append((nd, el))
                            totList.append((nd, el))
                        else:
                            newList.append((el, nd))
                            totList.append((el, nd))
        cont += 1
        cutsets.append(newList)
        totCut.append(totList)
    #print("Cutsets:", cutsets)

    #remove the last and the first element of the list because are empty
    # cutsets.pop(cont - 1)
    # cutsets.pop(0)
    # Check and remove the last element if it's empty and the index exists
    if len(cutsets) > 0 and len(cutsets[-1]) == 0:
        cutsets.pop(-1)

    # Check and remove the first element if it's empty and the list is not empty after previous operation
    if len(cutsets) > 0 and len(cutsets[0]) == 0:
        cutsets.pop(0)

    totCut = [x for x in totCut if x]
    #print("totCut:",totCut)
    return cutsets


# Function that returns the availability of the VN considering
# down a VN that has at least a cut-set down
def get_availability_cutsets(cutsets, mapsOrd):
    #print("Cutsets:", cutsets)
    numFail = 0
    av = {}
    #print("\n\nDF:",DF,"\n\n")
    for df in DF:
        #for each double failure find down virtual links
        virLinksDown = []
        for key in mapsOrd:
            for el in mapsOrd[key]:
                #print("Sto confrontando:",el,"con",df[0],"e",df[1])
                # if (el == df[0]):
                #     virLinksDown.append(key)
                # elif (el == df[1]):
                #     virLinksDown.append(key)
                if (el[0] == df[0][0] and el[1] == df[0][1]):
                    virLinksDown.append(key)
                elif (el[0] == df[0][1] and el[1] == df[0][0]):
                    virLinksDown.append(key)
                elif (el[0] == df[1][0] and el[1] == df[1][1]):
                    virLinksDown.append(key)
                elif (el[0] == df[1][1] and el[1] == df[1][0]):
                    virLinksDown.append(key)
        #print("Physical links down",df[0],df[1],"-> Virtual links down:",virLinksDown)

        found = 0
        #find if at least a cut-set of the VN is down
        for cts in cutsets:
            ctsDown = 1
            for l in cts:
                if (l not in virLinksDown):
                    ctsDown = 0

            if (ctsDown == 1):
                av[numFail] = 1
                found = 1
                #print("Physical links down",df[0],df[1],"failure:",numFail,"cut-set down:",cts,"-> Availability:",av[numFail])

        if (found == 0):
            av[numFail] = 0
        numFail += 1

    #print("av:",av)
    totFail = sum(av.values())
    totAv = numFail - totFail
    #print("NumFail:",numFail)
    #print("TotFail:",totFail)
    #print("Availability:",totAv)
    return totAv


#Function that returns the availability of all VNs considering
#down a VN that has at least a cut-set down
def get_availability_cutsets_total(totCut, totMaps):
    #print("Cutsets:", cutsets)
    av = {}
    totCut = [x for x in totCut if x]
    #print("\n\nDF:",DF,"\n\n")
    for vn in range(1, num_vn + 1):
        numFail = 0
        for df in DF:
            #for each double failure find down virtual links
            virLinksDown = []
            for key in totMaps:
                # todo: check if the following two line is needed
                if key[0] != vn:
                    continue
                for el in totMaps[key]:
                    # flag_1 = False
                    # if (el == df[0]):
                    #     virLinksDown.append(key)
                    # elif (el == df[1]):
                    #     virLinksDown.append(key)
                    # else:
                    #     flag_1 = True
                    flag_2 = False
                    if (el[0] == df[0][0] and el[1] == df[0][1]):
                        virLinksDown.append(key)
                    elif (el[0] == df[0][1] and el[1] == df[0][0]):
                        virLinksDown.append(key)
                    elif (el[0] == df[1][0] and el[1] == df[1][1]):
                        virLinksDown.append(key)
                    elif (el[0] == df[1][1] and el[1] == df[1][0]):
                        virLinksDown.append(key)
                    else:
                        flag_2 = True
                    # if not flag_2 and flag_1:
                    #     print("Debug")

            #print("Physical links down",df[0],df[1],"-> Virtual links down:",virLinksDown)

            found = 0
            #find if at least a cut-set of the VN is down
            for cts in totCut:
                if cts[0][0] != vn:
                    continue
                ctsDown = 1
                for l in cts:
                    if (l not in virLinksDown):
                        ctsDown = 0

                if (ctsDown == 1):
                    av[vn, numFail] = 1
                    found = 1
                    #print("Physical links down",df[0],df[1],"failure:",numFail,"cut-set down:",cts,"-> Availability:",av[vn,numFail])

            if (found == 0):
                av[vn, numFail] = 0
            numFail += 1

    #print("av:",av)
    totFail = sum(av.values())
    toAv = numFail * num_vn - totFail
    #print("NumFail:",numFail)
    #print("TotFail:",totFail)
    #print("Availability:",toAv)
    return toAv


def find_shortest_path_in_contract_graph(req, C):
    # get current virtual network index
    vn_index = req[0]
    # update the weight of the edges, assign higher weight for edges not in the same virtual network
    # for edge in C.edges():
    for u, v, key, data in C.edges(data=True, keys=True):
        if data['vn'] != vn_index:
            C[u][v][key]['weight'] = 1000
        else:
            C[v][u][key]['weight'] = 1
    # find the shortest path in the contracted graph
    try:
        sp = nx.shortest_path(C, source=req[1], target=req[2], weight='weight')
        # get the weight of the path
        weight = nx.shortest_path_length(C, source=req[1], target=req[2], weight='weight')
        if weight >= 1000:
            sharing_flag = True
        else:
            sharing_flag = False
    except nx.NetworkXNoPath:
        sp = []
        weight = np.Inf
        sharing_flag = False
    return sp, weight, sharing_flag


#Compute the availability allowing inter-VN capacity sharing
def get_availability_gateways(totMaps):
    numFail = 0
    totNumVLwithSharing = 0
    av = {}
    numVLwithSharingPerVNFailure_dic = {}
    for df in DF:
        #for each double failure find down virtual links
        virLinksDown = []
        for key in totMaps:
            for el in totMaps[key]:
                # if (el == df[0] and key not in virLinksDown):
                #     virLinksDown.append(key)
                # elif (el == df[1] and key not in virLinksDown):
                #     virLinksDown.append(key)
                if (el[0] == df[0][0] and el[1] == df[0][1]):
                    virLinksDown.append(key)
                elif (el[0] == df[0][1] and el[1] == df[0][0]):
                    virLinksDown.append(key)
                elif (el[0] == df[1][0] and el[1] == df[1][1]):
                    virLinksDown.append(key)
                elif (el[0] == df[1][1] and el[1] == df[1][0]):
                    virLinksDown.append(key)
        #print("Physical links down",df[0],df[1],"-> Virtual links down:",virLinksDown)

        CB2 = CB.copy()
        #print("CB edges:",CB.edges())
        #print("CB2 edges:",CB2.edges())
        #Remove failing links from the copy of the combined network
        for link in virLinksDown:
            if ((link[1], link[2]) in CB2.edges()):
                CB2.remove_edge(link[1], link[2])
            elif ((link[2], link[1]) in CB2.edges()):
                CB2.remove_edge(link[2], link[1])

        #print("Virtual links down:",virLinksDown)

        found = [0 for i in range(1, num_vn + 1)]
        numVLwithSharingList = [0 for i in range(1, num_vn + 1)]

        #print("Found:",found)
        #Find a path of each disconnected virtual link over the combined network (without failing links)
        for req in virLinksDown:
            # todo: update the weight of the edges, assign higher wight for edges not in the same virtual network
            sp, weight, sharing_flag = find_shortest_path_in_contract_graph(req, CB2)
            if len(sp) == 0:
                found[req[0] - 1] = 1
            else:
                if sharing_flag:
                    numVLwithSharingList[req[0] - 1] += 1
            # todo: check if the following five lines of code is needed
            # try:
            #     sp = nx.shortest_path(CB2, req[1], req[2])
            # except nx.NetworkXNoPath:
            #     #print("No path found for request",req,"with failure",numFail,":",df)
            #     found[req[0] - 1] = 1

            #else:
            #print("Shortest path from",req[1],"to",req[2],"is:",sp)

        #If at least a disconnected virtual link cannot be reconnected through a path on the combined network, then its VN is disconnected (and av=1)
        for vn in range(1, num_vn + 1):
            if (found[vn - 1] == 1):
                av[vn, numFail] = 1
            else:
                av[vn, numFail] = 0

            if numVLwithSharingList[vn - 1] > 0:
                totNumVLwithSharing += numVLwithSharingList[vn - 1]
                if (vn, numFail) in numVLwithSharingPerVNFailure_dic.keys():
                    numVLwithSharingPerVNFailure_dic[(vn, numFail)] += numVLwithSharingList[vn - 1]
                else:
                    numVLwithSharingPerVNFailure_dic[(vn, numFail)] = numVLwithSharingList[vn - 1]

        numFail += 1
    #print("AV:",av)
    totFail = sum(av.values())
    totAvGw = numFail * num_vn - totFail
    # averageNumVLwithSharing = totNumVLwithSharing / (len(DF) * num_vn)
    # here we divide by the number of vn that are not disconnected
    averageNumVLwithSharing = totNumVLwithSharing / totAvGw

    #print("NumFail:",numFail)
    #print("TotFail:",totFail)
    #print("Availability with gateways:",totAvGw)
    return totAvGw, totNumVLwithSharing, averageNumVLwithSharing


#Compute the availability allowing inter-VN capacity sharing and spare slice sharing
def get_availability_gateways_shared_slice(totMaps, shMaps):
    numFail = 0
    totNumVLwithSharing = 0
    av = {}
    numVLwithSharingPerVNFailure_dic = {}

    for df in DF:
        #for each double failure find down virtual links
        virLinksDown = []
        for key in totMaps:
            for el in totMaps[key]:
                # if (el == df[0] and key not in virLinksDown):
                #     virLinksDown.append(key)
                # elif (el == df[1] and key not in virLinksDown):
                #     virLinksDown.append(key)
                if (el[0] == df[0][0] and el[1] == df[0][1]):
                    virLinksDown.append(key)
                elif (el[0] == df[0][1] and el[1] == df[0][0]):
                    virLinksDown.append(key)
                elif (el[0] == df[1][0] and el[1] == df[1][1]):
                    virLinksDown.append(key)
                elif (el[0] == df[1][1] and el[1] == df[1][0]):
                    virLinksDown.append(key)
        #print("Physical links down",df[0],df[1],"-> Virtual links down:",virLinksDown)

        CB2 = CB.copy()
        #print("CB edges:",CB.edges())
        #print("CB2 edges:",CB2.edges())
        for link in virLinksDown:
            if ((link[1], link[2]) in CB2.edges()):
                CB2.remove_edge(link[1], link[2])
            elif ((link[2], link[1]) in CB2.edges()):
                CB2.remove_edge(link[2], link[1])
            # else:
            #     CB2.remove_edge(link[2], link[1])

        #print("Virtual links down:",virLinksDown)

        found = [0 for i in range(1, num_vn + 1)]
        numVLwithSharingList = [0 for i in range(1, num_vn + 1)]

        #print("Found:",found)
        #Appluy inter-VN capacity sharing to reconnect disconnected virtual links through a path over the combined VN
        for req in virLinksDown:
            #Try to find a path in the combined virtual network
            try:
                # todo: update the weight of the edges, assign higher wight for edges not in the same virtual network
                CB2_copy = copy.deepcopy(CB2)
                sp, weight, sharing_flag = find_shortest_path_in_contract_graph(req, CB2_copy)
                if sharing_flag:
                    numVLwithSharingList[req[0] - 1] += 1
                # here we try to find again to force it go to except part
                sp = nx.shortest_path(CB2, req[1], req[2])
            except nx.NetworkXNoPath:
                #print("No path found for request",req,"with failure",numFail,":",df)
                dummy = True

                #If no path is found with inter-VN capacity sharing, then apply spare slice sharing

                #SPARE SLICE SHARING
                #Compute spare slice links that are down
                shLinksDown = []
                for key in shMaps:
                    current_path_list = shMaps[key]
                    available_flag = False
                    for current_path in current_path_list:
                        available_flag_cur = True
                        for el in current_path:
                            if (el == df[0] and key not in shLinksDown):
                                available_flag_cur = False
                            elif (el == df[1] and key not in shLinksDown):
                                available_flag_cur = False
                        if available_flag_cur:
                            available_flag = True
                            break
                    if not available_flag:
                        shLinksDown.append(key)

                    # for el in shMaps[key]:
                    #     #print("Sto confrontando:",el,"con",df[0],"e",df[1])
                    #     if (el == df[0] and key not in shLinksDown):
                    #         shLinksDown.append(key)
                    #     elif (el == df[1] and key not in shLinksDown):
                    #         shLinksDown.append(key)

                #Add spare slice links not down to the combined network
                # for l in SH.edges():
                for l in shMaps.keys():
                    if (l not in shLinksDown):
                        # for the edge in spare slice, just give it a large nubmer of virtual network index
                        CB2.add_edge(l[0], l[1], vn=10000)

                link_add = 0
                #Try to route virtual request through combined network + shared spare slice 
                try:
                    sp = nx.shortest_path(CB2, req[1], req[2])
                except:
                    sp = []
                    link_add = 1

                # We are able to find a path in the combined network + shared spare slice
                if len(sp) > 0:
                    numVLwithSharingList[req[0] - 1] += 1
                    # todo: update the number of virtual links that are reconnected through shared spare slice
                    continue

                #Map the new edge in the physical network
                P2 = P.copy()
                #remove physical edges down (the mapping of the link must not use down links)
                for pl in df:
                    P2.remove_edge(pl[0], pl[1])
                #Mapping of the new added edge (the only constraint is not to use failing links)
                try:
                    phy_sp = nx.shortest_path(P2, req[1], req[2])
                    numVLwithSharingList[req[0] - 1] += 1
                except nx.NetworkXNoPath:
                    #If no path is found it means that a node is disconnected from the physical network
                    found[req[0] - 1] = 1
                    #print("No path found for request",req,"with failure",df)

                else:
                    #print("New virtual link",req,"mapped on physical path:",phy_sp,"for failure",df)
                    sp_links = []
                    # convert the nodal form in a link form
                    for jP in range(len(phy_sp)):
                        if jP < len(phy_sp) - 1:
                            if (phy_sp[jP] < phy_sp[jP + 1]):
                                sp_links.append((phy_sp[jP], phy_sp[jP + 1]))
                            else:
                                sp_links.append((phy_sp[jP + 1], phy_sp[jP]))

                    if (req[1], req[2]) in shMaps.keys():
                        shMaps[(req[1], req[2])].append(sp_links)
                    else:
                        shMaps[(req[1], req[2])] = [sp_links]
                    # shMaps[(req[1], req[2])] = sp_links

                    if (link_add == 1):
                        #Add the new edge in the shared slice
                        # todo: we may add two links between same end nodes
                        SH.add_edge(req[1], req[2])
                        #print("Sh edge added, SH edges:",SH.edges())

            #else:
            #    print("Shortest path from",req[1],"to",req[2],"is:",sp)

        #If at least a disconnected virtual link cannot be reconnected through a path on the combined network or on the shared spare slice, then its VN is 
        #disconnected (and av=1)
        for vn in range(1, num_vn + 1):
            if (found[vn - 1] == 1):
                av[vn, numFail] = 1
            else:
                av[vn, numFail] = 0

            if numVLwithSharingList[vn - 1] > 0:
                totNumVLwithSharing += numVLwithSharingList[vn - 1]
                if (vn, numFail) in numVLwithSharingPerVNFailure_dic.keys():
                    numVLwithSharingPerVNFailure_dic[(vn, numFail)] += numVLwithSharingList[vn - 1]
                else:
                    numVLwithSharingPerVNFailure_dic[(vn, numFail)] = numVLwithSharingList[vn - 1]

        numFail += 1
    #print("AV:",av)
    totFail = sum(av.values())
    totAvGw = numFail * num_vn - totFail
    #print("NumFail:",numFail)
    #print("TotFail:",totFail)
    print("Availability with gateways and shared spare slice:", totAvGw)

    #Spare slice wavelength consumption
    totW_sh = 0
    for path in shMaps:
        for link in shMaps[path]:
            totW_sh += 1
    #Total wavelength consumption
    totW = 0
    for path in totMaps:
        for link in totMaps[path]:
            totW += 1

    #print("Wavelengths consumption without shared slice:",totW*2)
    #print("Wavelengths consumption of the shared slice:",totW_sh*2)
    #print("Total wavelengths consumption:",totW*2+totW_sh*2)
    #print("Shmaps",shMaps)
    # averageNumVLwithSharing = totNumVLwithSharing / (len(DF) * num_vn)
    # here we divide by the number of vn that are not disconnected
    averageNumVLwithSharing = totNumVLwithSharing / totAvGw

    return totAvGw, totNumVLwithSharing, averageNumVLwithSharing


# Function that verifies the survivability of a mapping (against single link failures)
# For each cut-set, if not all virtual links belongig to a cut-set share a physical link, then the mapping is survivable
def verify_survivability(newMap, totCut):
    survivable = True
    totCut = [x for x in totCut if x]
    for plink in P.edges():  #for each physical link
        #print("totCut:",totCut)
        for cs in totCut:  # for each cut-set
            count = 0
            card_cut = 0
            for cslink in cs:  #for each link of the cut-set
                card_cut += 1
                #print("NewMap",newMap)
                #print("cslink",cslink)
                #print("NewMap[cslink]:",newMap[cslink])
                #print("plink:",plink)

                #If a physical link is used by the virtual link, increment count
                if (plink in newMap[cslink]):
                    count += 1
            #If the number of virtual links that use the physical link is equal to the cardinality of the cut-set, then mapping NOT survivable
            if (count == card_cut):
                survivable = False
                #print("Cutset",cs,"is not mapped in a survivable way")
    return survivable


##########################################################################################################################################
if __name__ == '__main__':
    #THE PROGRAM STARTS HERE
    if len(sys.argv) == 4:
        cur_num_vn = int(sys.argv[1])
        cur_num_vl = int(sys.argv[2])
        num_instances = int(sys.argv[3])
        # First file and last file to run
        start_file = 1
        # end_file = start_file
        end_file = num_instances
    elif len(sys.argv) == 5:
        cur_num_vn = int(sys.argv[1])
        cur_num_vl = int(sys.argv[2])
        start_file = int(sys.argv[3])
        end_file = int(sys.argv[4])
    elif len(sys.argv) == 5:
        cur_num_vn = int(sys.argv[1])
        cur_num_vl = int(sys.argv[2])
        start_file = int(sys.argv[3])
        end_file = int(sys.argv[4])
    else:
        cur_num_vn = 5
        cur_num_vl = 10
        num_instances = 6
        start_file = 6
        end_file = num_instances


    #end_file=10

    #Number of data files
    num_datafile = (end_file - start_file) + 1

    # Sum, Max and Min values of Availability and Total Wavelength Consumption (over the data files)
    sum_av = 0
    sum_wave = 0
    max_av = 0
    min_av = 200000
    max_wave = 0
    min_wave = 200000
    mean_av = 0
    mean_wave = 0
    #Survivability scenario
    scenario = 4

    #To start the clock
    virtualLinkRequirementOneFiveDic = {}
    virtualLinkRequirementOneThreeDic = {}
    for scenario in [0]:
        #For each data file
        for datafile in range(start_file, end_file + 1):
            time_start = time.time()

            #List of double failures of the physical network
            DF = []
            #Availability and Total Wavelength Consumption values
            totAv = 0
            totW = 0
            #Param that take count of the key assigned to the links
            start_key = 0
            #Dictionary with the mapping of virtual links obver the physical network
            totMaps = {}
            #Cut-sets list of all virtual networks
            totCut = []
            #CB represents the combined virtual network made up by nodes and links of all VNs
            #(common nodes are inserted only 1 time, while common links are inserted many times)
            CB = nx.MultiGraph()

            #Name of input files
            # file_name = 'Datfiles/DataFile' + str(datafile) + '.dat'
            # file_name = 'All_datafiles_used/Ring/2 VNs/DataFile' + str(datafile) + '.dat'
            # file_name = 'DatafilesNew/german-modified/6vn/6vl/DataFile' + str(datafile) + '.dat'
            # file_name = 'DatafilesNew/tokyo-5nodes/' + str(cur_num_vn) + 'vn/' + str(cur_num_vl) + 'vl/DataFile' + str(datafile) + '.dat'
            if cur_num_vl == 6:
                folder_name = 'DatafilesNew/7-node-German-modified/Ring/5Nodes' + str(cur_num_vn) + 'VNs/'
                file_name = folder_name + 'DataFile' + str(datafile) + '.dat'
            else:
                folder_name = 'DatafilesNew/7-node-German-modified/Mesh/Mesh5Nodes' + str(cur_num_vn) + 'VNs/'
                file_name = folder_name + 'DataFile' + str(datafile) + '.dat'

            # file_name = "previous_datafile/DataFile4" + ".dat"
            #Number of virtual networks (VNs)
            num_vn = read_number_of_VNs(file_name)

            # P is the physical network
            P = nx.Graph()
            read_physical_topology(file_name)
            # Find all possible combinations of double link failures in the physical network
            numFail = find_double_failures(DF)

            #For each VN
            # todo: check if we find the routing of each VN separately without considering the other VNs
            vn_Maps_dic = {}
            vn_CutSets_dic = {}

            requests_folder = "requests/german-Capacity/"
            requests_folder = requests_folder + str(cur_num_vn) + "vn/" + str(cur_num_vl) + "vl/"
            # create the folder if it does not exist
            # if not os.path.exists(results_folder):
            # os.makedirs(results_folder)
            requests_file = requests_folder + "instance_" + str(datafile) + "_OneFive.obj"
            with open(requests_file, 'rb') as f:
                virtualLinkRequirementOneFiveDic = pickle.load(f)
            requests_file = requests_folder + "instance_" + str(datafile) + "_OneThree.obj"
            with open(requests_file, 'rb') as f:
                virtualLinkRequirementOneThreeDic = pickle.load(f)

            for vn in range(1, num_vn + 1):

                # L represents the logical network
                L = nx.MultiGraph()

                #read a logical network from file (vn is the number of the logical network that I want to read)
                # the start_key is the key that I have to assign to the links of the logical network, it can mark the virtual link of the logical network
                # todo: check if the start_key can be used to identify the sharing of the virtual link
                start_key = CB.number_of_edges()
                read_logical_topology(vn, start_key, file_name, vn_index=vn)

                nodeTotal = nx.number_of_nodes(L)

                #Copies of the logical network (useful for the rest of the program)
                C = L.copy()
                Co = C.copy()
                Co2 = Co.copy()
                CP = C.copy()

                # P is the physical network
                P = nx.Graph()
                read_physical_topology(file_name)

                #Shared spare slice
                SH = nx.MultiGraph()

                mapping = []
                for u, v, k in Co2.edges(keys=True):
                    # find the path in physical network
                    sp = nx.shortest_path(P, source=u, target=v)
                    # get the list of links in the shortest path
                    sp_links = []
                    for node_index in range(len(sp) - 1):
                        sp_links.append((sp[node_index], sp[node_index + 1]))
                    mapping.append(sp_links)

                no_survivable_mapping_flag = False
                if no_survivable_mapping_flag is False:
                    ######################## First Fit wavelength assignement #############################
                    mapping.sort()
                    # print("Mapping:",mapping)
                    # associations of links with wavelengths
                    link_wavelength = {}
                    # associations of paths with wavelengths
                    path_wavelength = {}
                    for path in mapping:
                        not_found = 0
                        wavelength_path = 0
                        for link in path:
                            if link_wavelength:
                                if link in link_wavelength:
                                    link_wavelength[link] = link_wavelength[link] + 1
                                    if wavelength_path < link_wavelength[link]:
                                        wavelength_path = link_wavelength[link]
                                    not_found = 1
                        if not_found:
                            for link in path:
                                link_wavelength[link] = wavelength_path
                        else:
                            for link in path:
                                wavelength_path = 1
                                link_wavelength[link] = wavelength_path
                            # print("Wavelength path:",wavelength_path)
                        path_wavelength[repr(path)] = wavelength_path

                    ####################### AVAILABILITY COMPUTATION #################################
                    # Find all possible combinations of double link failures in the physical network (only for the first VN since the physical network is only one)
                    # if (vn == 1):
                    #     numFail = find_double_failures(DF)
                    # print("Double Failures:",DF)

                    used_links = []
                    for key in mapping:
                        # print("Key:",key)
                        for el in key:
                            el_app = ()
                            if (el[0] > el[1]):
                                el_app = tuple((el[1], el[0]))
                                # print(el_app)
                                if (el_app not in used_links):
                                    used_links.append(el_app)
                            else:
                                el_app = tuple((el[0], el[1]))
                                if (el_app not in used_links):
                                    used_links.append(el_app)

                    # print("Used physical links:",used_links)

                    # num_Fail=0
                    # cont=0
                    # for df in DF:
                    #    for f in df:
                    #        if (f in used_links):
                    #            num_Fail+=1
                    # print("f:",f)
                    # print("Number of failures:",numFail)

                    # print("Number of failures:",numFail)
                    # print("Mapping final:",mapping)

                    maps = {}
                    for l in L.edges():
                        # print("l:",l)
                        for key in mapping:
                            first = 0
                            cont = 0
                            num_link = 0
                            for el in key:
                                if (el[0] == l[0] and cont == 0 and num_link == 0):
                                    first = 1
                                num_link += 1
                            if (el[1] == l[1] and first == 1):
                                maps[l] = key
                                cont += 1
                    # print("MAPS:",maps)

                    # Create a dictionary with virtual links as keys and with the corresponding mappings as values (links (s,t) with s<t)
                    mapsOrd = {}
                    keyApp = []
                    for key in maps:
                        if (key[0] < key[1]):
                            keyApp = key
                        else:
                            keyApp = (key[1], key[0])

                        newList = []
                        for el in maps[key]:
                            if (el[0] < el[1]):
                                newList.append((el[0], el[1]))
                            else:
                                newList.append((el[1], el[0]))

                        mapsOrd[keyApp] = newList

                    # print("MapsOrd:",mapsOrd)

                    for key in mapsOrd:
                        # if vn == 2:
                        #     break
                        totMaps[(vn, key[0], key[1])] = mapsOrd[key]
                    print("Total mapping:", totMaps)

                    # todo: double check when the totCut will have empty values
                    cutsets = get_cutsets(vn, totCut)

                    # mapped={}
                    # for l in L.edges():
                    #    for key in mapping:
                    #        for el in key:
                    #            if(el[0]):
                    #                mapped[l] = el

                    # If at least a cut-set of a VN is down then that VN is disconnected
                    av = get_availability_cutsets(cutsets, mapsOrd)

                    vn_Maps_dic[vn] = mapsOrd
                    vn_CutSets_dic[vn] = cutsets

                    totAv += av

                    ####################### RESULTS ############################

                    numWave = 0
                    for path in maps:
                        for link in maps[path]:
                            numWave += 1
                    # print('Wavelength consumption of network',vn,':',numWave*2)

                    totW += numWave * 2



                else:
                    print('No survivable mapping')
            # End time
            time_elapsed = (time.time() - time_start)
            print("Computational time:", time_elapsed)

            totAv = get_availability_cutsets_total(totCut, totMaps)
            numWave = 0
            for path in totMaps:
                for link in totMaps[path]:
                    numWave += 1
            #Bidirectional links
            totW = numWave * 2

            physicalEdgeOccupiedCapacityOneOneDic = {}
            physicalEdgeOccupiedCapacityOneThreeDic = {}
            physicalEdgeOccupiedCapacityOneFiveDic = {}
            for cur_virtual_link in totMaps.keys():
                cur_path_physical_link_list = totMaps[cur_virtual_link]
                for cur_path_physical_link in cur_path_physical_link_list:
                    if cur_virtual_link[1] < cur_virtual_link[2]:
                        cur_path_required_capacityOneThree \
                            = virtualLinkRequirementOneThreeDic[datafile, cur_virtual_link[0], cur_virtual_link[1], cur_virtual_link[2]]
                        cur_path_required_capacityOneFive \
                            = virtualLinkRequirementOneFiveDic[datafile, cur_virtual_link[0], cur_virtual_link[1], cur_virtual_link[2]]
                    else:
                        cur_path_required_capacityOneThree \
                            = virtualLinkRequirementOneThreeDic[datafile, cur_virtual_link[0], cur_virtual_link[1], cur_virtual_link[2]]
                        cur_path_required_capacityOneFive \
                            = virtualLinkRequirementOneFiveDic[datafile, cur_virtual_link[0], cur_virtual_link[1], cur_virtual_link[2]]
                    # try:
                    if (cur_path_physical_link[0], cur_path_physical_link[1]) not in physicalEdgeOccupiedCapacityOneThreeDic.keys():
                        physicalEdgeOccupiedCapacityOneOneDic[cur_path_physical_link[0], cur_path_physical_link[1]] = 1
                        physicalEdgeOccupiedCapacityOneOneDic[cur_path_physical_link[1], cur_path_physical_link[0]] = 1
                        physicalEdgeOccupiedCapacityOneThreeDic[cur_path_physical_link[0], cur_path_physical_link[1]] = cur_path_required_capacityOneThree
                        physicalEdgeOccupiedCapacityOneThreeDic[cur_path_physical_link[1], cur_path_physical_link[0]] = cur_path_required_capacityOneThree
                        physicalEdgeOccupiedCapacityOneFiveDic[cur_path_physical_link[0], cur_path_physical_link[1]] = cur_path_required_capacityOneFive
                        physicalEdgeOccupiedCapacityOneFiveDic[cur_path_physical_link[1], cur_path_physical_link[0]] = cur_path_required_capacityOneFive
                    else:
                        physicalEdgeOccupiedCapacityOneOneDic[cur_path_physical_link[0], cur_path_physical_link[1]] += 1
                        physicalEdgeOccupiedCapacityOneOneDic[cur_path_physical_link[1], cur_path_physical_link[0]] += 1
                        physicalEdgeOccupiedCapacityOneThreeDic[cur_path_physical_link[0], cur_path_physical_link[1]] += cur_path_required_capacityOneThree
                        physicalEdgeOccupiedCapacityOneThreeDic[cur_path_physical_link[1], cur_path_physical_link[0]] += cur_path_required_capacityOneThree
                        physicalEdgeOccupiedCapacityOneFiveDic[cur_path_physical_link[0], cur_path_physical_link[1]] += cur_path_required_capacityOneFive
                        physicalEdgeOccupiedCapacityOneFiveDic[cur_path_physical_link[1], cur_path_physical_link[0]] += cur_path_required_capacityOneFive
                    # except Exception as e:
                    #     print(e)

            totalCapacityOneOne = sum(physicalEdgeOccupiedCapacityOneOneDic.values()) / 2
            totalCapacityOneThree = sum(physicalEdgeOccupiedCapacityOneThreeDic.values()) / 2
            totalCapacityOneFive = sum(physicalEdgeOccupiedCapacityOneFiveDic.values()) / 2
            maxCapacityOneOne = max(physicalEdgeOccupiedCapacityOneOneDic.values())
            maxCapacityOneThree = max(physicalEdgeOccupiedCapacityOneThreeDic.values())
            maxCapacityOneFive = max(physicalEdgeOccupiedCapacityOneFiveDic.values())

            cur_availability = round(totAv / ((num_vn * numFail)) * 100, 2)

            totNumVLwithSharing = 0
            averageNumVLwithSharing = 0

            results_folder = "results/german-SP-Capacity/"
            results_folder = results_folder + str(cur_num_vn) + "vn/" + str(cur_num_vl) + "vl/"
            # create the folder if it does not exist
            try:
                if not os.path.exists(results_folder):
                    os.makedirs(results_folder)
            except Exception as e:
                print("Error in creating the folder:", e)
            results_folder = results_folder + "scenario-" + str(scenario) + "_instance_" + str(datafile) + ".txt"
            with open(results_folder, 'w') as f:
                line = str(cur_availability) + " " + str(totW) + " " + str(totNumVLwithSharing)
                # line = line + " " + str(averageNumVLwithSharing) + " " + str(time_elapsed) + "\n"
                line = line + " " + str(averageNumVLwithSharing) + " " + str(time_elapsed)
                line = line + " " + str(totalCapacityOneOne) + " " + str(totalCapacityOneThree) + " " + str(totalCapacityOneFive)
                line = line + " " + str(maxCapacityOneOne) + " " + str(maxCapacityOneThree) + " " + str(maxCapacityOneFive)
                line = line + "\n"
                f.write(line)

        mean_av = sum_av / num_datafile
        mean_wave = sum_wave / num_datafile

        print("\n\n################ FINAL RESULTS ###################")
        print("\nMean Wavelengths Consumption", mean_wave)
        print("Min Wavelengths Consumption", min_wave)
        print("Max Wavelengths Consumption", max_wave)
        print("\nMean number of surviving VNs:", mean_av)
        print("Min number of surviving VNs:", min_av)
        print("Max number of surviving VNs:", max_av)
        print("\nMean Availability:", round(mean_av / ((num_vn * numFail)) * 100, 2))
        print("Min Availability:", round(min_av / ((num_vn * numFail)) * 100, 2))
        print("Max Availability:", round(max_av / ((num_vn * numFail)) * 100, 2))
