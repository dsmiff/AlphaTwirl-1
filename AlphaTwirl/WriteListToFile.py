# Tai Sakuma <tai.sakuma@cern.ch>
from .mkdir_p import mkdir_p
from .listToAlignedText import listToAlignedText
import os

##__________________________________________________________________||
class WriteListToFile(object):
    def __init__(self, outPath):
        self._outPath = outPath

    def deliver(self, results):
        if results is None: return
        f = self._open(self._outPath)
        f.write(listToAlignedText(results))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
