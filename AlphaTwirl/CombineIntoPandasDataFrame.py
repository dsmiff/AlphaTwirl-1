# Tai Sakuma <tai.sakuma@cern.ch>

from Combine import Combine
import pandas

##__________________________________________________________________||
def countsToDataFrame(counts, keyNames):
    valNames = counts.values()[0].keys()
    d = [k + tuple([v[n] for n in valNames]) for k, v in counts.iteritems()]
    d.sort()
    columns = tuple(keyNames) + tuple(valNames)
    return pandas.DataFrame(d, columns = columns)

##__________________________________________________________________||
class CombineIntoPandasDataFrame(object):
    def __init__(self, keyNames):
        self.datasetColumnName = 'component'
        self.keyNames = keyNames

    def combine(self, datasetReaderPairs):
        if len(datasetReaderPairs) == 0: return None
        combine = Combine()
        combined = combine.combine(datasetReaderPairs)
        reader = datasetReaderPairs[0][1]
        if len(combined) == 0:
            columns = (self.datasetColumnName, ) + tuple(self.keyNames) + tuple(reader.valNames())
            d = dict([(e, [ ]) for e in columns])
            return pandas.DataFrame(d, columns = columns)
        return countsToDataFrame(combined, (self.datasetColumnName, ) + self.keyNames)

##__________________________________________________________________||
