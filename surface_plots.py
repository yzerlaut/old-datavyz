import numpy as np
from matplotlib import cm

def twoD_plot(ax, x, y, z, alpha=1.,
              cmap=cm.viridis,
              diverging=False,
              vmin=None, vmax=None,
              interpolation='none'):
    """
    surface plots for x, y and z 1 dimensional data
    """
    
    if diverging and (cmap==cm.viridis):
        cmap = cm.PiYG # we switch to a diverging colormap

        
    x, y = np.array(x), np.array(y)
    Z = np.ones((len(np.unique(y)), len(np.unique(x))))*np.nan
    for i, yy in enumerate(np.unique(y)):
        cond1 = y==yy
        for j, xx in enumerate(np.unique(x[cond1])):
            Z[i,j] = z[cond1][x[cond1]==xx]
    z1 = np.array(Z).reshape(len(np.unique(y)), len(np.unique(x)))
    z1 = Z
    
    if vmin is None:
        if diverging:
            vmin = -np.max(np.abs(z))
        else:
            vmin = np.min(z)
    if vmax is None:
        if diverging:
            vmax = np.max(np.abs(z))
        else:
            vmax = np.max(z)
            
    ac = ax.imshow(z1, interpolation=interpolation,
                   extent = (x.min(), x.max(), y.min(), y.max()),
                   vmin = vmin,
                   vmax = vmax,
                   alpha=alpha, cmap=cmap,
                   origin='lower', aspect='auto')
    return ac, vmin, vmax
    

if __name__=='__main__':
    from my_graph import *
    
    x, y = np.meshgrid(np.arange(1, 11), np.arange(1, 11))
    z = np.sqrt(x*y)
    x, y, z = np.array(x).flatten(),\
              np.array(y).flatten(),\
              np.array(z).flatten()*np.random.randn(len(z.flatten()))
    index = np.arange(len(x))
    np.random.shuffle(index)
    x, y, z = x[index], y[index], z[index]
    # x, y, z = x[z>20], y[z>20], z[z>20]
    fig, ax = figure(figsize=(.25,.1), right=.7)
    # ax = twoD_plot(plt.gca(), x[x<y], y[x<y], z[x<y]*0.+1, cmap=cm.Greys)
    acb = plt.axes([.75,.3,.03,.55], facecolor='b')
    ac, vmin, vmax = twoD_plot(ax, x, y, z, interpolation='bilinear', diverging=True)
    # ac = twoD_plot(ax, x, y, np.log(z)/np.log(10), interpolation='bilinear', diverging=True)
    build_bar_legend(np.logspace(np.log(vmin)/np.log(10),
                                 np.log(vmax)/np.log(10), 6),\
                     acb, viridis)
    set_plot(ax)
    show()
