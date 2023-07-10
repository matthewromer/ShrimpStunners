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

#Number of samples to use when sampling distributions 
numSamples = 20000

############################# INPUTS #############################

#Import moral weight project results 
shrimpSimData         = pickle.load(open('shrimp_wr_Mixture Neuron Count_model.p', 'rb'))
moralWeightS          = sq.discrete(shrimpSimData)

chickenSimData        = pickle.load(open('chickens_wr_Mixture Neuron Count_model.p', 'rb'))
moralWeightC          = sq.discrete(chickenSimData)

#Data for SWP 
animalsPerDollarS     = sq.norm(mean=14796, sd=7708,lclip=0.0)
hoursPerAnimalS       = sq.lognorm(mean=np.log(15),sd=((np.log(180)-np.log(15))/2))/(60) #Hours
probRenderedUnconS    = sq.beta(a = 3, b= 1.5)

#Data for coporate campaings (e.g. THL) from Duffy (2023)
hoursPerDollarC = sq.gamma( 1.7, 1)*(365*24)

############################ COMPUTATION ###########################

#Obtain hours of disabling-equivalent pain removed per dollar donated to SWP's 
#intervention 
hoursPerDollarS       = animalsPerDollarS*hoursPerAnimalS*probRenderedUnconS

#Multiply by the RP moral weights to obtain weighted hours of 
#suffering disabling-equivalent pain averted per dollar 
weightedHoursPerDollarS = moralWeightS*hoursPerDollarS
weightedHoursPerDollarC = moralWeightC*hoursPerDollarC

#Summary stats 
computeSummaryStats(weightedHoursPerDollarS,printEn=True,name='Human-Equivalent Hours Suffering Averted Per Dollar Donated to SWP:',numSamples = numSamples)
computeSummaryStats(weightedHoursPerDollarC,printEn=True,name='Human-Equivalent Hours Suffering Averted Per Dollar Donated to THL:',numSamples = numSamples)


############################## PLOTS #############################

#Welfare capacity ranges
plotSquiggleDist(moralWeightS,printEn=True,
                 titleTxt="Welfare Capacity Ranges",
                 numSamples = 10000,
                 xText="Welfare Capacity Range (Frac. of Human)",
                 xlims = [0,20],
                 bins  = 100,
                 dist2 = moralWeightC,
                 bins2=20,
                 name1='Shrimp',
                 name2='Chickens')
plotSquiggleDist(moralWeightS,printEn=True,
                 titleTxt="Welfare Capacity Ranges (Zoomed)",
                 numSamples = 10000,
                 xText="Welfare Capacity Range (Frac. of Human)",
                 xlims = [0,1.5],
                 bins  = 40,
                 dist2 = moralWeightC,
                 bins2=40,
                 name1='Shrimp',
                 name2='Chickens')

#Shrimp helped per dollar
plotSquiggleDist(animalsPerDollarS,printEn=True,
                 titleTxt="Animals Helped per Dollar Given to SWP",
                 numSamples = 200000,
                 xText="Animals Impacted",
                 xlims = [0,50000],
                 bins  = 50)

#Hours of suffering per shrimp
plotSquiggleDist(hoursPerAnimalS,printEn=True,
                 titleTxt="Hours of Disabling Pain for Slaughtered Shrimp",
                 numSamples = 10000,
                 xText="Duration of Disabling Pain During Slaughter (Hours)",
                 xlims = [0,10])

#Chicken suffering per dollar
plotSquiggleDist(hoursPerDollarC,printEn=True,
                 titleTxt="Pain Averted Per Dollar for Corp. Campaigns",
                 numSamples = 100000,
                 xText="Disabling Pain Averted (Hours Per Dollar)",
                 bins  = 100,
                 xlims = [0,100000])

#Probability that stunners work
plotSquiggleDist(probRenderedUnconS,printEn=True,
                 titleTxt="Probability that Stunning Renders Shrimp Unconcious",
                 numSamples = 200000,
                 xText="FProbability",
                 xlims = [0,1],
                 bins  = 100)

#Weighted Results 
plotSquiggleDist(weightedHoursPerDollarS,printEn=True,
                 titleTxt="Weighted Pain Averted Per Dollar",
                 numSamples = 10000,
                 xText="Disabling Pain Averted (Weighted Hours Per Dollar)",
                 xlims = [0,5000],
                 bins  = 100,
                 dist2 = weightedHoursPerDollarC,
                 bins2=100,
                 name1='Shrimp Stunners',
                 name2='Corp. Campaigns')
plotSquiggleDist(weightedHoursPerDollarS,printEn=True,
                 titleTxt="Weighted Pain Averted Per Dollar (Zoomed)",
                 numSamples = 10000,
                 xText="Disabling Pain Averted (Weighted Hours Per Dollar)",
                 xlims = [0,200000],
                 bins  = 100,
                 dist2 = weightedHoursPerDollarC,
                 bins2=100,
                 name1='Shrimp Stunners',
                 name2='Corp. Campaigns')
