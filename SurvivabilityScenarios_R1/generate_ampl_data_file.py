import networkx as nx
import random
import os


class NetworkEnvironment:
    def __init__(self, num_physical_nodes, num_virtual_network, num_virtual_nodes, num_virtual_links):
        self.num_physical_nodes = num_physical_nodes
        self.physical_nodes_list = list(range(1, num_physical_nodes + 1))
        self.num_virtual_network = num_virtual_network
        self.num_virtual_nodes = num_virtual_nodes
        self.num_virtual_links = num_virtual_links

        self.virtual_nodes_list_dict = {}
        self.virtual_links_list_dict = {}
        self.virtual_links_to_add_list_dict = {}

        self.initialize_virtual_networks()

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
    num_virtual_network_list = [6, 12, 18, 24, 30]
    num_virtual_nodes = 6
    num_virtual_link_min = num_virtual_nodes
    num_virtual_link_max = int(num_virtual_nodes * (num_virtual_nodes - 1) / 2)
    for num_virtual_network in num_virtual_network_list:
        for i in range(1, 11):
            network_environment = NetworkEnvironment(num_physical_nodes=num_physical_nodes,
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
