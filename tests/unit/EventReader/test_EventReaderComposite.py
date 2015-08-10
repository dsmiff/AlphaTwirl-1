from AlphaTwirl.EventReader import EventReaderComposite
import unittest

##____________________________________________________________________________||
class MockReader(object):

    def __init__(self):
        self._beganWith = None
        self._events = [ ]
        self._ended = False

    def begin(self, event):
        self._beganWith = event

    def event(self, event):
        self._events.append(event)

    def end(self):
        self._ended = True

    def copyFrom(self, src):
        self._copy = src

##____________________________________________________________________________||
class MockEvent(object):
    pass

##____________________________________________________________________________||
class TestEventReaderComposite(unittest.TestCase):

    def test_event_two_readers_two_events(self):
        """
        composite
            |- reader1
            |- reader2
        """
        composite = EventReaderComposite()
        reader1 = MockReader()
        reader2 = MockReader()
        composite.add(reader1)
        composite.add(reader2)

        events = MockEvent()
        composite.begin(events)
        self.assertIs(events, reader1._beganWith)
        self.assertIs(events, reader2._beganWith)

        event1 = MockEvent()
        composite.event(event1)

        event2 = MockEvent()
        composite.event(event2)
        self.assertEqual([event1, event2], reader1._events)
        self.assertEqual([event1, event2], reader2._events)

        composite.end()
        self.assertTrue(reader1._ended)
        self.assertTrue(reader2._ended)

    def test_event_nested_composite(self):
        """
        composite1
            |- composite2
            |      |- reader1
            |      |- reader2
            |- reader3
        """
        composite1 = EventReaderComposite()
        composite2 = EventReaderComposite()
        reader1 = MockReader()
        reader2 = MockReader()
        reader3 = MockReader()
        composite1.add(composite2)
        composite2.add(reader1)
        composite2.add(reader2)
        composite1.add(reader3)

        events = MockEvent()
        composite1.begin(events)
        self.assertIs(events, reader1._beganWith)
        self.assertIs(events, reader2._beganWith)
        self.assertIs(events, reader3._beganWith)

        event1 = MockEvent()
        composite1.event(event1)

        event2 = MockEvent()
        composite1.event(event2)
        self.assertEqual([event1, event2], reader1._events)
        self.assertEqual([event1, event2], reader2._events)
        self.assertEqual([event1, event2], reader3._events)

        composite1.end()
        self.assertTrue(reader1._ended)
        self.assertTrue(reader2._ended)
        self.assertTrue(reader3._ended)

    def test_copyFrom(self):
        """
        composite1
            |- composite2
            |      |- reader1
            |      |- reader2
            |- reader3
        """
        dest_composite1 = EventReaderComposite()
        dest_composite2 = EventReaderComposite()
        dest_reader1 = MockReader()
        dest_reader2 = MockReader()
        dest_reader3 = MockReader()
        dest_composite1.add(dest_composite2)
        dest_composite2.add(dest_reader1)
        dest_composite2.add(dest_reader2)
        dest_composite1.add(dest_reader3)

        src_composite1 = EventReaderComposite()
        src_composite2 = EventReaderComposite()
        src_reader1 = MockReader()
        src_reader2 = MockReader()
        src_reader3 = MockReader()
        src_composite1.add(src_composite2)
        src_composite2.add(src_reader1)
        src_composite2.add(src_reader2)
        src_composite1.add(src_reader3)

        dest_composite1.copyFrom(src_composite1)

        self.assertIs(src_reader1, dest_reader1._copy)
        self.assertIs(src_reader2, dest_reader2._copy)
        self.assertIs(src_reader3, dest_reader3._copy)

##____________________________________________________________________________||
