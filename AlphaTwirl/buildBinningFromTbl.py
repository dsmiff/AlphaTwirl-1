# Tai Sakuma <tai.sakuma@cern.ch>
import Binning
import pandas

##__________________________________________________________________||
def buildBinningFromTbl(path, retvalue = 'lowedge'):
    tbl = pandas.read_table(path, delim_whitespace=True)
    if retvalue == 'number':
        return Binning.Binning(bins = tbl.bin.tolist(), lows = tbl.low.tolist(), ups = tbl.up.tolist(), retvalue = retvalue)
    if retvalue == 'lowedge':
        return Binning.Binning(lows = tbl.low.tolist(), ups = tbl.up.tolist(), retvalue = retvalue)

##__________________________________________________________________||
