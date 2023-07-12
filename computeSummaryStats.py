#ComputeSummaryStats returns summary statistics for a squiggle distribution

import numpy as np

def computeSummaryStats(dist,printEn=False,name="",numSamples=10000):
    samples = dist @ numSamples
    samplesArr = np.array(samples)
    sumStats = np.percentile(samplesArr, [5, 25, 50, 75, 95]) 
    if printEn:
        print("Summary Statistics: {}".format(name))
        print("5th, 25th, 50th, 75th, 95th percentiles:")
        print("{}".format(sumStats))
        print("Mean:")
        print(" {}".format(np.mean(samplesArr)))
    return sumStats,samples