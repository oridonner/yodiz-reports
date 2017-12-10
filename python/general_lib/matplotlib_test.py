import matplotlib
import Tkinter as tk
import matplotlib.pyplot as plt


def build_sprint_chart(config, sprint_headers_dict):
    TOTAL_SPRINT_DAYS = 12
    TOTAL_SPRINT_HOURS = 200

    # We want X and Y to be of the same size
    step = TOTAL_SPRINT_HOURS // TOTAL_SPRINT_DAYS +1
    step = -step

    # Days
    x=range(TOTAL_SPRINT_DAYS, 0, -1)

    # Hours
    y = range(TOTAL_SPRINT_HOURS,-1, step)

    estimated_hours_left = [200, 130, 125]

    # Proper subset of Days
    x2 = x[:len(estimated_hours_left)]

    plt.plot(x,y, label = 'Trend Line')
    plt.plot(x2, estimated_hours_left, label = 'Estimated Effort Left')

    #Invert x axis and annotate with the y values
    ax = plt.gca()
    ax.invert_xaxis()
    for x, y in zip(x2, estimated_hours_left):
        ax.annotate(y, xy = (x,y), xytext=(x, y-1))

    plt.legend()
    # plt.show()       # Use this to view the plot
    plt.savefig('nizzle2.png')