import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockCounts(object):
    def __init__(self):
        self._counts = [ ]
        self._keys = [ ]

    def count(self, key, weight):
        self._counts.append((key, weight))

    def addKeys(self, keys):
        self._keys.append(keys)

##____________________________________________________________________________||
class MockKeyGapKeeper(object):
    def __init__(self):
        self.keys = [ ]
        self.updates = [ ]
        self.nexts = [ ]

    def update(self, key):
        self.keys.append(key)
        return self.updates.pop()

    def next(self, key):
        return self.nexts.pop()

##____________________________________________________________________________||
class TestCountsWithEmptyKeysInGap(unittest.TestCase):

    def test_count(self):
        counts = MockCounts()
        keys = [(14, ), (11, )]
        keyGapKeeper = MockKeyGapKeeper()
        keyGapKeeper.updates = [[(11, ), (12, ), (13, ), (14, )], [()]]
        countsWEKIG = Counter.CountsWithEmptyKeysInGap(counts, keyGapKeeper)

        countsWEKIG.count((11, ), 1)
        self.assertEqual([(11,)], keyGapKeeper.keys)
        self.assertEqual([((11,), 1.0)], counts._counts)
        self.assertEqual([[()]], counts._keys)

        countsWEKIG.count((14, ), 1)
        self.assertEqual([(11, ), (14, )], keyGapKeeper.keys)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
        self.assertEqual([[()], [(11, ), (12, ), (13, ), (14, )]], counts._keys)

##____________________________________________________________________________||
class TestCountsWithEmptyKeysInGapAndNext(unittest.TestCase):

    def test_count(self):
        counts = MockCounts()
        keyGapKeeper = MockKeyGapKeeper()
        countsWEKIG = Counter.CountsWithEmptyKeysInGapAndNext(counts, keyGapKeeper)

        keyGapKeeper.updates = [[()], [()]]
        keyGapKeeper.nexts = [(12, )]
        countsWEKIG.count((11, ), 1)
        self.assertEqual([(11,), (12,)], keyGapKeeper.keys)
        self.assertEqual([((11,), 1.0)], counts._counts)
        self.assertEqual([[()], [()]], counts._keys)

        keyGapKeeper.updates = [[(15, )], [(13, ), (14, )]]
        keyGapKeeper.nexts = [(15, )]
        countsWEKIG.count((14, ), 1)
        self.assertEqual([(11, ), (12, ), (14, ), (15, )], keyGapKeeper.keys)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], counts._counts)
        self.assertEqual([[()], [()], [(13, ), (14, )], [(15, )]], counts._keys)

##____________________________________________________________________________||
class TestCountsWithEmptyKeysInGapBuilder(unittest.TestCase):

    def test_call(self):
        builder = Counter.CountsWithEmptyKeysInGapBuilder(MockCounts, MockKeyGapKeeper)
        counts1 = builder()
        counts2 = builder()
        self.assertIsInstance(counts1, Counter.CountsWithEmptyKeysInGap)
        self.assertIsInstance(counts1._countMethod, MockCounts)
        self.assertIsInstance(counts1._keyGapKeeper, MockKeyGapKeeper)
        self.assertIsNot(counts1, counts2)
        self.assertIsNot(counts1._countMethod, counts2._countMethod)
        self.assertIsNot(counts1._keyGapKeeper, counts2._keyGapKeeper)

##____________________________________________________________________________||
class TestCountsWithEmptyKeysInGapAndNextBuilder(unittest.TestCase):

    def test_call(self):
        builder = Counter.CountsWithEmptyKeysInGapAndNextBuilder(MockCounts, MockKeyGapKeeper)
        counts1 = builder()
        counts2 = builder()
        self.assertIsInstance(counts1, Counter.CountsWithEmptyKeysInGapAndNext)
        self.assertIsInstance(counts1._countMethod, MockCounts)
        self.assertIsInstance(counts1._keyGapKeeper, MockKeyGapKeeper)
        self.assertIsNot(counts1, counts2)
        self.assertIsNot(counts1._countMethod, counts2._countMethod)
        self.assertIsNot(counts1._keyGapKeeper, counts2._keyGapKeeper)

##____________________________________________________________________________||