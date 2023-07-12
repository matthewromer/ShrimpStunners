#plotSquiggleDist creates a nicely-formatted plot for a squiggle distribution 
#
# Some code from https://towardsdatascience.com/take-your-histograms-to-the-next-level-using-matplotlib-5f093ad7b9d3


import squigglepy as sq
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,FormatStrFormatter,MaxNLocator
import pandas as pd
import contextlib
import numpy as np

def plotSquiggleDist(dist,printEn=False,titleTxt="",numSamples = 10000,
                     xText="",xlims = [0,0],bins=25,dist2=sq.norm(0,0),
                     bins2=25,name1="",name2="",data1=np.ndarray(0),data2=np.ndarray(0)):

    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = 'Arial'

    
    #Generate samples and store in data frame
    if data1.size == 0:
        samples = dist @ numSamples
    else:
        samples = data1
        
    if xlims != [0,0]:
        samples = samples[samples>=xlims[0]]
        samples = samples[samples<=xlims[1]]
    df = pd.DataFrame(data={name1:samples})

    #Create figure
    fig, ax = plt.subplots(figsize = (7,3.5),dpi=900)
    
    #Plot histogram and kde 
    df.plot(kind = "hist", density = True, alpha = 0.65, bins = bins,ax=ax, color = "lightsteelblue", lw=0) 
    df.plot(kind = "kde",ax=ax, color = "navy", legend=False)
    
    #If 2nd histogram was populated, plot it
    if dist2.mean != 0.0:
        if data2.size == 0:
            samples = dist2 @ numSamples
        else:
            samples = data2       
        if xlims != [0,0]:
            samples = samples[samples>xlims[0]]            
            samples = samples[samples<xlims[1]]
        df = pd.DataFrame(data={name2:samples})
        df.plot(kind = "hist", density = True, alpha = 0.65, bins = bins2,ax=ax, color = "lightcoral", lw=0) 
        df.plot(kind = "kde",ax=ax, color = "maroon", legend=False)
    else:
        #Remove legend 
        with contextlib.redirect_stdout(None):
            legend = ax.legend()
            legend.remove()
        
        #Add Quantile lines
        ymin, ymax = ax.get_ylim()   
        quant_5  = df.quantile(0.05)
        quant_25 = df.quantile(0.25)
        quant_50 = df.quantile(0.50)
        quant_75 = df.quantile(0.75)
        quant_95 = df.quantile(0.95)
        quants = [[quant_5.values.tolist(), 0.16], 
                  [quant_25.values.tolist(), 0.26], 
                  [quant_50.values.tolist(), 0.36],  
                  [quant_75.values.tolist(), 0.46], 
                  [quant_95.values.tolist(), 0.56]]
        for i in quants:
            ax.axvline(i[0], alpha = 0.6, ymax = i[1], linestyle = ":")
                
        #Annotations
        ax.text(quant_5-.1, ymax*0.17, "5th", size = 11, alpha = 0.85)
        ax.text(quant_25-.13, ymax*0.27, "25th", size = 11, alpha = 0.85)
        ax.text(quant_50-.13, ymax*0.37, "50th", size = 11, alpha = 0.85)
        ax.text(quant_75-.13, ymax*0.47, "75th", size = 11, alpha = 0.85)
        ax.text(quant_95-.25, ymax*0.57, "95th Percentile", size = 11, alpha =0.85)            
        
    
    #X
    ax.set_xlabel(xText)
    if xlims != [0,0]:
        ax.set_xlim(xlims[0], xlims[1])
    
    #Y
    #ax.set_yticklabels([])
    ax.set_ylabel("Probability Density")
    
    #Overall
    ax.grid(False)
    ax.set_title(titleTxt, size = 17, pad = 10)
    
    #Add borders
    ax.patch.set_edgecolor('black')  
    ax.patch.set_linewidth('1')
    
    #Remove ticks and spines
    ax.tick_params(left = False, bottom = False)
    for ax, spine in ax.spines.items():
        spine.set_visible(False)

    plt.show()
    
    if printEn:
        name = './Plots/%s.png' % titleTxt
        fig.savefig(name)

        