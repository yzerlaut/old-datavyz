import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.scaling import FONTSIZE, A0_format, inch2cm, cm2inch

import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import string, datetime

# SPECIAL PYTHON PACKAGES FOR:
import svgutils.compose as sg # SVG
# import fpdf # PDF
from PIL import Image # BITMAP (png, jpg, ...)
INKSCAPE_PATH = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'

def put_list_of_figs_to_svg_fig(FIGS,
                                fig_name="fig.svg",
                                visualize=True,export_as_png=False,
                                Props = None,
                                figsize = None,
                                with_top_left_letter=False,
                                transparent=True):
    """ take a list of figures and make a multi panel plot"""
    
    label = list(string.ascii_uppercase)[:len(FIGS)]


    SIZE = []
    for fig in FIGS:
        SIZE.append(fig.get_size_inches())
    width = np.max([s[0] for s in SIZE])
    height = np.max([s[1] for s in SIZE])
    
    if Props is None:
        LABELS, XCOORD, YCOORD = [], [], []

        # saving as svg
        for i in range(len(FIGS)):
            LABELS.append(label[i])
            XCOORD.append((i%3)*width*100)
            YCOORD.append(int(i/3)*height*100)
        XCOORD_LABELS,\
            YCOORD_LABELS = XCOORD, YCOORD

    else:
        XCOORD, YCOORD = Props['XCOORD'],\
                Props['YCOORD'], 
        if 'LABELS' in Props:
            LABELS = Props['LABELS']
        else:
            LABELS = ['' for x in XCOORD]
        if 'XCOORD_LABELS' in Props:
            XCOORD_LABELS,\
                YCOORD_LABELS = Props['XCOORD_LABELS'],\
                                Props['YCOORD_LABELS']
        else:
            XCOORD_LABELS,\
                YCOORD_LABELS = XCOORD, YCOORD
            
    for i in range(len(FIGS)):
        FIGS[i].savefig('/tmp/'+str(i)+'.svg', format='svg',
                        transparent=transparent)
        
    PANELS = []
    for i in range(len(FIGS)):
        PANELS.append(sg.Panel(\
            sg.SVG('/tmp/'+str(i)+'.svg').move(XCOORD[i],YCOORD[i])))
            # sg.Text(LABELS[i], 15, 10,
            #         size=FONTSIZE+1, weight='bold').move(\
                               # XCOORD_LABELS[i],YCOORD_LABELS[i]))\
        # ))
                      
    for i in range(len(LABELS)):
        PANELS.append(sg.Panel(\
            sg.Text(LABELS[i], 15, 10,
                    size=FONTSIZE+1, weight='bold').move(\
                                                       XCOORD_LABELS[i],YCOORD_LABELS[i]))\
        )

    if figsize is None:
        sg.Figure("21cm", "29.7cm", *PANELS).save(fig_name)
    else:
        sg.Figure(str(inch2cm(figsize[0]*A0_format['width'])[0])+"cm",\
                  str(inch2cm(figsize[1]*A0_format['height'])[0])+"cm", *PANELS).scale(1.25).save(fig_name)

    if visualize:
        os.system('open '+fig_name) # works well with 'Gapplin' on OS-X
        ## KEEP -> previous version
        # os.system('convert '+fig_name+' '+fig_name.replace('.svg', '.png'))
        # plt.close('all')
        # z = plt.imread(fig_name.replace('.svg', '.png'))
        # plt.imshow(z)
        # fig = plt.gcf()
        # # if figsize is not None:
        # #     fig.set_size_inches(fig.get_size_inches()[0]*3,
        # #                         fig.get_size_inches()[1]*3,
        # #                         forward=True)
        # if not no_show:
        #     from graphs.my_graph import show
        #     show()

def export_as_png(fig_name, dpi=300):
    instruction = INKSCAPE_PATH+' '+fig_name+' --export-area-drawing --export-png='+\
                    fig_name.replace('.svg', '.png')+' --export-dpi='+str(dpi)
    os.system(instruction)
        
def put_list_of_figs_to_multipage_pdf(FIGS,
                                      pdf_name='figures.pdf',
                                      pdf_title=''):
    """
    adapted from:
    http://matplotlib.org/examples/pylab_examples/multipage_pdf.html
    """
    
    # Create the PdfPages object to which we will save the pages:
    # The with statement makes sure that the PdfPages object is closed properly at
    # the end of the block, even if an Exception occurs.
    with PdfPages(pdf_name) as pdf:
        
        for fig in FIGS:
            pdf.savefig(fig)  # saves the current figure into a pdf page

        # We can also set the file's metadata via the PdfPages object:
        d = pdf.infodict()
        d['Title'] = pdf_title
        d['Author'] = u'Y. Zerlaut'
        # d['Keywords'] = 'PdfPages multipage keywords author title subject'
        d['CreationDate'] = datetime.datetime(2009, 11, 13)
        d['ModDate'] = datetime.datetime.today()


def concatenate_pngs(PNG_LIST, ordering='vertically', figname='fig.png'):
    
    images = map(Image.open, PNG_LIST)
    widths, heights = zip(*(i.size for i in images))

    if ordering=='vertically':
        total_height = sum(heights)
        max_width = max(widths)
        new_im = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for fig in PNG_LIST:
            im = Image.open(fig)
            new_im.paste(im, (0, y_offset))
            y_offset += im.size[1]

    new_im.save(figname)


if __name__=='__main__':

    from my_graph import *

    fig1, ax1 = plot(Y=np.random.randn(10,4),\
                     sY=np.random.randn(10,4))
    ax1.annotate('a', (0.,.9), xycoords='axes fraction', fontsize=FONTSIZE+1, weight='bold')
    fig1.savefig('fig1.svg')
    fig2, ax2 = scatter(Y=np.random.randn(10,4),\
                        sY=np.random.randn(10,4))
    curdir=os.path.abspath(__file__).replace(os.path.basename(__file__),'')

    # put_list_of_figs_to_multipage_pdf([fig1, fig2])
    put_list_of_figs_to_svg_fig([fig1, fig2, fig1],
                                fig_name=curdir+'fig.svg',
                                Props={'XCOORD':[10,160,310],
                                       'YCOORD':10*np.ones(3),
                                       'LABELS':['a','b','c']},
                                figsize=(.9,.2),
                                visualize=False, export_as_png=True, transparent=True)
    
    export_as_png(curdir+'fig.svg')
