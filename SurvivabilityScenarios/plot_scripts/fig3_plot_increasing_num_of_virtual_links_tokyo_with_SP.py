import numpy as np
import matplotlib as mpl
# mpl.use('pdf')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def plot_settings(fig_width=3.487, fig_height=3.487/1.618):
    # plt.rc('font', family='serif', serif='Times')
    # Arial
    plt.rc('font', family='Arial')
    # plt.rc('text', usetex=True)
    plt.rc('xtick', labelsize=7)
    plt.rc('ytick', labelsize=8)
    plt.rc('axes', labelsize=8)
    # axes.linewidth : 0.5
    plt.rc('axes', linewidth=0.5)
    # ytick.major.width : 0.5
    plt.rc('ytick.major', width=0.5)
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rc('ytick.minor', visible=True)

    # set grid under the plot
    # https://stackoverflow.com/questions/23357798/how-to-draw-grid-lines-behind-matplotlib-bar-graph
    # https://stackoverflow.com/questions/1726391/matplotlib-draw-grid-lines-behind-other-graph-elements/39039520#39039520
    plt.rc('axes', axisbelow=True)

    # plt.style.use(r"..\..\styles\infocom.mplstyle") # Insert your save location here


def get_av_twc_shared_link(topology, num_of_vn_list, num_of_vl, num_instance):
    num_scenarios = 5
    scenario_list = ["scenario-1", "scenario-2", "scenario-3", "scenario-4", "scenario-7"]
    scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]
    av_matrix = [] # np.zeros(num_scenarios, len(num_of_vn_list))
    twc_matrix = [] # np.zeros(num_scenarios, len(num_of_vn_list))
    shared_link_matrix = [] # np.zeros(num_scenarios, len(num_of_vn_list))
    for i in range(num_scenarios):
        av_vector_all_instances_matrix = []
        twc_vector_all_instances_matrix = []
        shared_link_vector_all_instances_matrix = []
        for j in range(1, num_instance+1):
            cur_av_vector = []
            cur_twc_vector = []
            cur_shared_link_vector = []
            for num_of_vn in num_of_vn_list:
                file_name = "../results/" + topology + "/" + str(num_of_vn) + "vn/" + str(num_of_vl) + "vl/" + scenario_list[i] + "_instance_" + str(j) + ".txt"
                with open(file_name, "r") as file:
                    lines = file.readlines()
                    line = lines[0]
                    line = line.strip()
                    line = line.split(" ")
                    line = [float(x) for x in line]
                    av = line[0]
                    twc = line[1]
                    shared_link = line[3]
                    cur_av_vector.append(av)
                    cur_twc_vector.append(twc)
                    cur_shared_link_vector.append(shared_link)
            av_vector_all_instances_matrix.append(cur_av_vector)
            twc_vector_all_instances_matrix.append(cur_twc_vector)
            shared_link_vector_all_instances_matrix.append(cur_shared_link_vector)
        # calculate the average of all instances
        av_vector_all_instances_matrix = np.array(av_vector_all_instances_matrix)
        twc_vector_all_instances_matrix = np.array(twc_vector_all_instances_matrix)
        shared_link_vector_all_instances_matrix = np.array(shared_link_vector_all_instances_matrix)
        av_vector = np.mean(av_vector_all_instances_matrix, axis=0)
        twc_vector = np.mean(twc_vector_all_instances_matrix, axis=0)
        shared_link_vector = np.mean(shared_link_vector_all_instances_matrix, axis=0)
        av_matrix.append(av_vector)
        twc_matrix.append(twc_vector)
        shared_link_matrix.append(shared_link_vector)
    av_matrix = np.array(av_matrix)
    twc_matrix = np.array(twc_matrix)
    shared_link_matrix = np.array(shared_link_matrix)
    return av_matrix, twc_matrix, shared_link_matrix


if __name__ == '__main__':
    cur_topology = "tokyo-5nodesVN"
    # num_of_vn_list = [6, 12, 18, 24, 30]
    cur_num_of_vn_list = [5, 10, 15, 20, 25]
    cur_num_of_vl = 5
    cur_num_instance = 10
    av_matrix, twc_matrix, shared_link_matrix \
        = get_av_twc_shared_link(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list, num_of_vl=cur_num_of_vl,
                                 num_instance=cur_num_instance)

