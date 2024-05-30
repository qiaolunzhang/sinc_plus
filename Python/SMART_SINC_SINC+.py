# SMART ALGORITHM FOR SURVIVABILITY

import networkx as nx
import random
import itertools
from collections import Counter
import time as time


#Function to read the number of virtual networks that is a value present in the data file
#The value with the number of VNs is read in a specific position in the data file
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
def read_logical_topology(top, start_key, file_name):
    #datafile = 'Ring4Node-' + str(datfileinstance+1) + '.dat'
    datafile = file_name
    num_logical_links = 0

    data = open(datafile, "r")
    data.readline()
    data.readline()
    line = data.readline()
    app = line.split("=")
    app2 = str(app[1]).split(";")
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
        CB.add_edge(n1, n2, key=list_of_keys[start_key + l])
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
    cutsets.pop(cont - 1)
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
                if (el == df[0]):
                    virLinksDown.append(key)
                elif (el == df[1]):
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
                for el in totMaps[key]:
                    if (el == df[0]):
                        virLinksDown.append(key)
                    elif (el == df[1]):
                        virLinksDown.append(key)
            #print("Physical links down",df[0],df[1],"-> Virtual links down:",virLinksDown)

            found = 0
            #find if at least a cut-set of the VN is down
            for cts in totCut:
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


#Compute the availability allowing inter-VN capacity sharing
def get_availability_gateways(totMaps):
    numFail = 0
    av = {}
    for df in DF:
        #for each double failure find down virtual links
        virLinksDown = []
        for key in totMaps:
            for el in totMaps[key]:
                if (el == df[0] and key not in virLinksDown):
                    virLinksDown.append(key)
                elif (el == df[1] and key not in virLinksDown):
                    virLinksDown.append(key)
        #print("Physical links down",df[0],df[1],"-> Virtual links down:",virLinksDown)

        CB2 = CB.copy()
        #print("CB edges:",CB.edges())
        #print("CB2 edges:",CB2.edges())
        #Remove failing links from the copy of the combined network
        for link in virLinksDown:
            if ((link[1], link[2]) in CB2.edges()):
                CB2.remove_edge(link[1], link[2])
            else:
                CB2.remove_edge(link[2], link[1])

        #print("Virtual links down:",virLinksDown)

        found = [0 for i in range(1, num_vn + 1)]
        #print("Found:",found)
        #Find a path of each disconnected virtual link over the combined network (without failing links)
        for req in virLinksDown:
            try:
                sp = nx.shortest_path(CB2, req[1], req[2])
            except nx.NetworkXNoPath:
                #print("No path found for request",req,"with failure",numFail,":",df)
                found[req[0] - 1] = 1
            #else:
            #print("Shortest path from",req[1],"to",req[2],"is:",sp)

        #If at least a disconnected virtual link cannot be reconnected through a path on the combined network, then its VN is disconnected (and av=1)
        for vn in range(1, num_vn + 1):
            if (found[vn - 1] == 1):
                av[vn, numFail] = 1
            else:
                av[vn, numFail] = 0

        numFail += 1
    #print("AV:",av)
    totFail = sum(av.values())
    totAvGw = numFail * num_vn - totFail
    #print("NumFail:",numFail)
    #print("TotFail:",totFail)
    #print("Availability with gateways:",totAvGw)
    return totAvGw


#Compute the availability allowing inter-VN capacity sharing and spare slice sharing
def get_availability_gateways_shared_slice(totMaps, shMaps):
    numFail = 0
    av = {}
    for df in DF:
        #for each double failure find down virtual links
        virLinksDown = []
        for key in totMaps:
            for el in totMaps[key]:
                if (el == df[0] and key not in virLinksDown):
                    virLinksDown.append(key)
                elif (el == df[1] and key not in virLinksDown):
                    virLinksDown.append(key)
        #print("Physical links down",df[0],df[1],"-> Virtual links down:",virLinksDown)

        CB2 = CB.copy()
        #print("CB edges:",CB.edges())
        #print("CB2 edges:",CB2.edges())
        for link in virLinksDown:
            if ((link[1], link[2]) in CB2.edges()):
                CB2.remove_edge(link[1], link[2])
            else:
                CB2.remove_edge(link[2], link[1])

        #print("Virtual links down:",virLinksDown)

        found = [0 for i in range(1, num_vn + 1)]
        #print("Found:",found)
        #Appluy inter-VN capacity sharing to reconnect disconnected virtual links through a path over the combined VN
        for req in virLinksDown:
            #Try to find a path in the combined virtual network
            try:
                sp = nx.shortest_path(CB2, req[1], req[2])
            except nx.NetworkXNoPath:
                #print("No path found for request",req,"with failure",numFail,":",df)
                dummy = True

                #If no path is found with inter-VN capacity sharing, then apply spare slice sharing

                #SPARE SLICE SHARING
                #Compute spare slice links that are down
                shLinksDown = []
                for key in shMaps:
                    for el in shMaps[key]:
                        #print("Sto confrontando:",el,"con",df[0],"e",df[1])
                        if (el == df[0] and key not in shLinksDown):
                            shLinksDown.append(key)
                        elif (el == df[1] and key not in shLinksDown):
                            shLinksDown.append(key)

                #Add spare slice links not down to the combined network
                for l in SH.edges():
                    if (l not in shLinksDown):
                        CB2.add_edge(l[0], l[1])

                link_add = 0
                #Try to route virtual request through combined network + shared spare slice 
                try:
                    sp = nx.shortest_path(CB2, req[1], req[2])
                except:
                    link_add = 1

                #Map the new edge in the physical network
                P2 = P.copy()
                #remove physical edges down (the mapping of the link must not use down links)
                for pl in df:
                    P2.remove_edge(pl[0], pl[1])
                #Mapping of the new added edge (the only constraint is not to use failing links)
                try:
                    phy_sp = nx.shortest_path(P2, req[1], req[2])
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

                    shMaps[(req[1], req[2])] = sp_links

                    if (link_add == 1):
                        #Add the new edge in the shared slice
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

    return totAvGw


#Function that tries to map a virtual link of a VN over a different path on the physical network (different means that at least a physical link must differs w.r.t. initial mapping)
def different_mapping(totMaps, link, totCut, totAv, wave, scenario):
    for plink in totMaps[link]:
        P2 = P.copy()
        trials = 0
        while trials < 1:
            mapping = []

            #if(trials==0):
            #print("Link",plink)
            #Increment the weight of each physical link (once at time) already used to allow to find a disjoint mapping 
            P2[plink[0]][plink[1]]['weight'] += 10
            sp = nx.shortest_path(P2, source=link[1], target=link[2],
                                  weight='weight')
            sp_links = []
            for jP in range(len(sp)):
                if jP < len(sp) - 1:
                    sp_links.append((sp[jP], sp[jP + 1]))
                    linksUsedInMapping.append((sp[jP], sp[jP + 1]))
            mapping.append(sp_links)
            #print("Mapping:",mapping[0])

            newMap = totMaps.copy()
            #for l in totMaps:
            #    newMap[l]=totMaps[l]

            newMap[link] = mapping[0]
            #Verify if the new mapping is survivable
            surv = verify_survivability(newMap, totCut)
            if (surv == True):
                #print("SURVIVABLE MAPPING")
                #print("Link",link,"mapped on new path",mapping)

                #Compute the new availability value
                new_av = get_availability_cutsets_total(totCut, newMap)
                #print("Availability of the new mapping:",new_av)
                if (new_av > totAv):
                    if (scenario == 2 or scenario == 4):
                        #print("Availability improved, new mapping saved")
                        totMaps[link] = newMap[link]
                        totAv = new_av
                    else:
                        #scenario 1 or 3
                        #Compute number of wavelengths used for the mapping of the new link 
                        numWaveNew = 0
                        numWave = 0
                        for l in newMap[link]:
                            numWaveNew += 1
                        for l in totMaps[link]:
                            numWave += 1
                        #If wavelengths consumption is equal than before, then save the new mapping
                        if (numWaveNew * 2 == numWave * 2):
                            #print("Availability improved, new mapping saved")
                            totMaps[link] = newMap[link]
                            totAv = new_av
                        else:
                            #print("New availability value is an improving one, but wavelengths consumption is larger -> mapping discarded")
                            for l in mapping[0]:
                                P2[l[0]][l[1]]['weight'] += 1
                else:
                    #print("New availability value is not an improving one, mapping discarded")
                    for l in mapping[0]:
                        P2[l[0]][l[1]]['weight'] += 1
            #else:
            #    print("New mapping not survivable")

            trials += 1

    return totAv


#Function that verifies the survivability of a mapping (against single link failures)
#For each cut-set, if not all virtual links belongig to a cut-set share a physical link, then the mapping is survivable
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

#THE PROGRAM STARTS HERE

#First file and last file to run
start_file = 1
end_file = start_file
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
scenario = 1

#To start the clock
time_start = time.time()

#For each data file
for datafile in range(start_file, end_file + 1):
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
    file_name = 'Datfiles/DataFile' + str(datafile) + '.dat'
    #Number of virtual networks (VNs)
    num_vn = read_number_of_VNs(file_name)

    #For each VN
    for vn in range(1, num_vn + 1):

        # L represents the logical network
        L = nx.MultiGraph()

        #read a logical network from file (vn is the number of the logical network that I want to read)
        start_key = CB.number_of_edges()
        read_logical_topology(vn, start_key, file_name)

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
                            for link in altVirLink:

                                #print("Mapping of virtual link:",link)
                                #print("P2.edges:",P2.edges())
                                sp = nx.shortest_path(P2, source=link[0], target=link[1],
                                                      weight='weight')

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

        variable = False
        if variable is False:

            ######################## First Fit wavelength assignement #############################
            mapping.sort()
            #print("Mapping:",mapping)
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
                    #print("Wavelength path:",wavelength_path)
                path_wavelength[repr(path)] = wavelength_path

            ####################### AVAILABILITY COMPUTATION #################################
            #Find all possible combinations of double link failures in the physical network (only for the first VN since the physical network is only one)
            if (vn == 1):
                numFail = find_double_failures(DF)
            #print("Double Failures:",DF)

            used_links = []
            for key in mapping:
                #print("Key:",key)
                for el in key:
                    el_app = ()
                    if (el[0] > el[1]):
                        el_app = tuple((el[1], el[0]))
                        #print(el_app)
                        if (el_app not in used_links):
                            used_links.append(el_app)
                    else:
                        el_app = tuple((el[0], el[1]))
                        if (el_app not in used_links):
                            used_links.append(el_app)

            #print("Used physical links:",used_links)

            #num_Fail=0
            #cont=0
            #for df in DF:
            #    for f in df:
            #        if (f in used_links):
            #            num_Fail+=1
            #print("f:",f)
            #print("Number of failures:",numFail)

            #print("Number of failures:",numFail)
            #print("Mapping final:",mapping)

            maps = {}
            for l in L.edges():
                #print("l:",l)
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
            #print("MAPS:",maps)

            #Create a dictionary with virtual links as keys and with the corresponding mappings as values (links (s,t) with s<t)
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

            #print("MapsOrd:",mapsOrd)

            for key in mapsOrd:
                totMaps[(vn, key[0], key[1])] = mapsOrd[key]
            #print("Total mapping:",totMaps)

            cutsets = get_cutsets(vn, totCut)

            #mapped={}
            #for l in L.edges():
            #    for key in mapping:
            #        for el in key:  
            #            if(el[0]):
            #                mapped[l] = el

            #If at least a cut-set of a VN is down then that VN is disconnected
            av = get_availability_cutsets(cutsets, mapsOrd)

            totAv += av

            ####################### RESULTS ############################

            numWave = 0
            for path in maps:
                for link in maps[path]:
                    numWave += 1
            #print('Wavelength consumption of network',vn,':',numWave*2)

            totW += numWave * 2



        else:
            print('No survivable mapping')

        #print("Mapping of virtual network",vn,"done")
        #print("\n\n------------------------------------------------------------------\n\n")

    #totWB=totW*2

    numWave = 0
    for path in totMaps:
        for link in totMaps[path]:
            numWave += 1
    totW = numWave * 2
    #print("TOTW:",totW)

    backAv = totAv

    backMaps = {}
    backMaps = totMaps.copy()
    print("totMaps:", totMaps)

    ######################## LOCAL SEARCH #####################################
    #print("\n\n########## LOCAL SEARCH #########\n\n")
    for vn in range(1, num_vn + 1):
        for link in totMaps:
            #Consider only virtual links of the VN selected
            if (link[0] == vn):
                #print("Trying with vn and link:", vn, link)
                #Map a single virtual link of a VN in a different way to see if a neighbour solution gets a greater availability value
                totAv = different_mapping(totMaps, link, totCut, totAv, totW, scenario)

    #print("\n\n########## LOCAL SEARCH RESULTS #########\n\n")
    #print("Previous mapping:",backMaps)
    #print("New mapping:",totMaps)
    #print("Previous availability:",backAv)
    #print("Total availability:",totAv)

    #Compute the total wavelength consumption of the new solution
    numWave = 0
    for path in totMaps:
        for link in totMaps[path]:
            numWave += 1
    #Bidirectional links
    totW = numWave * 2

    if (totAv > backAv):
        print("AVAILABILITY IMPROVED FROM THE LOCAL SEARCH")

    #Compute the availability considering inter-VN capacity sharing
    if (scenario == 3 or scenario == 4):
        totAv = get_availability_gateways(totMaps)

    if (scenario == 7):
        shMaps = {}
        #Compute the availability considering inter-VN capacity sharing and spare slice sharing
        totAv = get_availability_gateways_shared_slice(totMaps, shMaps)
        #Added wavelengths (in the shared spare slice) computation
        totW_sh = 0
        for path in shMaps:
            for link in shMaps[path]:
                totW_sh += 1

        #Total wavelength consumption computation
        numWave = 0
        for path in totMaps:
            for link in totMaps[path]:
                numWave += 1
        #Bidirectional links
        totW = numWave * 2

        #Total wave consumption = wavelengths used to map virtual links of the VNs + wavelengths used to map spare slice virtual links
        totW = totW + (totW_sh * 2)

    print("\n############# DATAFILE", datafile, "###############")
    print("Total availability:", totAv)
    print("Total wavelength consumption:", totW)
    print("TotMaps:", totMaps)

    sum_av += totAv
    sum_wave += totW

    if (totAv < min_av):
        min_av = totAv

    if (totAv > max_av):
        max_av = totAv

    if (totW < min_wave):
        min_wave = totW

    if (totW > max_wave):
        max_wave = totW

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

#End time
time_elapsed = (time.time() - time_start)
print("Computational time:", time_elapsed)
