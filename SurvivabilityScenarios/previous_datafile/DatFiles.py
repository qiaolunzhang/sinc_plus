#Python script to create more dat files setting the number of virtual networks, number of virtual nodes and number of virtual links 
#for each file. The physical network must be specified correctly as a variable

import networkx as nx
import random as random

letters= list(map(chr,range(97,123)))

numberofdatfiles = 50
indexvn = 611
numberoflogicalnetworks = 2

for datfileinstance in range(numberofdatfiles):
    keyiterator = 0
    #contatore = 0
    
    L = nx.MultiGraph()
    
    #print('creating data file for virtual network ', datfileinstance+1)
    datafile = 'DataFile' + str(datfileinstance+1) + '.dat'
    data= open(datafile,"w+")
    
    data.write("data;\n")
    data.write("\nparam num_top:="+str(numberoflogicalnetworks)+";")
    data.write("\n\n")
    data.write("#nodes and edges of the physical network\n")
    #data.write("set N := 1 2 3 4 5 6 7 8 9 10;\n")
    
    #7-node German Network
    #data.write("param n := 7;\n")
    #data.write("\n")
    #data.write("set E := (1,2) (1,7) (2,3) (2,6) (2,7) (3,4) (3,6) (4,5) (4,6) (5,6) (6,7) ;\n")
    #data.write("set E := (1,2) (1,7) (2,3) (2,6) (2,7) (3,4) (3,6) (4,5) (4,6) (5,6) (6,7) (1,6) (3,5) ;\n")
    #data.write("\n")
    
    #10-node Italian Network
    #data.write("param n := 10;\n")
    #data.write("\n")
    #data.write("set E := (1,2) (1,3) (1,7) (2,4) (2,7) (3,5) (4,8) (5,6) (5,7) (6,7) (6,9) (7,8) (7,9) (8,10) (9,10) ;\n")
    #data.write("\n")
    
    #52-node Tim Small Network
    #data.write("param n := 52;\n")
    #data.write("\n")
    #data.write("set E := (1,3) (1,4) (1,8) (3,5) (4,5) (4,6) (4,7) (6,7) (2,6) (2,8) (1,9) (9,17) (9,45) (1,28) (1,45) (10,11) (5,11) (11,41) (6,12) (2,12) (12,35) (12,49) (13,40) (13,52) (14,24) (14,28) (15,17) (15,22) (15,43) (15,45) (16,21) (16,51) (16,52) (3,25) (3,38) (4,21) (4,22) (4,50) (17,43) (8,18) (18,40) (18,43) (5,19) (19,41) (6,20) (6,44) (2,23) (23,42) (24,39) (25,39) (25,50) (8,26) (26,52) (27,48) (2,29) (2,31) (2,51) (29,31) (30,32) (30,42) (32,35) (33,34) (8,33) (8,34) (36,42) (37,38) (38,41) (40,43) (44,48) (46,47) (46,48) (47,49) ;\n")
    #data.write("\n")

    #23-node Tokyo Network
    data.write("param n := 23;\n")
    data.write("\n")
    data.write("set E := (1,2) (1,3) (1,4) (1,5) (1,6) (2,3) (2,8) (3,13) (3,9) (4,5) (4,13) (4,14) (4,16) (5,16) (5,18) (6,7) (6,18) (7,8) (7,21) (7,22) (7,23) (8,23) (9,10) (9,11) (9,13) (10,11) (10,12) (10,13) (11,12) (12,13) (12,15) (14,15) (14,20) (15,20) (16,17) (16,19) (16,20) (17,18) (17,19) (18,21) (19,20) (21,22) (22,23) ;\n") 
    data.write("\n")

    numberVNs = 6
    numberVLs = 6
    listofNl = []
    mixed = False
    mixedVNs = []
    mixedVLs = []

    data.write("#nodes and edges of the virtual networks\n")

    if mixed==False:
        for y in range(numberoflogicalnetworks):
            mixedVNs.append(numberVNs)
            mixedVLs.append(numberVLs)
        print(mixedVLs)
    else:
        #Specify the number of nodes and links of each virtual network in case of mixed virtual networks
        mixedVNs=[6,6,6,6,6,6]
        mixedVLs=[6,15,6,15,6,15]

    for logicalnetwork in range(1,numberoflogicalnetworks+1):
        
        listofvirtualnodes = []
        
        y = 0
        x = 0
        #Select the correct node list for virtual networks
        #lista_nodes = [1, 2, 3, 4, 5, 6, 7]
        #lista_nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        lista_nodes = [i for i in range(1,24)]
        
        #data.write("\n") 
        data.write("set Nl["+str(logicalnetwork)+"] := ")
        for y in range(mixedVNs[logicalnetwork-1]):  
            #a = lista_nodes[random.randint(0,mixedVNs[logicalnetwork-1]-y)]
            a = lista_nodes[random.randint(0,len(lista_nodes)-1)]
            lista_nodes.remove(a)
            listofvirtualnodes.append(a)
            data.write(str(a) + " ")
            #print(listofvirtualnodes)
    
        data.write(";\n")
        listofNl.append(listofvirtualnodes)


    for logicalnetwork in range(1,numberoflogicalnetworks+1):
        listofvirtualnodes=listofNl[logicalnetwork-1]
        #print(listofvirtualnodes)
        #data.write("# all the links of the logical topologies (ordered)\n")
        if(logicalnetwork==1):
            data.write("\n")
        else:
            data.write(";\n")
        data.write("set El["+str(logicalnetwork)+"] := ")
        stringofvirtuallinks = "set El:= "
    
        for virtuallink in range(mixedVNs[logicalnetwork-1]-1):
            #L.add_edge(listofvirtualnodes[virtuallink], listofvirtualnodes[virtuallink+1], key=str(letters[keyiterator]))
            #print(listofvirtualnodes[virtuallink], listofvirtualnodes[virtuallink+1], letters[keyiterator])
            #inserting 1
            keyiterator += 1
            if (listofvirtualnodes[virtuallink]<listofvirtualnodes[virtuallink+1]):
                data.write("(" + str(listofvirtualnodes[virtuallink]) + "," + str(listofvirtualnodes[virtuallink+1]) + ") " )
            else:
                data.write("(" + str(listofvirtualnodes[virtuallink+1]) + "," + str(listofvirtualnodes[virtuallink]) + ") " )
            stringofvirtuallinks = stringofvirtuallinks + "(" + str(listofvirtualnodes[virtuallink]) + "," + str(listofvirtualnodes[virtuallink+1]) + ") "
            stringofvirtuallinks = stringofvirtuallinks + "(" + str(listofvirtualnodes[virtuallink+1]) + "," + str(listofvirtualnodes[virtuallink]) + ") "

        if (listofvirtualnodes[mixedVNs[logicalnetwork-1]-1]<listofvirtualnodes[0]):
            data.write("(" + str(listofvirtualnodes[mixedVNs[logicalnetwork-1]-1]) + "," + str(listofvirtualnodes[0]) + ") " )
        else:
            data.write("(" + str(listofvirtualnodes[0]) + "," + str(listofvirtualnodes[mixedVNs[logicalnetwork-1]-1]) + ") " )

        #L.add_edge(listofvirtualnodes[mixedVNs[logicalnetwork-1]-1], listofvirtualnodes[0], key=str(letters[keyiterator]))
        #print(listofvirtualnodes[mixedVNs[logicalnetwork-1]-1], listofvirtualnodes[0], letters[keyiterator])
        #inserting 2
        keyiterator += 1
        stringofvirtuallinks = stringofvirtuallinks + "(" + str(listofvirtualnodes[mixedVNs[logicalnetwork-1]-1]) + "," + str(listofvirtualnodes[0]) + ") "
        stringofvirtuallinks = stringofvirtuallinks + "(" + str(listofvirtualnodes[0]) + "," + str(listofvirtualnodes[mixedVNs[logicalnetwork-1]-1]) + ") "
        if mixedVLs[logicalnetwork-1] > mixedVNs[logicalnetwork-1]:
            #print('here')
            VLscreated = mixedVNs[logicalnetwork-1]
            while VLscreated < mixedVLs[logicalnetwork-1]:
                created = False
                while created == False:
                    loc1 = random.randint(0,mixedVNs[logicalnetwork-1]-1)
                    loc2 = random.randint(0,mixedVNs[logicalnetwork-1]-1)
                    if (loc1 == 0 and loc2 == mixedVNs[logicalnetwork-1]) or (loc2 == 0 and loc1 == mixedVNs[logicalnetwork-1]) or (loc1 == loc2):
                        print('link added before')
                    elif loc1-loc2 >= 2 or loc2-loc1 >=2 or loc1-loc2 >=-2 or loc2-loc1 >=-2:
                        a = listofvirtualnodes[loc1]
                        b = listofvirtualnodes[loc2]
                        print('adding a link:'+str(a)+" "+str(b))
                        stringtoadd = "(" + str(a) + "," + str(b) + ")"
                        if stringtoadd in stringofvirtuallinks:
                            print('link added before 2')    
                        else:    
                            stringofvirtuallinks = stringofvirtuallinks + "(" + str(a) + "," + str(b) + ") "
                            stringofvirtuallinks = stringofvirtuallinks + "(" + str(b) + "," + str(a) + ") "
                            if(a<b):
                                data.write("(" + str(a) + "," + str(b) + ") " )
                            else:
                                data.write("(" + str(b) + "," + str(a) + ") " )
                            #L.add_edge(a, b, key=str(letters[keyiterator]))
                            #inserting 3
                            keyiterator += 1
                            created = True
                            VLscreated += 1    
        
    data.write(";\n")
    data.close() 
    