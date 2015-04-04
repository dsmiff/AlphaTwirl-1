#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import os
import argparse
from AlphaTwirl import EventBuilder
from AlphaTwirl.HeppyResult import HeppyResult
from AlphaTwirl.Counter import Counts

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--heppydir', default = '/Users/sakuma/work/cms/c150130_RA1_data/c150130_01_PHYS14/201525_SingleMu', help = "Heppy results dir")
parser.add_argument('-o', '--outdir', default = 'tmp')
parser.add_argument("-n", "--nevents", default = -1, type = int, help = "maximum number of events to process for each component")
args = parser.parse_args()

analyzerName = 'treeProducerSusyAlphaT'
fileName = 'tree.root'
treeName = 'tree'
outPath = os.path.join(args.outdir, 'tbl_met.txt')

eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)

outFile = open(outPath, 'w')
print >>outFile, "{:>22s} {:>12s} {:>6s}".format("component", "met", "n")

heppyResult = HeppyResult(args.heppydir)
for component in heppyResult.components():

    boundaries = [10**(i*0.1) for i in range(-10, 36)]
    counts = Counts()

    events = eventBuilder.build(component)
    for event in events:

        met = event.met_pt
        met_bin = max([b for b in boundaries if b < met])

        counts.count(met_bin)

    results = counts.results()
    keys = results.keys()
    keys.sort()
    for k in  keys:
        print >>outFile, "{:>22s} {:12.6f} {:6.0f}".format(component.name, k, results[k]['n'])

##__________________________________________________________________||