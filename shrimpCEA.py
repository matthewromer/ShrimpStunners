# Script to analyze relative cost-effectiveness of the Shrimp Welfare Project's
# electrical stunner program compared to corporate cage-free chicken campaigns 
#
# The goal is to compare the number of hours of human-equivalent disabling pain 
# averted per dollar donated to each cause. This script uses the Rethink 
# Priorities moral weights to weight pain across species, and assumes that the
# pain averted via electrical stunning is at the disabling level 
#

############################# SETUP #############################
import squigglepy as sq
import pickle
from computeSummaryStats import computeSummaryStats
from plotSquiggleDist import plotSquiggleDist
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

#Number of samples to use when sampling distributions 
numSamples = 20000

#Plot options
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
my_pal = {"lightsteelblue","lightcoral"}
sns.set_style(style='white')

#Enable or disable clipping shrimp moral weight distribution
clipShrimpWeight = False

############################# INPUTS #############################

#Import moral weight project results 
shrimpSimData         = pickle.load(open('shrimp_wr_Mixture Neuron Count_model.p', 'rb'))
if clipShrimpWeight: 
    shrimpArr = np.array(shrimpSimData)
    shrimpArr[shrimpArr > 0.1] = 0.1
    shrimpSimData = shrimpArr.tolist()
moralWeightS          = sq.discrete(shrimpSimData)

chickenSimData        = pickle.load(open('chickens_wr_Mixture Neuron Count_model.p', 'rb'))
moralWeightC          = sq.discrete(chickenSimData)

#Data for SWP 
animalsPerDollarS     = sq.norm(mean=14796, sd=7708,lclip=0.0)
hoursPerAnimalS       = sq.lognorm(mean=np.log(20),sd=((np.log(180)-np.log(20))/2))/(60) #Hours
probRenderedUnconS    = 2/3
sufferingIntensityS   = sq.gamma(1.5,1.0,lclip=0.15,rclip=5)

#Data for corporate campaigns (e.g. THL) from Duffy (2023)
hoursPerDollarC = sq.gamma( 1.7, 1)*(365*24)

############################ COMPUTATION ###########################

#Obtain hours of disabling-equivalent pain removed per dollar donated to SWP's 
#intervention 
hoursPerDollarS       = animalsPerDollarS*hoursPerAnimalS*probRenderedUnconS*sufferingIntensityS

#Multiply by the RP moral weights to obtain weighted hours of 
#suffering disabling-equivalent pain averted per dollar 
weightedHoursPerDollarS = moralWeightS*hoursPerDollarS
weightedHoursPerDollarC = moralWeightC*hoursPerDollarC

#Summary stats 
sumStatWelfareRangeS,samplesWelfareRangeS = computeSummaryStats(moralWeightS,printEn=True,name='Moral Weight of Shrimp:',numSamples = numSamples)
sumStatWelfareRangeC,samplesWelfareRangeC = computeSummaryStats(moralWeightC,printEn=True,name='Moral Weight of Chickens:',numSamples = numSamples)
sumStatsHoursPerDollarS,samplesHoursPerDollarS = computeSummaryStats(weightedHoursPerDollarS,printEn=True,name='Human-Equivalent Hours Suffering Averted Per Dollar Donated to SWP:',numSamples = numSamples)
sumStatsHoursPerDollarC,samplesHoursPerDollarC = computeSummaryStats(weightedHoursPerDollarC,printEn=True,name='Human-Equivalent Hours Suffering Averted Per Dollar Donated to THL:',numSamples = numSamples)

############################## PLOTS #############################

#Welfare capacity ranges
boxData = [samplesWelfareRangeS, samplesWelfareRangeC]
fig, ax = plt.subplots(figsize = (7,4),dpi=900)
ax.set_xscale("log")
sns.boxplot(data=boxData, orient='h', ax=ax, showfliers=True, palette=my_pal)
ax.set_yticks([0, 1])
ax.set_yticklabels(["Shrimp","Chickens"])
ax.set_title("Welfare Capacity Ranges")
ax.set_xlabel("Welfare Capacity Range (Frac. of Human)")
name = './Plots/Box Welfare Capacity Range.png' 
fig.savefig(name)
plotSquiggleDist(moralWeightS,printEn=True,
                 titleTxt="Welfare Capacity Ranges (Zoomed)",
                 xText="Welfare Capacity Range (Frac. of Human)",
                 xlims = [0.0,1.5],
                 bins  = 40,
                 dist2 = moralWeightC,
                 bins2=40,
                 name1='Shrimp',
                 name2='Chickens',
                 data1 = samplesWelfareRangeS,
                 data2 = samplesWelfareRangeC)

#Hours of suffering per shrimp
plotSquiggleDist(sufferingIntensityS,printEn=True,
                 titleTxt="Pain Intensity for Slaughtered Shrimp",
                 numSamples = 10000,
                 xText="Pain Intensity (0.15 = Hurtful, 1 = Disabling, 5 = Excruciating)",
                 bins  = 40,
                 xlims = [0,5])

#Intensity of shrimp suffering 
plotSquiggleDist(hoursPerAnimalS,printEn=True,
                 titleTxt="Hours of Suffering for Slaughtered Shrimp",
                 numSamples = 10000,
                 xText="Duration of Suffering During Slaughter (Hours)",
                 bins  = 40,
                 xlims = [0,10])

#Shrimp helped per dollar
plotSquiggleDist(animalsPerDollarS,printEn=True,
                 titleTxt="Animals Helped per Dollar Given to SWP",
                 numSamples = 200000,
                 xText="Animals Impacted",
                 xlims = [0,50000],
                 bins  = 80)

#Chicken suffering per dollar
plotSquiggleDist(hoursPerDollarC,printEn=True,
                 titleTxt="Pain Averted Per Dollar for Corp. Campaigns",
                 numSamples = 100000,
                 xText="Disabling Pain Averted (Hours Per Dollar)",
                 bins  = 100,
                 xlims = [0,100000])


#Weighted Results 
plotSquiggleDist(weightedHoursPerDollarS,printEn=True,
                 titleTxt="Weighted Pain Averted Per Dollar (Zoomed)",
                 numSamples = 10000,
                 xText="Disabling Pain Averted (Weighted Hours Per Dollar)",
                 xlims = [0,5000],
                 bins  = 100,
                 dist2 = weightedHoursPerDollarC,
                 bins2=100,
                 name1='Shrimp Stunners',
                 name2='Corp. Campaigns',
                 data1 = samplesHoursPerDollarS, 
                 data2 = samplesHoursPerDollarC)


#Weighted Results (Box Plot)
boxData = [samplesHoursPerDollarS, samplesHoursPerDollarC]
fig, ax = plt.subplots(figsize = (7,4),dpi=900)
ax.set_xscale("log")
sns.boxplot(data=boxData, orient='h', ax=ax, showfliers=True, palette=my_pal)
ax.set_yticks([0, 1])
ax.set_yticklabels(["Shrimp \n Stunners","Corp. Hen \n Welfare \n Campaigns"])
if clipShrimpWeight:
    ax.set_title("Weighted Pain Averted Per Dollar (Log Scale) - Shrimp Welfare Range Capped")    
else:
    ax.set_title("Weighted Pain Averted Per Dollar (Log Scale)")        
ax.set_xlabel("Disabling Pain Averted (Weighted Hours Per Dollar)")
ax.set_xlim(5e-2, 1e6)
name = './Plots/Box Weighted Pain Averted Per Dollar.png' 
fig.savefig(name)