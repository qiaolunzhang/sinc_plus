import matplotlib.pyplot as plt

# Example data
x = [1, 2, 3, 4, 5]  # X-axis data
y1 = [82, 86, 88, 90, 93]  # Data ranging from 80 to 100
y2 = [99.1, 99.3, 99.5, 99.7, 99.9]  # Data ranging from 99 to 100

fig, ax1 = plt.subplots()

# Plotting the data for the first y-axis
ax1.set_xlabel('X Axis Label')
ax1.set_ylabel('Range 80 to 100', color='tab:red')
ax1.plot(x, y1, 'r-')  # 'r-' indicates red solid line
ax1.tick_params(axis='y', labelcolor='tab:red')

# Creating a second y-axis
ax2 = ax1.twinx()
ax2.set_ylabel('Range 99 to 100', color='tab:blue')
ax2.plot(x, y2, 'b-')  # 'b-' indicates blue solid line
ax2.tick_params(axis='y', labelcolor='tab:blue')

fig.tight_layout()  # Adjust layout for neatness
plt.show()
