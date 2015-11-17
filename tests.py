import unittest
from plan_learning import PredicateDefinition

class ExampleParsingTests(unittest.TestCase):

    def test_predicate_parsing_double(self):
        predicate_str = 'on(a,b)'
        predicate = PredicateDefinition.parse(predicate_str)
        self.assertEqual(str(predicate),'(on ?x0 ?x1)')

    def test_predicate_parsing_single(self):
        predicate_str = 'location(a)'
        predicate = PredicateDefinition.parse(predicate_str)
        self.assertEqual(str(predicate),'(location ?x0)')

    def test_predicate_parsing_triple(self):
        predicate_str = 'connected(a,b,x)'
        predicate = PredicateDefinition.parse(predicate_str)
        self.assertEqual(str(predicate),'(connected ?x0 ?x1 ?x2)')


if __name__ == '__main__':
    unittest.main()
