from twisted.trial.unittest import TestCase
from stupiphany.twistedspace.server.object_store import ObjectStore, ObjectMatcher

class ObjectStoreTest(TestCase):
    def test_creation(self):
        os = ObjectStore()
        self.assertEqual(0, os.size())

    def test_put_value(self):
        os = ObjectStore()
        os.put({'a': 1})

        self.assertEqual(1, os.size())

    def test_get_value_with_exact_match(self):
        os = ObjectStore([{'a': 1}, {'b': 5, 'c': 6}])

        self.assertEqual({'a': 1}, os.get({'a': 1}))

    def test_get_value_with_no_match(self):
        os = ObjectStore([{'a': 1}, {'b': 5, 'c': 6}])

        self.assertEqual(None, os.get({'a': 5}))

    def test_get_value_with_match(self):
        os = ObjectStore([{'a': 1}, {'b': 5, 'c': 6}])

        self.assertEqual({'b': 5, 'c': 6}, os.get({'b': 5}))

    def test_get_removes_matched_value(self):
        os = ObjectStore([{'a': 1}, {'b': 5, 'c': 6}])

        self.assertEqual({'b': 5, 'c': 6}, os.get({'b': 5}))
        self.assertEqual(1, os.size())

class ObjectMatcherTest(TestCase):
    def test_creation(self):
        om = ObjectMatcher({})
        self.assertTrue(om.matches({}))

    def test_no_matching_empty_set(self):
        om = ObjectMatcher({})
        self.assertFalse(om.matches({'a': 1}))

    def test_empty_set_always_matches(self):
        om = ObjectMatcher({'a': 1, 'b': 2, 'c': 3})
        self.assertTrue(om.matches({}))

    def test_matches_exactly(self):
        om = ObjectMatcher({'a': 1})
        self.assertTrue(om.matches({'a': 1}))

    def test_matches_multiple_keys_exactly(self):
        om = ObjectMatcher({'a': 1, 'b': 2, 'c': 3})
        self.assertTrue(om.matches({'a': 1, 'b': 2, 'c': 3}))

    def test_matches_multiple_keys_out_of_order(self):
        om = ObjectMatcher({'a': 1, 'b': 2, 'c': 3})
        self.assertTrue(om.matches({'c': 3, 'b': 2, 'a': 1}))

    def test_matches_subset(self):
        om = ObjectMatcher({'a': 1, 'b': 2, 'c': 3})
        self.assertTrue(om.matches({'b': 2, 'a': 1}))

    def test_does_not_match_superset(self):
        om = ObjectMatcher({'b': 2, 'c': 3})
        self.assertFalse(om.matches({'a': 1, 'b': 2, 'c': 3}))

