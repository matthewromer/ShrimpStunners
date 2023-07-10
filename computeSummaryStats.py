#ComputeSummaryStats returns summary statistics for a squiggle distribution

import numpy as np

def computeSummaryStats(dist,printEn=False,name="",numSamples=10000):
    samples = dist @ numSamples
    samplesArr = np.array(samples)
    sumStats = np.percentile(samplesArr, [5, 50, 95]) 
    if printEn:
        print("Summary Statistics: {}".format(name))
        print("5th, 50th, 95th percentiles: {}".format(sumStats))
        print("Mean: {}".format(np.mean(samplesArr)))
    return sumStats