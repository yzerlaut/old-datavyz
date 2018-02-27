import matplotlib.pylab as plt

def add_inset(ax, rect=[.9,.3,.05,.6], facecolor='w'):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)    
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x,y,width,height],facecolor=facecolor)
    # x_labelsize = subax.get_xticklabels()[0].get_size()
    # y_labelsize = subax.get_yticklabels()[0].get_size()
    # x_labelsize *= rect[2]**0.5
    # y_labelsize *= rect[3]**0.5
    # subax.xaxis.set_tick_params(labelsize=x_labelsize)
    # subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax
