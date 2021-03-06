# Tai Sakuma <tai.sakuma@cern.ch>
from .EventLoop import EventLoop
from .Associator import Associator

import math

##__________________________________________________________________||
class EventReader(object):
    def __init__(self, eventBuilder, eventLoopRunner, reader, collector, maxEventsPerRun = -1):

        if maxEventsPerRun == 0:
            raise ValueError("maxEventsPerRun cannot be 0")

        self.eventBuilder = eventBuilder
        self.eventLoopRunner = eventLoopRunner
        self.associator = Associator(reader, collector)
        self.collector = collector
        self.maxEventsPerRun = maxEventsPerRun
        self.EventLoop = EventLoop

    def begin(self):
        self.eventLoopRunner.begin()

    def read(self, dataset):
        if self.maxEventsPerRun < 0:
            self._run_one_eventLoop_for_the_dataset(dataset)
        else:
            self._split_the_dataset_run_multiple_eventLoops(dataset)

    def end(self):
        self.eventLoopRunner.end()
        return self.collector.collect()

    def _run_one_eventLoop_for_the_dataset(self, dataset):
        reader = self.associator.make(dataset.name)
        eventLoop = self.EventLoop(self.eventBuilder, dataset, reader)
        self.eventLoopRunner.run(eventLoop)

    def _split_the_dataset_run_multiple_eventLoops(self, dataset):
        nTotal = self.eventBuilder.getNumberOfEventsInDataset(dataset)
        nPerRun = self.maxEventsPerRun
        for start, nEvents in self._create_start_nEvents_list(nTotal, nPerRun):
            reader = self.associator.make(dataset.name)
            eventLoop = self.EventLoop(
                self.eventBuilder, dataset, reader,
                start = start, nEvents = nEvents
            )
            self.eventLoopRunner.run(eventLoop)

    def _create_start_nEvents_list(self, nTotal, nPerRun):
        nLoops = nTotal/nPerRun
        ret = [(i*nPerRun, nPerRun) for i in range(nLoops)]
        if nTotal % nPerRun > 0:
            ret.append((nLoops*nPerRun, nTotal % nPerRun))
        return ret

##__________________________________________________________________||
