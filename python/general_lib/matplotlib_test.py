import matplotlib
import Tkinter as tk
import matplotlib.pyplot as plt
import os


def build_sprint_chart(config, remaining_days,trend_line,remaining_effort):

    # Days
    x = remaining_days
    # Hours
    y = trend_line
    estimated_hours_left = remaining_effort
    
    # Proper subset of Days
    x2 = x[:len(estimated_hours_left)]

    plt.plot(x,y, label = 'Estimated Effort Planned')
    plt.plot(x2, estimated_hours_left, label = 'Estimated Effort Left')

    #Invert x axis and annotate with the y values
    ax = plt.gca()
    ax.invert_xaxis()
    for x, y in zip(x2, estimated_hours_left):
        if x is not None and y is not None:
            ax.annotate(y, xy = (x,y), xytext=(x, y-1))
    
    for x, y in zip(x2, trend_line):
        if x is not None and y is not None:
            ax.annotate(y, xy = (x,y), xytext=(x, y-1))

    plt.legend()
    # plt.show()       # Use this to view the plot
    chart_path = config['project']['charts']
    chart_name = 'sprint.png'
    plt.savefig(os.path.join(chart_path,chart_name))