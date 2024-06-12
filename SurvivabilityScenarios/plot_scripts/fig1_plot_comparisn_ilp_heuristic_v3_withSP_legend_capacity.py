import numpy as np
import matplotlib as mpl
# mpl.use('pdf')
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.patheffects import withStroke
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
from matplotlib.ticker import FuncFormatter
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


def get_av_twc_shared_link_time(topology, num_of_vn_list, num_of_vl, num_instance,
                                scenario_list: list=None, scenario_legend_list: list=None):
    num_scenarios = len(scenario_list)
    if scenario_list is None:
        scenario_list = ["scenario-1", "scenario-2", "scenario-3", "scenario-4", "scenario-7"]
    if scenario_legend_list is None:
        scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]
    av_matrix = [] # np.zeros(num_scenarios, len(num_of_vn_list))
    twc_matrix = [] # np.zeros(num_scenarios, len(num_of_vn_list))
    shared_link_matrix = [] # np.zeros(num_scenarios, len(num_of_vn_list))
    computation_time_matrix = []
    for i in range(num_scenarios):
        av_vector_all_instances_matrix = []
        twc_vector_all_instances_matrix = []
        shared_link_vector_all_instances_matrix = []
        computation_time_all_instances_matrix = []
        for j in range(1, num_instance+1):
            cur_av_vector = []
            cur_twc_vector = []
            cur_shared_link_vector = []
            cur_computation_time_vector = []
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
                    computation_time = line[4]
                    cur_av_vector.append(av)
                    cur_twc_vector.append(twc)
                    cur_shared_link_vector.append(shared_link)
                    cur_computation_time_vector.append(computation_time)

            av_vector_all_instances_matrix.append(cur_av_vector)
            twc_vector_all_instances_matrix.append(cur_twc_vector)
            shared_link_vector_all_instances_matrix.append(cur_shared_link_vector)
            computation_time_all_instances_matrix.append(cur_computation_time_vector)
        # calculate the average of all instances
        av_vector_all_instances_matrix = np.array(av_vector_all_instances_matrix)
        twc_vector_all_instances_matrix = np.array(twc_vector_all_instances_matrix)
        shared_link_vector_all_instances_matrix = np.array(shared_link_vector_all_instances_matrix)
        computation_time_all_instances_matrix = np.array(computation_time_all_instances_matrix)
        av_vector = np.mean(av_vector_all_instances_matrix, axis=0)
        twc_vector = np.mean(twc_vector_all_instances_matrix, axis=0)
        shared_link_vector = np.mean(shared_link_vector_all_instances_matrix, axis=0)
        computation_time_vector = np.mean(computation_time_all_instances_matrix, axis=0)
        av_matrix.append(av_vector)
        twc_matrix.append(twc_vector)
        shared_link_matrix.append(shared_link_vector)
        computation_time_matrix.append(computation_time_vector)

    av_matrix = np.array(av_matrix)
    twc_matrix = np.array(twc_matrix)
    shared_link_matrix = np.array(shared_link_matrix)
    computation_time_matrix = np.array(computation_time_matrix)
    return av_matrix, twc_matrix, shared_link_matrix, computation_time_matrix


def custom_formatter(x, pos):
    if x == 100.0:
        return f"{int(x):d}"  # Remove the decimal for 100.0
    else:
        return f"{x:.1f}"    # Otherwise, keep one decimal place


def plot_av_twc_computation_time_no_sp(topology, av_matrix, twc_matrix, computation_time_matrix, double_axis_flag=False):
    fig_width = 3.487
    fig_height = fig_width / 1.618
    plot_settings(fig_width, fig_height)
    # round av to 1 decimal place
    av_matrix = np.round(av_matrix, 1)

    # number of columns in each scenario
    N = 5
    # number of scenarios
    ind = np.arange(4)
    width = 1 / (N+1)

    fig, (ax) = plt.subplots(1, 3)

    x_tick_label_list = ['ILP-Ring', 'H-Ring', 'ILP-Mesh', 'H-Mesh']
    label_list = ['TP-Z', 'TP-L', 'IP-Z', 'IP-L', 'OP-Z', 'OP-L']

    patterns = ('//////', '\\\\\\', '---', 'xxx', 'ooo', '\\', '\\\\', '++', '*', 'O', '.')

    plt.rcParams['hatch.linewidth'] = 0.25  # previous pdf hatch linewidth
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    color_list = [color_cycle[0], color_cycle[1], color_cycle[2]]

    plt.rcParams['hatch.linewidth'] = 0.25  # previous pdf hatch linewidth
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    color_list = [color_cycle[0], color_cycle[1], color_cycle[2], color_cycle[3], color_cycle[4]]

    label_position = ind + width * (+1)  # + width * (1.5 - 1)
    scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]

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

    ax[0].set_ylim(50, 100)
    if double_axis_flag:
        ax0_twin.set_ylim(99, 100)
        # Set the y-axis format to one decimal place for each subplot
        formatter = FuncFormatter(custom_formatter)
        # formatter = FormatStrFormatter('%.1f')
        ax0_twin.yaxis.set_major_formatter(formatter)

    ax[0].set_xlabel('Scenarios \n (a) Availability')
    if double_axis_flag:
        ax[0].set_ylabel('AV of SVNM (%)')
        ax0_twin.set_ylabel('AV of SINC (%)')
    else:
        ax[0].set_ylabel('Availability')
    ax[0].grid(lw=0.25, clip_on=False)

    if double_axis_flag:
        # Get handles and labels for both axes
        handles1, labels1 = ax[0].get_legend_handles_labels()
        handles2, labels2 = ax0_twin.get_legend_handles_labels()

        # Combine the handles and labels
        handles = handles1 + handles2
        labels = labels1 + labels2

        ax[0].legend(handles, labels, loc='upper right',  bbox_to_anchor=(3.0, 1.245),
                     ncol=5, prop={'size': 7}, columnspacing=0.5)
    else:
        ax[0].legend(loc='upper right',  bbox_to_anchor=(3.1, 1.245),
                     ncol=5, prop={'size': 7}, columnspacing=0.5)

    # ************************************ Second subgraph ***************************************************
    # plot the twc
    for i in range(len(twc_matrix)):
        ax[1].bar(ind + width * (i - 1), twc_matrix[i], width,
                  alpha=0.7, label=scenario_legend_list[i], color=color_list[i], hatch=patterns[i])
    ax[1].set_xticks(label_position)
    ax[1].set_xticklabels(x_tick_label_list)
    ax[1].set_ylim(50, 180)

    ax[1].set_xlabel('Scenarios \n (b) Wavelength consumption')
    ax[1].set_ylabel('TWC')
    ax[1].grid(lw=0.25, clip_on=False)

    # ************************************ Third subgraph ***************************************************
    # plot the computation time
    for i in range(len(computation_time_matrix)):
        ax[2].bar(ind + width * (i - 1), computation_time_matrix[i], width,
                  alpha=0.7, label=scenario_legend_list[i], color=color_list[i], hatch=patterns[i])
    ax[2].set_xticks(label_position)
    ax[2].set_xticklabels(x_tick_label_list)
    # ax[2].set_ylim(0, 5000)
    # set y axis to log scale
    ax[2].set_yscale('log')

    ax[2].set_xlabel('Scenarios \n (c) Computation time')
    ax[2].set_ylabel('Computation time (s)')
    ax[2].grid(lw=0.25, clip_on=False)


    fig.set_size_inches(fig_width * 2, fig_height * 4 / 5)

    # adjust the space between the first subplot and the second subplot
    fig.subplots_adjust(left=.07, bottom=.26, right=.98, top=.87,
                        wspace=0.3)
    if double_axis_flag:
        mpl.pyplot.subplots_adjust(wspace=0.45)
        # Get the positions of the original subplots
        pos0 = ax[0].get_position()
        pos1 = ax[1].get_position()
        pos2 = ax[2].get_position()

        # Adjust the position of the second subplot (increase space between first and second)
        new_pos1 = [pos1.x0 + 0.025, pos1.y0, pos1.width, pos1.height]  # Increase x0 to move it right
        ax[1].set_position(new_pos1)
    else:
        mpl.pyplot.subplots_adjust(wspace=0.3)
    if double_axis_flag:
        fig.savefig('figures/' + topology + '/compare_ILP_heuristic_double_axis.pdf')
    else:
        fig.savefig('figures/' + topology + '/compare_ILP_heuristic_one_axis.pdf')


def plot_av_twc_computation_time_sp(topology, av_matrix, twc_matrix, computation_time_matrix, double_axis_flag=False):
    fig_width = 3.487
    fig_height = fig_width / 1.618
    plot_settings(fig_width, fig_height)
    # round av to 1 decimal place
    av_matrix = np.round(av_matrix, 1)

    # number of columns in matrix (number of scenario)
    N = len(av_matrix[0])
    # number of scenarios
    ind = np.arange(4)
    width = 1 / (N+1)

    fig, (ax) = plt.subplots(1, 3)

    x_tick_label_list = ['ILP-Ring', 'H-Ring', 'ILP-Mesh', 'H-Mesh']

    patterns = ('//////', '\\\\\\', '---', 'xxx', 'ooo', '\\', '\\\\', '++', '*', 'O', '.')

    plt.rcParams['hatch.linewidth'] = 0.25  # previous pdf hatch linewidth
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    color_list = [color_cycle[0], color_cycle[1], color_cycle[2]]

    plt.rcParams['hatch.linewidth'] = 0.25  # previous pdf hatch linewidth
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    color_list = [color_cycle[0], color_cycle[1], color_cycle[2], color_cycle[3], color_cycle[4]]

    label_position = ind + width * (+1)  # + width * (1.5 - 1)
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

    ax[0].set_ylim(75, 100)
    if double_axis_flag:
        ax0_twin.set_ylim(99, 100)
        # Set the y-axis format to one decimal place for each subplot
        formatter = FuncFormatter(custom_formatter)
        # formatter = FormatStrFormatter('%.1f')
        ax0_twin.yaxis.set_major_formatter(formatter)

    if not double_axis_flag:
        # Creating inset axes for zoom-in detail on specific columns of ILP-Ring and H-Ring
        axins = inset_axes(ax[0], width="100%", height="100%",
                           # loc='upper left',
                           # loc=1,
                           loc='upper left',
                           bbox_to_anchor=(0.07, 1 - 0.35, .3, .3), bbox_transform=ax[0].transAxes,
                           # bbox_to_anchor=(0.05, 0.5, 1, 1),
                           # bbox_to_anchor=[50, 80],
                           borderpad=1)
        inset_indices = [0, 1]  # Indices for ILP-Ring and H-Ring
        selected_data = [[av_matrix[2, 0], av_matrix[2, 1]], [av_matrix[3, 0], av_matrix[3, 1]]]
        inset_data = np.array(selected_data)
        # inset_data = av_matrix[:, [2, 3]]  # Select the last two columns data for ILP-Ring and H-Ring
        inset_ticks = np.array([0, 1])  # Position for the two bars
        inset_color_list = [color_list[2], color_cycle[3]]

        for i, index in enumerate(inset_indices):
            axins.bar(inset_ticks + width * i, inset_data[index], width, alpha=0.7, color=inset_color_list[index],
                      hatch=patterns[index])
        axins.set_xticks(inset_ticks + width * 0.5)
        axins.set_xticklabels(['ILP-Ring', 'H-Ring'])  # Labels specifically for the zoomed columns
        axins.set_ylim(99, 100)
    ax[0].set_xlabel('Scenarios \n (a) Availability')
    if double_axis_flag:
        ax[0].set_ylabel('AV of SP and SVNM (%)')
        ax0_twin.set_ylabel('AV of SINC (%)')
    else:
        ax[0].set_ylabel('Availability')
    ax[0].grid(lw=0.25, clip_on=False)

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

    # ************************************ Second subgraph ***************************************************
    # plot the twc
    for i in range(len(twc_matrix)):
        ax[1].bar(ind + width * (i - 1), twc_matrix[i], width,
                  alpha=0.7, label=scenario_legend_list[i], color=color_list[i], hatch=patterns[i])
    ax[1].set_xticks(label_position)
    ax[1].set_xticklabels(x_tick_label_list)
    ax[1].set_ylim(50, 180)

    ax[1].set_xlabel('Scenarios \n (b) Total link resource consumption')
    ax[1].set_ylabel('TLRC')
    ax[1].grid(lw=0.25, clip_on=False)

    # legend in top left
    ax[1].legend(loc='upper left', ncol=1, prop={'size': 7}, columnspacing=0.5)

    # ************************************ Third subgraph ***************************************************
    # plot the computation time
    for i in range(len(computation_time_matrix)):
        ax[2].bar(ind + width * (i - 1), computation_time_matrix[i], width,
                  alpha=0.7, label=scenario_legend_list[i], color=color_list[i], hatch=patterns[i])
    ax[2].set_xticks(label_position)
    ax[2].set_xticklabels(x_tick_label_list)
    # ax[2].set_ylim(0, 5000)
    # set y axis to log scale
    ax[2].set_yscale('log')

    ax[2].set_xlabel('Scenarios \n (c) Computation time')
    ax[2].set_ylabel('Computation time (s)')
    ax[2].grid(lw=0.25, clip_on=False)


    fig.set_size_inches(fig_width * 2, fig_height * 3 / 4)

    # adjust the space between the first subplot and the second subplot
    fig.subplots_adjust(left=.07, bottom=.26, right=.98, top=.91,
                        wspace=0.3)
    if double_axis_flag:
        mpl.pyplot.subplots_adjust(wspace=0.45)
        # Get the positions of the original subplots
        pos0 = ax[0].get_position()
        pos1 = ax[1].get_position()
        pos2 = ax[2].get_position()

        # Adjust the position of the second subplot (increase space between first and second)
        new_pos1 = [pos1.x0 + 0.025, pos1.y0, pos1.width, pos1.height]  # Increase x0 to move it right
        ax[1].set_position(new_pos1)
    else:
        mpl.pyplot.subplots_adjust(wspace=0.3)

    if double_axis_flag:
        ############################## Add first purple dashed arrow ########################################
        # 椭圆中心和大小
        ellipse_center_x = 0.9
        ellipse_center_y = 70
        ellipse_width = 0.38
        ellipse_height = 5

        # 在柱状图上添加紫色虚线椭圆
        ellipse = patches.Ellipse((ellipse_center_x, ellipse_center_y), width=ellipse_width, height=ellipse_height,
                                  edgecolor='purple', facecolor='none', linestyle='dashed')
        ax[0].add_patch(ellipse)

        # 计算箭头的起始点和结束点
        arrow_start_x = ellipse_center_x - ellipse_width / 2 + 0.05 # 椭圆左侧边缘
        arrow_start_y = ellipse_center_y
        arrow_end_x = 0.42  # 指向y轴的方向
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
        ellipse_center_x = 1.3
        ellipse_center_y = 80
        ellipse_width = 0.38
        ellipse_height = 5

        # 在柱状图上添加紫色虚线椭圆
        ellipse = patches.Ellipse((ellipse_center_x, ellipse_center_y), width=ellipse_width, height=ellipse_height,
                                  edgecolor='purple', facecolor='none', linestyle='dashed')
        ax[0].add_patch(ellipse)

        # 计算箭头的起始点和结束点
        arrow_start_x = ellipse_center_x + ellipse_width / 2 - 0.05  # 椭圆左侧边缘
        arrow_start_y = ellipse_center_y
        arrow_end_x = ellipse_center_x + ellipse_width / 2 + 0.38  # 指向y轴的方向
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
        ellipse_center_x = 0.3
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
        arrow_end_x = ellipse_center_x# - 0.42 #0.42  # 指向y轴的方向
        arrow_end_y = ellipse_center_y - 2.3     * ellipse_height
        # 添加紫色虚线箭头
        # -|>
        arrow_style = patches.FancyArrowPatch((arrow_start_x, arrow_start_y), (arrow_end_x, arrow_end_y),
                                              connectionstyle="arc3", color='purple',
                                              arrowstyle='->', lw=1, mutation_scale=5)
                                              # path_effects=[withStroke(linewidth=2, foreground='purple', linestyle='dashed')])

        ax[0].add_patch(arrow_style)

        ############################## Add second purple dashed arrow ########################################
        # 椭圆中心和大小
        ellipse_center_x = 1.3
        ellipse_center_y = 100
        ellipse_width = 0.5
        ellipse_height = 2

        # 在柱状图上添加紫色虚线椭圆
        ellipse = patches.Ellipse((ellipse_center_x, ellipse_center_y), width=ellipse_width, height=ellipse_height,
                                  edgecolor='purple', facecolor='none', linestyle='dashed')
        ax[0].add_patch(ellipse)
        ellipse.set_clip_on(False)

        # 计算箭头的起始点和结束点
        arrow_start_x = ellipse_center_x# - ellipse_width / 2 + 0.05 # 椭圆左侧边缘
        arrow_start_y = ellipse_center_y - ellipse_height / 2
        arrow_end_x = ellipse_center_x - 0.2# - 0.42 #0.42  # 指向y轴的方向
        arrow_end_y = ellipse_center_y - 2.3     * ellipse_height
        # 添加紫色虚线箭头
        # -|>
        arrow_style = patches.FancyArrowPatch((arrow_start_x, arrow_start_y), (arrow_end_x, arrow_end_y),
                                              connectionstyle="arc3", color='purple',
                                              arrowstyle='->', lw=1, mutation_scale=5)
        # path_effects=[withStroke(linewidth=2, foreground='purple', linestyle='dashed')])

        ax[0].add_patch(arrow_style)


    if double_axis_flag:
        fig.savefig('figures/' + topology + '/fig1_compare_ILP_heuristic_double_axis_sp.pdf')
    else:
        fig.savefig('figures/' + topology + '/fig1_compare_ILP_heuristic_one_axis_sp.pdf')


def analyze_availability(topology, av_matrix, twc_matrix, computation_time_matrix, scenario_legend_list):
    approach_list = ["SP", "SVNM", "SINC", "SINC+"]
    scenario_list = ["ILP-Ring", "H-Ring", "ILP-Mesh", "H-Mesh"]
    file_name = "description/compare_ILP_heuristic_" + topology + "_av.txt"
    with open(file_name, "w") as file:
        # for ILP-Ring, SINC improves the availability by xx% compared to SVNM
        improvement = av_matrix[2, 0] - av_matrix[1, 0]
        improvement = round(improvement, 2)
        file.write("For ILP-Ring, SINC improves the availability by " + str(improvement) + "% compared to SVNM.\n")
        # for ILP-Ring, SINC+ improves the availability by xx% compared to SINC+
        improvement = av_matrix[3, 0] - av_matrix[2, 0]
        improvement = round(improvement, 2)
        file.write("For ILP-Ring, SINC+ improves the availability by " + str(improvement) + "% compared to SINC.\n")

        # for ILP-Ring, SINC requires xx% additional wavelength compared to SVNM
        additional_wavelength = twc_matrix[2, 0] - twc_matrix[1, 0]
        additional_wavelength_percentage = round(additional_wavelength / twc_matrix[1, 0] * 100, 2)
        file.write("For ILP-Ring, SINC requires " + str(additional_wavelength_percentage) + "% additional wavelength compared to SVNM.\n")
        # for ILP-Ring, SINC+ requires xx% additional wavelength compared to SINC
        additional_wavelength = twc_matrix[3, 0] - twc_matrix[2, 0]
        additional_wavelength_percentage = round(additional_wavelength / twc_matrix[2, 0] * 100, 2)
        file.write("For ILP-Ring, SINC+ requires " + str(additional_wavelength_percentage) + "% additional wavelength compared to SINC.\n")

        file.write("\n")
        # for ILP-Mesh, the availability of SVNM is xx%
        file.write("For ILP-Mesh, the availability of SVNM is " + str(av_matrix[1, 2]) + "%.\n")
        # for ILP-Mesh, the availability of SINC is xx%
        file.write("For ILP-Mesh, the availability of SINC is " + str(av_matrix[2, 2]) + "%.\n")
        # for ILP-Mesh, the availability of SINC+ is xx%
        file.write("For ILP-Mesh, the availability of SINC+ is " + str(av_matrix[3, 2]) + "%.\n")

        file.write("\n")
        # for Ring topology, the gap between ILP and heuristic
        for i in range(1, 4):
            gap = av_matrix[i, 0] - av_matrix[i, 1]
            gap = round(gap, 2)
            # calculate gap percentage
            gap_percentage = round(gap / av_matrix[i, 0] * 100, 2)
            file.write("For " + approach_list[i] + ", regarding availability, the gap between ILP and heuristic is " + str(gap_percentage) + "%.\n")
        # for Mesh topology, the gap between ILP and heuristic
        for i in range(1, 4):
            gap = av_matrix[i, 2] - av_matrix[i, 3]
            gap = round(gap, 2)
            # calculate gap percentage
            gap_percentage = round(gap / av_matrix[i, 2] * 100, 2)
            file.write("For " + approach_list[i] + ", regarding availability, the gap between ILP and heuristic is " + str(gap_percentage) + "%.\n")
        file.write("\n")
        # now calculate the gap for TWC
        # for Ring topology, the gap between ILP and heuristic
        for i in range(1, 4):
            gap = twc_matrix[i, 0] - twc_matrix[i, 1]
            gap = round(gap, 2)
            # calculate gap percentage
            gap_percentage = round(gap / twc_matrix[i, 0] * 100, 2)
            file.write("For " + approach_list[i] + ", regarding twc, the gap between ILP and heuristic is " + str(gap_percentage) + "%.\n")
        # for Mesh topology, the gap between ILP and heuristic
        for i in range(1, 4):
            gap = twc_matrix[i, 3] - twc_matrix[i, 2]
            gap = round(gap, 2)
            # calculate gap percentage
            gap_percentage = round(gap / twc_matrix[i, 2] * 100, 2)
            file.write("For " + approach_list[i] + ", regarding twc, the gap between ILP and heuristic is " + str(gap_percentage) + "%.\n")


if __name__ == '__main__':
    cur_topology = "german"
    # num_of_vn_list = [6, 12, 18, 24, 30]
    cur_num_instance = 10

    # cur_num_of_vn_list = [3]
    # cur_num_of_vl = 6
    # av_matrix_ring_3vn, twc_matrix_ring_3vn, shared_link_matrix_ring_3vn, computation_time_matrix_ring_3vn \
    #     = get_av_twc_shared_link_time(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list, num_of_vl=cur_num_of_vl,
    #                                 num_instance=cur_num_instance)
    #
    # av_matrix_ring_3vn_ILP = [[78.8], [78.8], [98.72], [99.15], [100.00]]
    # twc_matrix_ring_3vn_ILP = [[39], [39], [39], [41], [46]]
    # computation_time_matrix_ring_3vn_ILP = [[1], [4], [5], [35 * 60 + 50], [1 * 60 * 60 + 45 * 60 + 26]]
    #
    # 6 node
    scenario_list = ["scenario-1", "scenario-2", "scenario-3", "scenario-4", "scenario-7"]
    scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]

    cur_num_of_vn_list = [6]
    cur_num_of_vl = 6
    av_matrix_ring_6vn, twc_matrix_ring_6vn, shared_link_matrix_ring_6vn, computation_time_matrix_ring_6vn \
        = get_av_twc_shared_link_time(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list, num_of_vl=cur_num_of_vl,
                                      num_instance=cur_num_instance, scenario_list=scenario_list,
                                      scenario_legend_list=scenario_legend_list)

    av_matrix_ring_6vn_ILP = [[79.06], [79.06], [99.79], [100.00], [100.00]]
    twc_matrix_ring_6vn_ILP = [[77], [77], [77], [78], [78]]
    computation_time_matrix_ring_6vn_ILP = [[2], [25], [1 * 60 * 60 + 55 * 60 + 38], [2 * 60 * 60 + 26 * 60 + 10], [3 * 60 * 60 + 34 * 60 + 30]]

    cur_num_of_vn_list = [6]
    cur_num_of_vl = 15
    av_matrix_mesh_6vn, twc_matrix_mesh_6vn, shared_link_matrix_mesh_6vn, computation_time_matrix_mesh_6vn \
        = get_av_twc_shared_link_time(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list, num_of_vl=cur_num_of_vl,
                                      num_instance=cur_num_instance, scenario_list=scenario_list,
                                      scenario_legend_list=scenario_legend_list)

    av_matrix_mesh_6vn_ILP = [[99.81], [100.00], [100.00], [100.00], [100.00]]
    twc_matrix_mesh_6vn_ILP = [[167], [174], [167], [167], [167]]
    computation_time_matrix_mesh_6vn_ILP = [[4], [9], [5 * 60 * 60 + 26 * 60 + 10], [6 * 60 * 60 + 25 * 60 + 35], [6 * 60 * 60 + 38 * 60 + 43]]


    av_matrix_combine = np.hstack((av_matrix_ring_6vn_ILP, av_matrix_ring_6vn,
                                   av_matrix_mesh_6vn_ILP, av_matrix_mesh_6vn))
    # round the second column of av_matrix_combine to 2 decimal places
    av_matrix_combine[:, 1] = np.round(av_matrix_combine[:, 1], 2)
    twc_matrix_combine = np.hstack((twc_matrix_ring_6vn_ILP, twc_matrix_ring_6vn,
                                    twc_matrix_mesh_6vn_ILP, twc_matrix_mesh_6vn))
    # we round the second column since the first column is rounded
    # round the second column of twc_matrix_combine
    twc_matrix_combine[:, 1] = np.round(twc_matrix_combine[:, 1])
    computation_time_matrix_combine = np.hstack((computation_time_matrix_ring_6vn_ILP, computation_time_matrix_ring_6vn,
                                                 computation_time_matrix_mesh_6vn_ILP, computation_time_matrix_mesh_6vn))

    plot_av_twc_computation_time_no_sp(topology=cur_topology, av_matrix=av_matrix_combine,
                                       twc_matrix=twc_matrix_combine, computation_time_matrix=computation_time_matrix_combine,
                                       double_axis_flag=True)

    plot_av_twc_computation_time_no_sp(topology=cur_topology, av_matrix=av_matrix_combine,
                                       twc_matrix=twc_matrix_combine, computation_time_matrix=computation_time_matrix_combine,
                                       double_axis_flag=False)
    # get results with SP
    cur_topology = "german-SP"
    scenario_list_sp = ["scenario-0"]
    scenario_legend_list_sp = ["SP"]

    cur_num_of_vn_list = [6]
    cur_num_of_vl = 6
    av_matrix_ring_6vn_sp, twc_matrix_ring_6vn_sp, shared_link_matrix_ring_6vn_sp, computation_time_matrix_ring_6vn_sp \
        = get_av_twc_shared_link_time(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list, num_of_vl=cur_num_of_vl,
                                      num_instance=cur_num_instance, scenario_list=scenario_list_sp,
                                      scenario_legend_list=scenario_legend_list_sp)

    cur_num_of_vn_list = [6]
    cur_num_of_vl = 15

    av_matrix_mesh_6vn_sp, twc_matrix_mesh_6vn_sp, shared_link_matrix_mesh_6vn_sp, computation_time_matrix_mesh_6vn_sp \
        = get_av_twc_shared_link_time(topology=cur_topology, num_of_vn_list=cur_num_of_vn_list, num_of_vl=cur_num_of_vl,
                                      num_instance=cur_num_instance, scenario_list=scenario_list_sp,
                                      scenario_legend_list=scenario_legend_list_sp)
    empty_matrix = np.array([[0]])
    av_matrix_6vn_sp = np.hstack((empty_matrix, av_matrix_ring_6vn_sp, empty_matrix, av_matrix_mesh_6vn_sp))
    twc_matrix_6vn_sp = np.hstack((empty_matrix, twc_matrix_ring_6vn_sp, empty_matrix, twc_matrix_mesh_6vn_sp))
    computation_time_matrix_6vn_sp = np.hstack((empty_matrix, computation_time_matrix_ring_6vn_sp, empty_matrix, computation_time_matrix_mesh_6vn_sp))

    av_matrix_combine = np.vstack((av_matrix_6vn_sp, av_matrix_combine))
    twc_matrix_combine = np.vstack((twc_matrix_6vn_sp, twc_matrix_combine))
    computation_time_matrix_combine = np.vstack((computation_time_matrix_6vn_sp, computation_time_matrix_combine))

    row_index = [0, 1, 3, 5]
    scenario_list = ["scenario-1", "scenario-2", "scenario-3", "scenario-4", "scenario-7"]
    scenario_legend_list = ["SVNM-MinTWC", "SVNM-MaxAv", "SINC-MinTWC", "SINC-MaxAv", "SINC+"]
    av_matrix_combine = av_matrix_combine[row_index, :]
    twc_matrix_combine = twc_matrix_combine[row_index, :]
    computation_time_matrix_combine = computation_time_matrix_combine[row_index, :]
    # plot the figure with SP
    plot_av_twc_computation_time_sp(topology="german", av_matrix=av_matrix_combine,
                                    twc_matrix=twc_matrix_combine, computation_time_matrix=computation_time_matrix_combine,
                                    double_axis_flag=True)
    plot_av_twc_computation_time_sp(topology="german", av_matrix=av_matrix_combine,
                                    twc_matrix=twc_matrix_combine, computation_time_matrix=computation_time_matrix_combine,
                                    double_axis_flag=False)
    analyze_availability(topology="german", av_matrix=av_matrix_combine, twc_matrix=twc_matrix_combine,
                         computation_time_matrix=computation_time_matrix_combine, scenario_legend_list=scenario_legend_list)
    print("Finishing plotting comparison of ILP and heuristic for scenarios without SP.")
