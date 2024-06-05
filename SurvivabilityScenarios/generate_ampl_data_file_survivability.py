import itertools
from collections import Counter

import networkx as nx
import random
import os
import copy
import time as time


def check_survivability_mapping(num_vn, virtual_link_list, physical_network_Graph: nx.Graph):
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

    #For each VN
    # todo: check if we find the routing of each VN separately without considering the other VNs
    # for vn in range(1, num_vn + 1):
    try:
        # Keys database (each virtual link must have a key)
        list_of_keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z']
        list_of_keys2 = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp',
                         'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz', 'ab', 'b2', 'cb', 'db', 'eb', 'fb',
                         'gb', 'hb', 'ib', 'jb', 'kb', 'lb', 'mb', 'nb', 'ob', 'pb', 'qb', 'rb', 'sb', 'tb', 'ub', 'vb',
                         'wb', 'xb', 'yb', 'zb']

        list_of_keys.extend(list_of_keys2)

        # L represents the logical network
        L = nx.MultiGraph()

        #read a logical network from file (vn is the number of the logical network that I want to read)
        # todo: initialize the logical network
        # read_logical_topology(vn, start_key, file_name)
        for l in range(len(virtual_link_list)):
            n1 = int(virtual_link_list[l][0])
            n2 = int(virtual_link_list[l][1])
            L.add_edge(n1, n2, key=list_of_keys[l])

        nodeTotal = nx.number_of_nodes(L)

        #Copies of the logical network (useful for the rest of the program)
        C = L.copy()
        Co = C.copy()
        Co2 = Co.copy()
        CP = C.copy()

        # todo: initialize the physical network
        # P is the physical network
        # P = nx.Graph()
        # read_physical_topology(file_name)
        P = copy.deepcopy(physical_network_Graph)

        #Shared spare slice
        SH = nx.MultiGraph()


        # needed for the creation of the new node
        def convert(liste):
            # Converting integer list to string list
            s = [str(i) for i in liste]
            # Join list items using join()
            #print("String list:",s)
            if (len(s) != 0):
                res = int("".join(s))
            else:
                res = s
            return (res)


        # function that subtract equal element from lists
        def Diff(li1, li2):
            li_dif = [i for i in li1 + li2 if i not in li2]
            return li_dif


        ##########-----------FUNCTION FOR REAL LINK----------###############
        nodes = C.edges()
        mapping = []
        var = True
        variable = False
        selfloop = False
        remainingCyTotal = []
        remainingCyTotalkey = []
        bad = False
        index2 = 0
        first = 0

        while nodes and variable is False:
            if bad is False:  # if bad is false mean that I don't need to restart from the beginning with a new cycle
                first += 1  # needed for keeping track of the first loop of each iteration
                Co = C.copy()  # copy of the real logical topology used to eliminate link without loosing keys
                cnodes = []  # nodes that are present in the current cycle
                LinkList2 = C.edges(keys=True)  # list of all edges of the contracted topology
                # translate dictionaries in list
                all_keys1 = []
                for i, j in LinkList2.items():  # I add the keys to each link
                    all_keys1.append(i)
                #print("Allkeys1:",all_keys1)

                cycle = []  # list that will contain all the cycles found in the network
                chiavi = []  # list of cycles but with real names
                concatenate = []  # DON'T REMEMBER
                # print(Co.edges(keys=True))
                iterator = 0  # keep track of the number of time I enter in if later because I need to enter only one time (correct the code to make it function correctly)
                Co2 = Co.copy()
                for u, v, k in Co2.edges(keys=True):  # for each edge in the edges list
                    #print("Stampo",u,v,Co2.edges())
                    lista = []
                    chiavina = []
                    linking = []
                    ########-----Self Loop management ----######
                    if (u == v):  # if source is equal to the destination
                        #print("Source equal to destination")
                        C.remove_nodes_from(
                            list(nx.isolates(C)))  # I remove all the isolated nodes that are left in the network
                        #
                        if len(C.nodes()) <= 1 and iterator < 1:  # if we have only one node we car operate on these self loops
                            iterator += 1
                            lista.append(u)
                            cycle.append(lista + lista)  # create the cycle
                            keyVector = []
                            for i, j, k in all_keys1:
                                keyVector.append(k)
                            #print("Key vector:",keyVector)
                            chiavi.append(keyVector)  # create the cycle with the real name of the links
                            #print("Chiavi:", chiavi)
                            selfloop = True  # boolean variable needed for close all the other possibilities
                            var = False  # we don't want to enter in the next while

                            # this is needed to get the real information of the nodes of the links that we are going to map on the physical topology
                            LinkList = L.edges(keys=True)  # list of edges of the logical network not contracted
                            #### translate dictionaries in list ###
                            all_keys2 = []
                            for i, j in LinkList.items():
                                all_keys2.append(i)

                            link = []
                            for j in keyVector:
                                link.append([i for i in all_keys2 if j in i])
                            # in link we have the real link of the logical corresponding to the key of the link in the loop
                            linksUsedInMapping = []

                            # map the reamining links in the self loop using a shortest path
                            for i in link:
                                for u, v, k in i:
                                    #print("Sto calcolando lo shortest path del link:", u,v,k)
                                    sp = nx.shortest_path(P, source=u, target=v,
                                                          weight='weight')  # I do the shortest path to map these links

                                    sp_links = []
                                    for jP in range(len(sp)):
                                        if jP < len(sp) - 1:
                                            sp_links.append((sp[jP], sp[jP + 1]))
                                            linksUsedInMapping.append((sp[jP], sp[jP + 1]))
                                    mapping.append(sp_links)
                                    #print("Shortest path links array:", sp_links)
                            variable = False
                            #print('No remaining links')


                    else:  # if it's not a self loop
                        flag = 0
                        added = 0
                        #print("Sto tentando di rimuovere", u, v, "da", Co.edges())
                        Co.remove_edge(u, v,
                                       key=k)  # in order to calculate loops I +remove a link and consider the shortest path to reach it
                        # in this way I'm sure to consider firstly the smallest loops possible
                        lista.append(u)

                        #print("Co.nodes:",Co.nodes())
                        #print("Co.edges:",Co.edges())
                        #try:
                        # todo: double check if we will have failure here
                        short = nx.shortest_path(Co, source=u, target=v)
                        #except:
                        #    Co.add_edge(u, v, key=k)
                        #    short = nx.shortest_path(Co,source=u, target=v)
                        #    added=1
                        cycle.append(short + lista)
                        #print("Shortest path da",u,"a",v,":", short)
                        #print("Cycle:",cycle)
                        #print("Co.edges (con un link eliminato):",Co.edges())
                        i = 0
                        whileshort = short + lista  # the loop that we are considering in the form [1 2 3 1] where 1,2,3 are nodes
                        #print('whileshort:',whileshort)
                        while i < len(whileshort) - 1:
                            #print('while short',whileshort[i:i+2])
                            linking.append(whileshort[i:i + 2])  # with this I take the links out of the loops
                            i = i + 1
                        #print("linking:",linking)
                        contractedLink = []
                        alllinks = []
                        if (added == 0):
                            Co.add_edge(u, v, key=k)  # I add anew the link that I eliminated before
                        #print("Aggiungo il link tolto prima, Co.edges:",Co.edges)
                        for r, j in Co.edges(keys=True).items():
                            alllinks.append(r)  # I create the list of link that are still in the contracted topology
                            #print("Link che sono rimasti nella topologia contratta:", alllinks)
                        #print("Linking:",linking)
                        for j in linking:
                            # print(j)
                            # I will use this in order to get the key to use in the logic network not contracted
                            # in order to get the real information of the link to be mapped
                            # find element that has that key in the list
                            # I connect the link of the cycle with their keys
                            contractedLink.append([i for i in alllinks if all(x in i for x in j)])

                        contractedLink2 = list(
                            contractedLink for contractedLink, _ in itertools.groupby(contractedLink))
                        contractedLink4 = list(contractedLink2[
                                                   0])  # I create this new variable in the case there are more then two links between a couple of nodes

                        #print("ContractedLink2:",contractedLink2)
                        #print("ContractedLink4:",contractedLink4)
                        contractedLink3 = []
                        if len(contractedLink4) > 2:  # check if there are more then two links
                            for u in range(len(linking)):
                                contractedLink3.append(contractedLink4[u])

                            flag = 1
                            #print("ContractedLink3:",contractedLink3)


                        else:
                            flag = 0

                        keyVector = []

                        # takes the keys of the link (their real name)
                        if flag == 0:  # if we are here means that we don't have more then two link per couple of nodes
                            #print("No more than two links per couple of nodes (flag=0)")
                            for x in contractedLink2:
                                for i, j, k in x:
                                    keyVector.append(k)
                            #print("KeyVector:",keyVector)
                            if len(keyVector) <= 1:  # it may happen that there's only a link in contractedLink2 so I protect it with this
                                cycle.remove(short + lista)  # I remove that cycle becouse it's clearly wrong

                            else:
                                chiavi.append(keyVector)  # otherwise I update the vector of cycle of keys
                                #print("Update delle chiavi:",chiavi)

                        else:  # if the flag is one I update the cycle from contractedLink3
                            for i, j, k in contractedLink3:
                                keyVector.append(k)
                            #print("KeyVector (flag=1):",keyVector)
                            chiavi.append(keyVector)
                            #print("Chiavi:",chiavi)
                        #print(chiavi)

                    if selfloop is True:
                        nodes = []
                #print('')
            if bad is True:
                #print('returned back to the beginning')

                C = L.copy()
                Co = C.copy()
                mapping = []
                if cycle:
                    cycle = remainingCyTotal
                    chiavi = remainingCyTotalkey
                first = 0
                LinkList2 = C.edges(keys=True)
                # translate dictionaries in list
                all_keys1 = []
                for i, j in LinkList2.items():
                    all_keys1.append(i)

            # here I placed a while that say: if that cycle cannot be mapped disjointly I have to consider other cycles
            # subtracting cycles already considered
            if selfloop is False:
                var = True
            while var is True:
                #If cycle is not empty
                # todo: check if it's the smart algorithm
                if cycle:
                    #print("Cycle:",cycle)
                    mincycle = min(cycle, key=len)  # elected cycle that is the min
                    #print("Min cycle selected", mincycle)
                    mincyclekey = min(chiavi, key=len)

                    cnodes = list(dict.fromkeys(mincycle))  # nodes that are in the cycle
                    # I subtract the cycle from the available cycles (I need to consider the cycle in both directions)
                    remainingCy = Diff(cycle, [mincycle])
                    remainingCy = Diff(remainingCy, [list(reversed(mincycle))])
                    cycle = remainingCy
                    #print("Remaining cycles:",cycle)
                    #print("RemainingCycle:",remainingCy)

                    remainingCyKey = Diff(chiavi, [mincyclekey])
                    remainingCyKey = Diff(remainingCyKey, [list(reversed(mincyclekey))])
                    chiavi = remainingCyKey
                    #print("Chiavi:",chiavi)
                    #print("RemainingCycleKeys:",remainingCyKey)

                    if first == 1:  # store the remaining loops of first loops of each main iteration
                        remainingCyTotal = remainingCy
                        remainingCyTotalkey = remainingCyKey
                    i = 0
                    #print("RemainingCycleTotal:",remainingCyTotal)

                    contractedLink = []

                    for j in mincyclekey:
                        #print('element of mincycle key', j)
                        # I will use this in order to get the key to use in the logic network not contracted
                        # in order to get the real information of the link to be mapped
                        # find element that has that key in the list
                        # I connect the link of the cycle with their keys
                        #print("All keys1:",all_keys1)
                        contractedLink.append([i for i in all_keys1 if all(x in i for x in j)])
                        # contractedLink.append([i for i in all_keys1 if all(x in i for x in j)])
                    contractedLink2 = list(contractedLink for contractedLink, _ in itertools.groupby(contractedLink))
                    #print("Contracted links of the min cycle:",contractedLink)
                    #print('new way of represent, contractedLink2:', contractedLink2)
                    keyVector = mincyclekey

                    # takes the keys of the link (their real name)

                    #print('Real name of link in the cycle (key), keyVector:', keyVector)

                    LinkList = L.edges(keys=True)
                    #### translate dictionaries in list ###
                    all_keys2 = []
                    for i, j in LinkList.items():
                        all_keys2.append(i)

                    link = []
                    for j in keyVector:
                        link.append([i for i in all_keys2 if j in i])
                    #print('mapping link in disjoint way:', link)

                    #########################################################
                    ########---Mapping of links in disjoint way----###########
                    #########################################################

                    link2 = []
                    link2_back = []
                    for i in link:
                        for u, v, k in i:
                            link2.append((u, v))
                    #print('mapping link in disjoint way', link2)
                    end = 1
                    disjoint = 0
                    trials = 0
                    linksAumentedWeight = []
                    while end and trials < 60:
                        mappingShortest = []
                        linksUsedInMapping = []

                        for i in link2:
                            # shortest path to map the links
                            #print("P.edges:",P.edges())
                            sp = nx.shortest_path(P, source=i[0], target=i[1],
                                                  weight='weight')
                            sp_links = []
                            # convert the nodal form in a link form
                            for jP in range(len(sp)):
                                if jP < len(sp) - 1:
                                    sp_links.append((sp[jP], sp[jP + 1]))
                                    linksUsedInMapping.append((sp[jP], sp[jP + 1]))

                            mappingShortest.append(sp_links)
                        #print("Mapping shortest:",mappingShortest)

                        method = 2
                        if (method == 1):
                            # find how many time a physical link is used in the mapping to identify if it is disjoint
                            occurances = Counter(linksUsedInMapping)

                            disjoint = 1
                            for linkSelected, times in occurances.items():
                                if times > 1:
                                    P[linkSelected[0]][linkSelected[1]]['weight'] = P[linkSelected[0]][linkSelected[1]][
                                                                                        'weight'] + 1
                                    disjoint = 0
                        else:
                            #Count the occurances to understand if the mapping is survivable
                            occurances = {}
                            for lis in mappingShortest:
                                for link in lis:
                                    occurances[link] = 0
                            for lis in mappingShortest:
                                for link in lis:
                                    occurances[link] += 1
                                    if ((link[1], link[0]) in occurances):
                                        occurances[(link[1], link[0])] += 1

                            disjoint = 1
                            for linkSelected in occurances:
                                if occurances[linkSelected] > 1:
                                    if (linkSelected[1], linkSelected[0]) not in linksAumentedWeight:
                                        P[linkSelected[0]][linkSelected[1]]['weight'] = \
                                            P[linkSelected[0]][linkSelected[1]]['weight'] + 1
                                        linksAumentedWeight.append(linkSelected)
                                    disjoint = 0
                            #print("Links Aumented Weight",linksAumentedWeight)
                            #Save variables of the first trial, useful if the mapping does not converge
                            if (trials == 0):
                                linksAumentedWeight_back = []
                                mappingShortest_back = []
                                link2_back = []
                                #cycle_back=cycle
                                linksAumentedWeight_back = linksAumentedWeight.copy()
                                mappingShortest_back = mappingShortest.copy()
                                link2_back = link2.copy()
                                mapping_back = mapping.copy()
                                #print("\n\nCYCLE:",cycle_back)
                                #print("\n\nLinksAumented:",linksAumentedWeight_back)
                                #print("\n\nMappingShortest:",mappingShortest_back)

                        if disjoint:
                            #print("DISJOINT MAPPING FOUND")
                            end = 0
                            for node1, node2 in P.edges():
                                P[node1][node2]['weight'] = 1
                            variable = False
                            var = False
                        else:
                            #print("Incrementing trials")
                            trials = trials + 1
                else:
                    #print("CYCLE EMPTY, SMART DOES NOT CONVERGE")
                    if (True):
                        #Find an alternative path only to one of the requests that share some physical links
                        alt_trials = 0
                        ok = True
                        P2 = P.copy()
                        #print("\nLinks Aumented:",linksAumentedWeight_back)
                        #print("\nMappingShortest:",mappingShortest_back)
                        #print("\nLink 2 Back",link2_back)

                        altVirLink = []
                        pos = 0
                        #these cycles save in a list the virtual links that in the first trial of the precedent cycle are not mapped disjointly
                        for l in link2_back:
                            for l2 in linksAumentedWeight_back:
                                if (l2 in mappingShortest_back[pos] or (l2[1], l2[0]) in mappingShortest_back[pos]):
                                    if (l not in altVirLink):
                                        altVirLink.append(l)
                            pos += 1

                        #print("\nAlternative virtual links:",altVirLink)

                        while ok and alt_trials < 60:
                            mappingShortest_back2 = []

                            for l in mappingShortest_back:
                                mappingShortest_back2.append(l)

                            for link in altVirLink:

                                #print("Mapping the virtual link:",link)
                                sp = nx.shortest_path(P2, source=link[0], target=link[1],
                                                      weight='weight')

                                sp_links = []
                                # convert the nodal form in a link form
                                for jP in range(len(sp)):
                                    if jP < len(sp) - 1:
                                        sp_links.append((sp[jP], sp[jP + 1]))

                                #print("Sp links:",sp_links)

                                #Increment the weight of links already used
                                for l in sp_links:
                                    P2[l[0]][l[1]]['weight'] = P2[l[0]][l[1]]['weight'] + 10

                                count = 0
                                for i in link2_back:
                                    #print("i e link:",i,link)
                                    if i == link or (i[1], i[0]) == link:
                                        #print("Substitute mapping")
                                        mappingShortest_back2[count] = sp_links
                                    count += 1
                                #print("Alternative mapping shortest:",mappingShortest_back2)

                            #Count occurances to discover if the mapping is a disjoint mapping (if occurances>1 at least one time, the mapping is not disjoint)
                            occurances = {}
                            for lis in mappingShortest_back2:
                                for link in lis:
                                    occurances[link] = 0
                            for lis in mappingShortest_back2:
                                for link in lis:
                                    occurances[link] += 1
                                    if ((link[1], link[0]) in occurances):
                                        occurances[(link[1], link[0])] += 1
                            #print("Occurances:",occurances)

                            disjoint = 1
                            for linkSelected in occurances:
                                if occurances[linkSelected] > 1:
                                    if (linkSelected[1], linkSelected[0]) not in linksAumentedWeight:
                                        P2[linkSelected[0]][linkSelected[1]]['weight'] = \
                                            P2[linkSelected[0]][linkSelected[1]]['weight'] + 1
                                        #print("Weigth of edge",linkSelected,":",P2[linkSelected[0]][linkSelected[1]]['weight'])
                                    disjoint = 0

                            if (disjoint == 0):
                                alt_trials += 1
                            else:
                                ok = False

                        if disjoint:
                            end = 0
                            #print("mapping shortest back 2",mappingShortest_back2)
                            mappingShortest = mappingShortest_back2.copy()
                        else:
                            ################ SECOND ALTERNATIVE METHOD ###############################
                            #If the program arrives here, it means that some virtual links cannot be mapped in a disjoint way with the precedent methods
                            #Then, here the program try to map the disjoint links of a cycle selecting a physical path for each virtual link and avoiding the use
                            #of physical links used for the mapping of other virtual links (basically the physical links already used for a virtual link are removed from the physical graph)

                            mappingShortest_back2 = []
                            #print("Mapping shortest back", mappingShortest_back)

                            usedPhyLink = []
                            pos = 0
                            #Find which physical links are already used
                            for l in link2_back:
                                if (l not in altVirLink):
                                    #print("Mapping shortest back [pos]",mappingShortest_back[pos])
                                    for l2 in mappingShortest_back[pos]:
                                        if (l2 not in usedPhyLink):
                                            usedPhyLink.append(l2)
                                pos += 1

                            #print("Used phy links",usedPhyLink)

                            #Remove physical links used from the physical graph
                            for l in usedPhyLink:
                                P2.remove_edge(l[0], l[1])
                            #print("P2.edges()",P2.edges())

                            mappingShortest_back2 = mappingShortest_back.copy()
                            num_error_finding_path = 0
                            for link in altVirLink:

                                #print("Mapping of virtual link:",link)
                                #print("P2.edges:",P2.edges())
                                # try:
                                sp = nx.shortest_path(P2, source=link[0], target=link[1],
                                                      weight='weight')
                                # except Exception as e:
                                #     print("Error finding the path")
                                #     num_error_finding_path += 1
                                #     continue
                                #     # assert "No path found"

                                sp_links = []
                                # convert the nodal form in a link form
                                for jP in range(len(sp)):
                                    if jP < len(sp) - 1:
                                        sp_links.append((sp[jP], sp[jP + 1]))

                                #print("Sp links:",sp_links)

                                #Remove links used
                                for l in sp_links:
                                    P2.remove_edge(l[0], l[1])

                                count = 0
                                for i in link2_back:
                                    #print("i e link:",i,link)
                                    if i == link or (i[1], i[0]) == link:
                                        #print("Substitute mapping")
                                        mappingShortest_back2[count] = sp_links
                                    count += 1
                                #print("Alternative mapping shortest:",mappingShortest_back2)

                            if num_error_finding_path > 0:
                                continue

                            #Count occurances of the new mapping
                            occurances = {}
                            for lis in mappingShortest_back2:
                                for link in lis:
                                    occurances[link] = 0
                            for lis in mappingShortest_back2:
                                for link in lis:
                                    occurances[link] += 1
                                    if ((link[1], link[0]) in occurances):
                                        occurances[(link[1], link[0])] += 1
                            #print("Occurances:",occurances)

                            #If a mapping is found, it is not possible to have some virtual links not mapped in a disjoint way
                            disjoint = 1
                            for linkSelected in occurances:
                                if occurances[linkSelected] > 1:
                                    #print("NOT POSSIBLE TO ARRIVE HERE")
                                    if (linkSelected[1], linkSelected[0]) not in linksAumentedWeight:
                                        P2[linkSelected[0]][linkSelected[1]]['weight'] = \
                                            P2[linkSelected[0]][linkSelected[1]]['weight'] + 1
                                        #print("Weigth of edge",linkSelected,":",P2[linkSelected[0]][linkSelected[1]]['weight'])
                                    disjoint = 0

                            if disjoint:
                                end = 0
                                #print("mapping shortest back 2",mappingShortest_back2)
                                mappingShortest = mappingShortest_back2.copy()

                        #Reset the weigth of each physical link to 1
                        P2 = P.copy()
                        for node1, node2 in P.edges():
                            P2[node1][node2]['weight'] = 1
                        variable = False
                        var = False

                        mapping = mapping_back.copy()
                        #print("mapping",mapping)

                if end == 0:
                    #print('mapped loop', mappingShortest)
                    for linkMapped in mappingShortest:
                        mapping.append(linkMapped)
                    #print("mapping at the end",mapping)
                else:
                    for node1, node2 in P.edges():
                        P[node1][node2]['weight'] = 1
                    #print('NO DISJOINT MAPPING FOUND Select a new cycle')

                ###########################################################################################

                # identify remaining links and nodes and build new node
                if var is False and selfloop is False:
                    #print("Identify remaining links and nodes")
                    #print("C.edges:",C.edges())
                    #print("CP.edges:",CP.edges())
                    #print("contractedLink2",contractedLink2)
                    for i in contractedLink2:
                        for u, v, k in i:
                            try:
                                C.remove_edge(u, v, key=k)
                            except:
                                C = CP.copy()
                                C.remove_edge(u, v, key=k)
                    clink = []
                    #print('cnodes', cnodes)
                    index3 = 0
                    Co = C.copy()
                    for i in cnodes:
                        #print("Node i",i)
                        edges = list(Co.edges(i, keys=True))
                        #print("edges:",edges)
                        for u, v, k in edges:
                            Co.remove_edge(u, v, key=k)
                        #print("Co.edges:",Co.edges)
                        clink.append(edges)

                    #if len(clink) > 0:
                    #    print('link connected to nodes of cycle', clink)
                    #else:
                    #    print('No link connected to the nodes of the cycle')

                    newNode = convert(cnodes)

                    ed = []
                    for i in clink:
                        for j in i:
                            ed.append(j)
                    nestedList = [list(i) for i in ed]
                    #print("Nested List:",nestedList)

                    for i, j, k in nestedList:
                        if i in cnodes and j in cnodes:
                            C.remove_edge(i, j)  # k)
                            C.add_edge(newNode, newNode, key=k)

                        elif i in cnodes and j not in cnodes:

                            if nodeTotal == len(str(abs(newNode))):
                                C.add_edge(newNode, newNode, key=k)

                                C.remove_edge(i, j)
                            else:
                                C.add_edge(newNode, j, key=k)

                                C.remove_edge(i, j)
                    if len(nestedList) > 0:
                        #print('Remaining links', C.edges(keys=True))
                        CP = C.copy()
                    #else:
                    #print('\n\nNo remaining links')

                if var is False:
                    bad = False
                if len(remainingCy) < 1 and var is True:
                    var = False
                    #print("Remaining",remainingCy)
                    variable = False
                    bad = True
                    index2 += 1
            if selfloop is False:
                nodes = C.edges()
    except Exception as e:
        print("Error in the mapping of the virtual network", e)
        return False
    return True


def canonical_cycle(permutation):
    """Convert permutation to its canonical form (smallest lexicographical rotation)."""
    n = len(permutation)
    return min(permutation[i:] + permutation[:i] for i in range(n))


def generate_unique_cycles(k):
    nodes = list(range(k))
    all_cycles = set()

    # Generate permutations of k-1 nodes, keeping one node fixed
    for perm in itertools.permutations(nodes[1:]):
        # Create the full cycle including the fixed node
        cycle = (nodes[0],) + perm

        # Check and add the canonical form of the cycle
        canonical = canonical_cycle(cycle)
        reversed_canonical = canonical_cycle(canonical[::-1])
        if canonical < reversed_canonical:
            all_cycles.add(canonical)
        else:
            all_cycles.add(reversed_canonical)

    return all_cycles


class NetworkEnvironment:
    def __init__(self, num_physical_nodes, physical_link_list, num_virtual_network, num_virtual_nodes,
                 num_virtual_links):
        self.physical_network_Graph = nx.Graph()
        self.initialize_physical_network(physical_link_list)
        self.num_physical_nodes = num_physical_nodes
        self.physical_nodes_list = list(range(1, num_physical_nodes + 1))

        self.num_virtual_network = num_virtual_network
        self.num_virtual_nodes = num_virtual_nodes
        self.num_virtual_links = num_virtual_links

        self.virtual_nodes_list_dict = {}
        self.virtual_links_list_dict = {}
        self.virtual_links_to_add_list_dict = {}

        self.initialize_virtual_networks_survivable()

    def initialize_physical_network(self, physical_link_list: list):
        for link in physical_link_list:
            self.physical_network_Graph.add_edge(link[0], link[1], weight=1)

    def get_survivable_ring_link_list(self, cur_num_virtual_nodes):
        virtual_nodes_list = random.sample(self.physical_nodes_list, cur_num_virtual_nodes)
        virtual_nodes_list.sort()
        unique_cycles = generate_unique_cycles(len(virtual_nodes_list))
        for cycle in unique_cycles:
            cur_virtual_nodes_ring = [virtual_nodes_list[i] for i in cycle]
            cur_virtual_links_ring = []
            for i in range(0, len(cur_virtual_nodes_ring) - 1):
                # node left shoud be less than node right
                if cur_virtual_nodes_ring[i] < cur_virtual_nodes_ring[i + 1]:
                    node_left = cur_virtual_nodes_ring[i]
                    node_right = cur_virtual_nodes_ring[i + 1]
                else:
                    node_left = cur_virtual_nodes_ring[i + 1]
                    node_right = cur_virtual_nodes_ring[i]
                cur_virtual_links_ring.append((node_left, node_right))
            if cur_virtual_nodes_ring[0] < cur_virtual_nodes_ring[-1]:
                node_left = cur_virtual_nodes_ring[0]
                node_right = cur_virtual_nodes_ring[-1]
            else:
                node_left = cur_virtual_nodes_ring[-1]
                node_right = cur_virtual_nodes_ring[0]
            cur_virtual_links_ring.append((node_left, node_right))

            survivability_mapping_flag = check_survivability_mapping(num_vn=self.num_virtual_network,
                                                                     virtual_link_list=cur_virtual_links_ring,
                                                                     physical_network_Graph=self.physical_network_Graph)
            if survivability_mapping_flag:
                return True, virtual_nodes_list, cur_virtual_links_ring
        return False, [], []

    def initialize_virtual_networks_survivable(self):
        for i in range(1, self.num_virtual_network + 1):
            survivability_flag = False
            cur_virtual_links_ring = []
            cur_virtual_nodes_list = []
            while not survivability_flag:
                survivability_flag, cur_virtual_nodes_list, cur_virtual_links_ring \
                    = self.get_survivable_ring_link_list(cur_num_virtual_nodes=self.num_virtual_nodes)
            if len(cur_virtual_links_ring) == 0:
                raise Exception("Error: No survivable virtual network found")
            self.virtual_nodes_list_dict[i] = copy.deepcopy(cur_virtual_nodes_list)
            self.virtual_links_list_dict[i] = copy.deepcopy(cur_virtual_links_ring)

            # get all possible links
            self.virtual_links_to_add_list_dict[i] = []
            for node_index in range(0, len(self.virtual_nodes_list_dict[i])):
                for node_index2 in range(node_index+1, len(self.virtual_nodes_list_dict[i])):
                    if self.virtual_nodes_list_dict[i][node_index] < self.virtual_nodes_list_dict[i][node_index2]:
                        left_node = self.virtual_nodes_list_dict[i][node_index]
                        right_node = self.virtual_nodes_list_dict[i][node_index2]
                    else:
                        left_node = self.virtual_nodes_list_dict[i][node_index2]
                        right_node = self.virtual_nodes_list_dict[i][node_index]
                    # check if the link is already in the list
                    if (left_node, right_node) not in self.virtual_links_list_dict[i]:
                        self.virtual_links_to_add_list_dict[i].append((left_node, right_node))
            num_virtual_links_to_add = self.num_virtual_links - len(self.virtual_links_list_dict[i])
            virtual_links_to_add_list = random.sample(self.virtual_links_to_add_list_dict[i], num_virtual_links_to_add)
            self.virtual_links_list_dict[i].extend(virtual_links_to_add_list)
            # remove the sample links from the list of links to add
            for link in virtual_links_to_add_list:
                self.virtual_links_to_add_list_dict[i].remove(link)

    def initialize_virtual_networks(self):
        for i in range(1, self.num_virtual_network+1):
            # randomly select self.num_virtual_nodes nodes from self.physical_nodes_list
            self.virtual_nodes_list_dict[i] = random.sample(self.physical_nodes_list, self.num_virtual_nodes)
            # order the nodes list
            self.virtual_links_list_dict[i] = []
            for node_index in range(0, len(self.virtual_nodes_list_dict[i])-1):
                node_index2 = node_index + 1
                # add the link where the left node should be less than the right node
                if self.virtual_nodes_list_dict[i][node_index] < self.virtual_nodes_list_dict[i][node_index2]:
                    left_node = self.virtual_nodes_list_dict[i][node_index]
                    right_node = self.virtual_nodes_list_dict[i][node_index2]
                else:
                    left_node = self.virtual_nodes_list_dict[i][node_index2]
                    right_node = self.virtual_nodes_list_dict[i][node_index]
                self.virtual_links_list_dict[i].append((left_node, right_node))
            if self.virtual_nodes_list_dict[i][0] < self.virtual_nodes_list_dict[i][-1]:
                left_node = self.virtual_nodes_list_dict[i][0]
                right_node = self.virtual_nodes_list_dict[i][-1]
            else:
                left_node = self.virtual_nodes_list_dict[i][-1]
                right_node = self.virtual_nodes_list_dict[i][0]
            self.virtual_links_list_dict[i].append((left_node, right_node))
            self.virtual_nodes_list_dict[i].sort()
            # get all possible links
            self.virtual_links_to_add_list_dict[i] = []
            for node_index in range(0, len(self.virtual_nodes_list_dict[i])):
                for node_index2 in range(node_index+1, len(self.virtual_nodes_list_dict[i])):
                    if self.virtual_nodes_list_dict[i][node_index] < self.virtual_nodes_list_dict[i][node_index2]:
                        left_node = self.virtual_nodes_list_dict[i][node_index]
                        right_node = self.virtual_nodes_list_dict[i][node_index2]
                    else:
                        left_node = self.virtual_nodes_list_dict[i][node_index2]
                        right_node = self.virtual_nodes_list_dict[i][node_index]
                    # check if the link is already in the list
                    if (left_node, right_node) not in self.virtual_links_list_dict[i]:
                        self.virtual_links_to_add_list_dict[i].append((left_node, right_node))
            num_virtual_links_to_add = self.num_virtual_links - len(self.virtual_links_list_dict[i])
            virtual_links_to_add_list = random.sample(self.virtual_links_to_add_list_dict[i], num_virtual_links_to_add)
            self.virtual_links_list_dict[i].extend(virtual_links_to_add_list)
            # remove the sample links from the list of links to add
            for link in virtual_links_to_add_list:
                self.virtual_links_to_add_list_dict[i].remove(link)

    def add_virtual_links(self, num_virtual_links_to_add, new_link_flag=True):
        for i in range(1, self.num_virtual_network + 1):
            # sample additional links so the number of links is equal to self.num_virtual_links
            virtual_links_to_add_list = random.sample(self.virtual_links_to_add_list_dict[i], num_virtual_links_to_add)
            self.virtual_links_list_dict[i].extend(virtual_links_to_add_list)
            # remove the sample links from the list of links to add
            for link in virtual_links_to_add_list:
                self.virtual_links_to_add_list_dict[i].remove(link)
        if new_link_flag:
            self.num_virtual_links += num_virtual_links_to_add


if __name__ == '__main__':
    physical_topology = "tokyo"
    num_physical_nodes = 23
    # (1,2) (1,3) (1,4) (1,5) (1,6) (2,3) (2,8) (3,13) (3,9) (4,5) (4,13) (4,14) (4,16) (5,16) (5,18) (6,7) (6,18) (7,8) (7,21) (7,22) (7,23) (8,23) (9,10) (9,11) (9,13) (10,11) (10,12) (10,13) (11,12) (12,13) (12,15) (14,15) (14,20) (15,20) (16,17) (16,19) (16,20) (17,18) (17,19) (18,21) (19,20) (21,22) (22,23)
    physical_link_list = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 8), (3, 13), (3, 9), (4, 5), (4, 13),
                          (4, 14), (4, 16), (5, 16), (5, 18), (6, 7), (6, 18), (7, 8), (7, 21), (7, 22), (7, 23),
                          (8, 23), (9, 10), (9, 11), (9, 13), (10, 11), (10, 12), (10, 13), (11, 12), (12, 13),
                          (12, 15), (14, 15), (14, 20), (15, 20), (16, 17), (16, 19), (16, 20), (17, 18), (17, 19),
                          (18, 21), (19, 20), (21, 22), (22, 23)]
    # num_virtual_network_list = [6, 12, 18, 24, 30]
    num_virtual_network_list = [5, 10, 15, 20, 25]
    num_virtual_nodes = 6
    num_virtual_link_min = num_virtual_nodes
    num_virtual_link_max = int(num_virtual_nodes * (num_virtual_nodes - 1) / 2)
    for num_virtual_network in num_virtual_network_list:
        for i in range(1, 11):
            network_environment = NetworkEnvironment(num_physical_nodes=num_physical_nodes,
                                                     physical_link_list=physical_link_list,
                                                     num_virtual_network=num_virtual_network,
                                                     num_virtual_nodes=num_virtual_nodes,
                                                     num_virtual_links=num_virtual_link_min)
            for j in range(num_virtual_link_min, num_virtual_link_max+1):
                folder_name = ("DatafilesNew/" + physical_topology + "/" + str(num_virtual_network)
                               + "vn/" + str(j) + "vl/")
                # create the folder if it does not exist
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                file_name = (folder_name + "DataFile" + str(i) + ".dat")
                # write the data to the file
                with open(file_name, "w") as file:
                    file.write("data;\n\n")
                    file.write("param num_top:=" + str(num_virtual_network) + ";\n\n")
                    file.write("#nodes and edges of the physical network\n")
                    file.write("param n := 23;\n\n")

                    file.write("set E := (1,2) (1,3) (1,4) (1,5) (1,6) (2,3) (2,8) (3,13) (3,9) (4,5) (4,13) (4,14) (4,16) (5,16) (5,18) (6,7) (6,18) (7,8) (7,21) (7,22) (7,23) (8,23) (9,10) (9,11) (9,13) (10,11) (10,12) (10,13) (11,12) (12,13) (12,15) (14,15) (14,20) (15,20) (16,17) (16,19) (16,20) (17,18) (17,19) (18,21) (19,20) (21,22) (22,23) ;\n\n")
                    file.write("#nodes and edges of the virtual networks\n")
                    for virtual_network_index in range(1, num_virtual_network+1):
                        # write the list of nodes
                        line = "set Nl[" + str(virtual_network_index) + "] := "
                        virtual_nodes_list = network_environment.virtual_nodes_list_dict[virtual_network_index]
                        line += " ".join(str(node) for node in virtual_nodes_list)
                        line += ";\n"
                        file.write(line)
                    file.write("\n")
                    for virtual_network_index in range(1, num_virtual_network+1):
                        line = "set El[" + str(virtual_network_index) + "] := "
                        virtual_links_list = network_environment.virtual_links_list_dict[virtual_network_index]
                        # line += " ".join(str(link) for link in virtual_links_list)
                        line += " ".join("("+str(link[0])+","+str(link[1])+")" for link in virtual_links_list)
                        line += ";\n"
                        file.write(line)
                if j < num_virtual_link_max:
                    network_environment.add_virtual_links(1)
