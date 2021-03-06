import AlphaTwirl.Counter as Counter
import unittest

##__________________________________________________________________||
class MockEvent(object):
    pass

##__________________________________________________________________||
class MockCounts(object):
    def __init__(self):
        self._counts = [ ]
        self._keys = set()
        self._addedkeys = set()

    def count(self, key, weight):
        self._counts.append((key, weight))
        self._keys.add(key)

    def keys(self):
        return list(self._keys)

    def addKey(self, key):
        self._addedkeys.add(key)

    def valNames(self):
        return ('n', 'nvar')

    def copyFrom(self, src):
        self._counts[:] = src._counts[:]

    def results(self):
        return self._counts

##__________________________________________________________________||
class MockWeightCalculator(object):
    def __call__(self, event):
        return 1.0

##__________________________________________________________________||
class MockBinning(object): pass

##__________________________________________________________________||
class MockKeyComposer(object):
    def __init__(self, listOfKeys = [ ]):
        self.listOfKeys = listOfKeys
        self._begin = None

    def begin(self, event):
        self._begin = event

    def __call__(self, event):
        return self.listOfKeys.pop()

##__________________________________________________________________||
class MockNextKeyComposer(object):
    def __init__(self, nextdic):
        self.nextdic = nextdic

    def __call__(self, key):
        return self.nextdic[key]

##__________________________________________________________________||
class TestMockKeyComposer(unittest.TestCase):

    def test_call(self):
        keys = [(13, 5), (11, 2), (11, 10), (2, 22)]
        keycomposer = MockKeyComposer(keys)
        self.assertEqual((2, 22), keycomposer(MockEvent()))
        self.assertEqual((11, 10), keycomposer(MockEvent()))
        self.assertEqual((11, 2), keycomposer(MockEvent()))
        self.assertEqual((13, 5), keycomposer(MockEvent()))
        self.assertRaises(IndexError, keycomposer, MockEvent())

##__________________________________________________________________||
class TestCounter(unittest.TestCase):

    def test_events(self):
        counts = MockCounts()
        listOfKeys = [[(11, ), (12, )], [(12, )], [ ], [(14, )], [(11, )]]
        keycomposer = MockKeyComposer(listOfKeys)
        nextdic = {(11, ): ((12, ), ), (12, ): ((13, ), ), (14, ): ((15, ), )}
        nextKeyComposer = MockNextKeyComposer(nextdic)
        counter = Counter.Counter(keycomposer, counts, nextKeyComposer, MockWeightCalculator())

        event = MockEvent()
        counter.begin(event)
        self.assertEqual(event, keycomposer._begin)

        event = MockEvent()
        counter.event(event)
        self.assertEqual([((11, ), 1.0)], counts._counts)
        self.assertEqual([((11, ), 1.0)], counter.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0)], counts._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0)], counts.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0), ((11,), 1.0), ((12,), 1.0)], counts._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0), ((11,), 1.0), ((12,), 1.0)], counts.results())

        counter.end()
        self.assertEqual(set([(15, ), (13, ), (12, )]), counts._addedkeys)

    def test_default_weight(self):
        counts = MockCounts()
        listOfKeys = [[(11, ), (12, )], [(12, )], [ ], [(14, )], [(11, )]]
        keycomposer = MockKeyComposer(listOfKeys)
        nextdic = {(11, ): ((12, ), ), (12, ): ((13, ), ), (14, ): ((15, ), )}
        nextKeyComposer = MockNextKeyComposer(nextdic)
        counter = Counter.Counter(keycomposer, counts, nextKeyComposer)

        self.assertIsInstance(counter.weightCalculator, Counter.WeightCalculatorOne)

        event = MockEvent()
        counter.event(event)
        self.assertEqual([((11, ), 1.0)], counts._counts)
        self.assertEqual([((11, ), 1.0)], counter.results())

    def test_copyFrom(self):
        counts = MockCounts()
        counter = Counter.Counter(MockKeyComposer(), counts, MockWeightCalculator())

        src_counts = MockCounts()
        src_counter = Counter.Counter(MockKeyComposer(), src_counts, MockWeightCalculator())
        src_counts._counts[:] = [((11, ), 1.0)]

        self.assertEqual([ ], counts._counts)
        counter.copyFrom(src_counter)
        self.assertEqual([((11,), 1.0)], counts._counts)

##__________________________________________________________________||
