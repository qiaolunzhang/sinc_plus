import numpy as np
import matplotlib as mpl
# mpl.use('pdf')
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.ticker import MaxNLocator, FuncFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def plot_settings(fig_width=3.487, fig_height=3.487/1.618):
    plt.rc('font', family='serif', serif='Times')
    # Arial
    # plt.rc('font', family='Arial')
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


def get_av_twc_shared_link(topology, num_of_vn_list, num_of_vl, num_instance, scenario_list: list = None,
                           scenario_legend_list: list = None):
    if scenario_list is None:
        scenario_list = ["scenario-1", "scenario-2", "scenario-3", "scenario-4", "scenario-7"]
    if scenario_legend_list is None:
        scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]
    num_scenarios = len(scenario_list)
    av_matrix = [] # np.zeros(num_scenarios, len(num_of_vn_list))
    twc_matrix = [] # np.zeros(num_scenarios, len(num_of_vn_list))
    shared_link_matrix = [] # np.zeros(num_scenarios, len(num_of_vn_list))
    total_capacity_matrix = []
    maximum_usage_matrix = []
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
                    shared_link = line[2]
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


def get_columns_max_list(topology, num_of_vn_list, num_of_vl, num_instance, scenario_list: list = None,
                         scenario_legend_list: list = None, column_index_list: list = None):
    if scenario_list is None:
        scenario_list = ["scenario-1", "scenario-2", "scenario-3", "scenario-4", "scenario-7"]
    if scenario_legend_list is None:
        scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]
    num_scenarios = len(scenario_list)
    one_column_max_list = []
    for column_index in column_index_list:
        # one_column_matrix = []
        one_column_max = - np.Inf
        for i in range(num_scenarios):
            cur_column_vector_all_instances_matrix = []
            for j in range(1, num_instance+1):
                cur_column_vector = []
                for num_of_vn in num_of_vn_list:
                    file_name = "../results/" + topology + "/" + str(num_of_vn) + "vn/" + str(num_of_vl) + "vl/" + scenario_list[i] + "_instance_" + str(j) + ".txt"
                    with open(file_name, "r") as file:
                        lines = file.readlines()
                        line = lines[0]
                        line = line.strip()
                        line = line.split(" ")
                        line = [float(x) for x in line]
                        cur_column = line[column_index]
                        cur_column_vector.append(cur_column)
                cur_column_vector_all_instances_matrix.append(cur_column_vector)
            # calculate the average of all instances

            cur_column_vector_all_instances_matrix = np.array(cur_column_vector_all_instances_matrix)
            cur_column_max = np.max(cur_column_vector_all_instances_matrix)
            if cur_column_max > one_column_max:
                one_column_max = cur_column_max
        one_column_max_list.append(one_column_max)
    return one_column_max_list


def get_matrix_columns(topology, num_of_vn_list, num_of_vl, num_instance, scenario_list: list = None,
                       scenario_legend_list: list = None, column_index_list: list = None):
    if scenario_list is None:
        scenario_list = ["scenario-1", "scenario-2", "scenario-3", "scenario-4", "scenario-7"]
    if scenario_legend_list is None:
        scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]
    num_scenarios = len(scenario_list)
    one_column_matrix_list = []
    for column_index in column_index_list:
        one_column_matrix = []
        for i in range(num_scenarios):
            cur_column_vector_all_instances_matrix = []
            for j in range(1, num_instance+1):
                cur_column_vector = []
                for num_of_vn in num_of_vn_list:
                    file_name = "../results/" + topology + "/" + str(num_of_vn) + "vn/" + str(num_of_vl) + "vl/" + scenario_list[i] + "_instance_" + str(j) + ".txt"
                    with open(file_name, "r") as file:
                        lines = file.readlines()
                        line = lines[0]
                        line = line.strip()
                        line = line.split(" ")
                        line = [float(x) for x in line]
                        cur_column = line[column_index]
                        cur_column_vector.append(cur_column)
                cur_column_vector_all_instances_matrix.append(cur_column_vector)
            # calculate the average of all instances

            cur_column_vector_all_instances_matrix = np.array(cur_column_vector_all_instances_matrix)
            cur_column_vector = np.mean(cur_column_vector_all_instances_matrix, axis=0)
            one_column_matrix.append(cur_column_vector)
        one_column_matrix = np.array(one_column_matrix)
        one_column_matrix_list.append(one_column_matrix)
    return one_column_matrix_list

def custom_formatter(x, pos):
    if x == 100.0:
        return f"{int(x):d}"  # Remove the decimal for 100.0
    else:
        return f"{x:.1f}"    # Otherwise, keep one decimal place


def plot_av_twc_computation_time_sp(topology, av_matrix, twc_matrix, shared_link_matrix, double_axis_flag=False):
    fig_width = 3.487
    fig_height = fig_width / 1.618
    plot_settings(fig_width, fig_height)
    # round av to 1 decimal place
    av_matrix = np.round(av_matrix, 1)

    # number of columns in each scenario
    N = len(av_matrix[0])
    # number of scenarios
    # ind = np.arange(4)
    ind = np.arange(N)
    width = 1 / (N+1)

    fig, (ax) = plt.subplots(1, 3)

    x_tick_label_list = ['5', '10', '15', '20', '25']

    patterns = ('//////', '\\\\\\', '---', 'xxx', 'ooo', '\\', '\\\\', '++', '*', 'O', '.')

    plt.rcParams['hatch.linewidth'] = 0.25  # previous pdf hatch linewidth
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    color_list = [color_cycle[0], color_cycle[1], color_cycle[2]]

    plt.rcParams['hatch.linewidth'] = 0.25  # previous pdf hatch linewidth
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    color_list = [color_cycle[0], color_cycle[1], color_cycle[2], color_cycle[3], color_cycle[4]]

    label_position = ind + width * (+0.5)  # + width * (1.5 - 1)
    scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]
    scenario_legend_list = ["SP", "SVNM", "SINC", "SINC+"]

    # ************************************ First subgraph ***************************************************
    # j is for ZR and long-haul transponders
    if double_axis_flag:
        ax0_twin = ax[0].twinx()
    for i in range(len(av_matrix)):
        if double_axis_flag:
            if i < 2:
                ax[0].bar(ind + width * (i - 1), av_matrix[i], width,
                          alpha=0.7, label=scenario_legend_list[i], color=color_list[i], hatch=patterns[i])
            else:
                ax0_twin.bar(ind + width * (i - 1), av_matrix[i], width,
                             alpha=0.7, label=scenario_legend_list[i], color=color_list[i], hatch=patterns[i])
        else:
            ax[0].bar(ind + width * (i - 1), av_matrix[i], width,
                      alpha=0.7, label=scenario_legend_list[i], color=color_list[i], hatch=patterns[i])

    ax[0].set_xticks(label_position)
    ax[0].set_xticklabels(x_tick_label_list)

    if double_axis_flag:
        ax[0].set_ylim(50, 100)
    else:
        ax[0].set_ylim(80, 100)
    if double_axis_flag:
        ax[0].set_ylim(75, 100)
        ax0_twin.set_ylim(98, 100)
        # Set the y-axis format to one decimal place for each subplot
        formatter = FuncFormatter(custom_formatter)
        # formatter = FormatStrFormatter('%.1f')
        ax0_twin.yaxis.set_major_formatter(formatter)

    ax[0].set_xlabel('Number of VNs\n (a) Availability')
    if double_axis_flag:
        ax[0].set_ylabel('AV of SP and SVNM (%)')
        ax0_twin.set_ylabel('AV of SINC (%)')
    else:
        ax[0].set_ylabel('Availability')
    ax[0].grid(lw=0.25, clip_on=False)


    if not double_axis_flag:
        # Creating inset axes for zoom-in detail on specific columns of ILP-Ring and H-Ring
        axins = inset_axes(ax[0], width="100%", height="100%",
                           # loc='upper left',
                           # loc=1,
                           loc='upper left',
                           bbox_to_anchor=(0.445, 1 - 0.35, .075, .3), bbox_transform=ax[0].transAxes,
                           # bbox_to_anchor=(0.05, 0.5, 1, 1),
                           # bbox_to_anchor=[50, 80],
                           borderpad=1)
        inset_indices = [0, 1]  # Indices for ILP-Ring and H-Ring
        # inset_indices = [0]
        # selected_data = [[av_matrix[2, 2], av_matrix[2, 3]], [av_matrix[3, 2], av_matrix[3, 3]]]
        selected_data = [[av_matrix[2, 2]], [av_matrix[3, 2]]]
        inset_data = np.array(selected_data)
        # inset_data = av_matrix[:, [2, 3]]  # Select the last two columns data for ILP-Ring and H-Ring
        inset_ticks = np.array([0])  # Position for the two bars
        inset_color_list = [color_list[2], color_cycle[3]]

        for i, index in enumerate(inset_indices):
            axins.bar(inset_ticks + width * i, inset_data[index], width, alpha=0.7, color=inset_color_list[index],
                      hatch=patterns[index])
        axins.set_xticks(inset_ticks + width * 0.5)
        axins.set_xticklabels(['15'])  # Labels specifically for the zoomed columns
        axins.set_ylim(99.8, 100)

    # if double_axis_flag:
    #     # Get handles and labels for both axes
    #     handles1, labels1 = ax[0].get_legend_handles_labels()
    #     handles2, labels2 = ax0_twin.get_legend_handles_labels()
    #
    #     # Combine the handles and labels
    #     handles = handles1 + handles2
    #     labels = labels1 + labels2
    #
    #     ax[0].legend(handles, labels, loc='upper right',  bbox_to_anchor=(2.8, 1.245),
    #                  ncol=5, prop={'size': 7}, columnspacing=0.5)
    # else:
    #     ax[0].legend(loc='upper right',  bbox_to_anchor=(3.1, 1.245),
    #                  ncol=5, prop={'size': 7}, columnspacing=0.5)
    #
    # ************************************ Second subgraph ***************************************************
    # plot the twc
    for i in range(len(twc_matrix)):
        ax[1].bar(ind + width * (i - 1), twc_matrix[i], width,
                  alpha=0.7, label=scenario_legend_list[i], color=color_list[i], hatch=patterns[i])
    ax[1].set_xticks(label_position)
    ax[1].set_xticklabels(x_tick_label_list)
    # ax[1].set_ylim(50, 180)


    ax[1].set_xlabel('Number of VNs\n (b) Wavelength consumption')
    ax[1].set_ylabel('TWC')
    ax[1].grid(lw=0.25, clip_on=False)


    # ************************************ Third subgraph ***************************************************
    label_position = ind + width * (+1.5)  # + width * (1.5 - 1)

    # plot the computation time
    for i in range(len(shared_link_matrix)):
        ax[2].bar(ind + width * (i - 1), shared_link_matrix[i], width,
                  alpha=0.7, label=scenario_legend_list[i], color=color_list[i], hatch=patterns[i])
    ax[2].set_xticks(label_position)
    ax[2].set_xticklabels(x_tick_label_list)
    # ax[2].set_ylim(0, 5000)
    # set y axis to log scale
    # ax[2].set_yscale('log')

    ax[2].legend(loc='upper left', ncol=1, prop={'size': 7}, columnspacing=0.5)

    ax[2].set_xlabel('Number of VNs\n (c) VLs enabled with sharing')
    ax[2].set_ylabel('Number of VLs enabled\n with sharing')
    ax[2].grid(lw=0.25, clip_on=False)


    fig.set_size_inches(fig_width * 2, fig_height * 3 / 4)

    # adjust the space between the first subplot and the second subplot
    fig.subplots_adjust(left=.07, bottom=.26, right=.98, top=.91,
                        wspace=0.3)
    if double_axis_flag:
        mpl.pyplot.subplots_adjust(wspace=0.5)
        # Get the positions of the original subplots
        pos0 = ax[0].get_position()
        pos1 = ax[1].get_position()
        pos2 = ax[2].get_position()

        # Adjust the position of the second subplot (increase space between first and second)
        new_pos1 = [pos1.x0 + 0.035, pos1.y0, pos1.width, pos1.height]  # Increase x0 to move it right
        ax[1].set_position(new_pos1)
    else:
        mpl.pyplot.subplots_adjust(wspace=0.3)

    if double_axis_flag:
        ############################## Add first purple dashed arrow ########################################
        # 椭圆中心和大小
        ellipse_center_x = 0.9
        ellipse_center_y = 85
        ellipse_width = 0.38
        ellipse_height = 2

        # 在柱状图上添加紫色虚线椭圆
        ellipse = patches.Ellipse((ellipse_center_x, ellipse_center_y), width=ellipse_width, height=ellipse_height,
                                  edgecolor='purple', facecolor='none', linestyle='dashed')
        ax[0].add_patch(ellipse)

        # 计算箭头的起始点和结束点
        arrow_start_x = ellipse_center_x - ellipse_width / 2 + 0.05 # 椭圆左侧边缘
        arrow_start_y = ellipse_center_y
        arrow_end_x = 0.32  # 指向y轴的方向
        arrow_end_y = ellipse_center_y
        # 添加紫色虚线箭头
        # -|>
        arrow_style = patches.FancyArrowPatch((arrow_start_x, arrow_start_y), (arrow_end_x, arrow_end_y),
                                              connectionstyle="arc3", color='purple',
                                              arrowstyle='->', lw=1, mutation_scale=5)
                                              # path_effects=[withStroke(linewidth=2, foreground='purple', linestyle='dashed')])

        ax[0].add_patch(arrow_style)

        ############################## Add second purple dashed arrow ########################################
        # 椭圆中心和大小
        ellipse_center_x = 1.25
        ellipse_center_y = 90
        ellipse_width = 0.38
        ellipse_height = 2

        # 在柱状图上添加紫色虚线椭圆
        ellipse = patches.Ellipse((ellipse_center_x, ellipse_center_y), width=ellipse_width, height=ellipse_height,
                                  edgecolor='purple', facecolor='none', linestyle='dashed')
        ax[0].add_patch(ellipse)

        # 计算箭头的起始点和结束点
        arrow_start_x = ellipse_center_x + ellipse_width / 2 - 0.05  # 椭圆左侧边缘
        arrow_start_y = ellipse_center_y
        arrow_end_x = ellipse_center_x + ellipse_width / 2 + 0.42  # 指向y轴的方向
        arrow_end_y = ellipse_center_y
        # 添加紫色虚线箭头
        # -|>
        arrow_style = patches.FancyArrowPatch((arrow_start_x, arrow_start_y), (arrow_end_x, arrow_end_y),
                                              connectionstyle="arc3", color='purple',
                                              arrowstyle='->', lw=1, mutation_scale=5)
        # path_effects=[withStroke(linewidth=2, foreground='purple', linestyle='dashed')])

        ax[0].add_patch(arrow_style)
    else:
        ############################## Add first purple dashed arrow ########################################
        # 椭圆中心和大小
        ellipse_center_x = 2.3
        ellipse_center_y = 100
        ellipse_width = 0.5
        ellipse_height = 2

        # 在柱状图上添加紫色虚线椭圆
        ellipse = patches.Ellipse((ellipse_center_x, ellipse_center_y), width=ellipse_width, height=ellipse_height,
                                  edgecolor='purple', facecolor='none', linestyle='dashed')
        ax[0].add_patch(ellipse)
        # Set clip_on to False so the ellipse is drawn even outside the axes
        ellipse.set_clip_on(False)

        # 计算箭头的起始点和结束点
        arrow_start_x = ellipse_center_x# - ellipse_width / 2 + 0.05 # 椭圆左侧边缘
        arrow_start_y = ellipse_center_y - ellipse_height / 2
        arrow_end_x = ellipse_center_x + 0.25# - 0.42 #0.42  # 指向y轴的方向
        arrow_end_y = ellipse_center_y - 2     * ellipse_height
        # 添加紫色虚线箭头
        # -|>
        arrow_style = patches.FancyArrowPatch((arrow_start_x, arrow_start_y), (arrow_end_x, arrow_end_y),
                                              connectionstyle="arc3", color='purple',
                                              arrowstyle='->', lw=1, mutation_scale=5)
                                              # path_effects=[withStroke(linewidth=2, foreground='purple', linestyle='dashed')])

        ax[0].add_patch(arrow_style)


    if double_axis_flag:
        fig.savefig('figures/' + topology + '/fig2_number_of_vn_double_axis_sp.pdf')
    else:
        fig.savefig('figures/' + topology + '/fig2_number_of_vn_one_axis_sp.pdf')


if __name__ == '__main__':
    # cur_topology = "tokyo-5nodesVN"
    cur_topology = "tokyo-5nodesVN-Capacity"
    # num_of_vn_list = [6, 12, 18, 24, 30]
    cur_num_of_vn_list = [5, 10, 15, 20, 25]
    cur_num_of_vl = 6
    cur_num_instance = 10

    scenario_list = ["scenario-1", "scenario-2", "scenario-3", "scenario-4", "scenario-7"]
    scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]
    av_matrix_survivable, twc_matrix_survivable, shared_link_matrix_survivable \
        = get_av_twc_shared_link(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list,
                                 num_of_vl=cur_num_of_vl, num_instance=cur_num_instance, scenario_list=scenario_list,
                                 scenario_legend_list=scenario_legend_list)

    one_column_matrix_list = get_matrix_columns(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list,
                                                num_of_vl=cur_num_of_vl, num_instance=cur_num_instance,
                                                scenario_list=scenario_list, scenario_legend_list=scenario_legend_list,
                                                column_index_list=[0,1])
    one_column_matrix_0 = one_column_matrix_list[0]
    one_column_matrix_1 = one_column_matrix_list[1]

    # total link resource consumption: 5, 6, 7
    total_link_resource_consumption_list = get_matrix_columns(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list,
                                                              num_of_vl=cur_num_of_vl, num_instance=cur_num_instance,
                                                              scenario_list=scenario_list, scenario_legend_list=scenario_legend_list,
                                                              column_index_list=[5, 6, 7])
    twc_matrix_survivable = total_link_resource_consumption_list[2]

    cur_topology = "tokyo-5nodesVN-SP"
    scenario_list = ["scenario-0"]
    scenario_legend_list = ["SP"]
    av_matrix_SP, twc_matrix_SP, shared_link_matrix_SP \
        = get_av_twc_shared_link(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list,
                                 num_of_vl=cur_num_of_vl, num_instance=cur_num_instance, scenario_list=scenario_list,
                                 scenario_legend_list=scenario_legend_list)
    # todo: reset the twc of shortest path before combining the matrix

    av_matrix_combine = np.vstack((av_matrix_SP, av_matrix_survivable))
    twc_matrix_combine = np.vstack((twc_matrix_SP, twc_matrix_survivable))
    shared_link_matrix_combine = np.vstack((shared_link_matrix_SP, shared_link_matrix_survivable))

    row_index = [0, 1, 3, 5]
    scenario_list = ["scenario-1", "scenario-2", "scenario-3", "scenario-4", "scenario-7"]
    scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]
    av_matrix_combine = av_matrix_combine[row_index, :]
    twc_matrix_combine = twc_matrix_combine[row_index, :]
    shared_link_matrix_combine = shared_link_matrix_combine[row_index, :]
    # divide the shared link by the number of double link failure scenarios
    shared_link_matrix_combine /= 903
    # plot the figure with SP
    plot_av_twc_computation_time_sp(topology="tokyo", av_matrix=av_matrix_combine,
                                    twc_matrix=twc_matrix_combine, shared_link_matrix=shared_link_matrix_combine,
                                    double_axis_flag=True)
    plot_av_twc_computation_time_sp(topology="tokyo", av_matrix=av_matrix_combine,
                                    twc_matrix=twc_matrix_combine, shared_link_matrix=shared_link_matrix_combine,
                                    double_axis_flag=False)

    cur_topology = "tokyo-5nodesVN-Capacity"

    # the maximum usage: 8, 9, 10
    maximum_usage_list = get_columns_max_list(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list,
                                              num_of_vl=cur_num_of_vl, num_instance=cur_num_instance,
                                              scenario_list=scenario_list, scenario_legend_list=scenario_legend_list,
                                              column_index_list=[8, 9, 10])

    print("test")


