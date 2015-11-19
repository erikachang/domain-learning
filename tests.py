import unittest
import representations


class PredicateClassTest(unittest.TestCase):

    def test_predicate_creation(self):
        predicate = representations.Predicate('on', 2)
        self.assertEqual(str(predicate), '(on ?x0 ?x1)')

    def test_predicate_parsing_double(self):
        predicate_str = 'on(a,b)'
        predicate = representations.Predicate.parse(predicate_str)
        self.assertEqual(str(predicate), '(on ?x0 ?x1)')

    def test_predicate_parsing_single(self):
        predicate_str = 'location(a)'
        predicate = representations.Predicate.parse(predicate_str)
        self.assertEqual(str(predicate), '(location ?x0)')

    def test_predicate_parsing_triple(self):
        predicate_str = 'connected(a,b,x)'
        predicate = representations.Predicate.parse(predicate_str)
        self.assertEqual(str(predicate), '(connected ?x0 ?x1 ?x2)')

    def test_predicate_parse_grounded(self):
        predicate_str = 'connected(a,b,x)'
        predicate = representations.Predicate.parse_grounded(predicate_str)
        self.assertEqual(predicate.print_grounded(), '(connected a b x)')


class ActionClassTest(unittest.TestCase):

    def test_action_creation(self):
        action = representations.Action('pick', 1)
        action.add_precondition('(block ?x0)')
        action.add_precondition('(free ?x0)')
        action.add_positive_effect('(holding ?x0)')
        action.add_negative_effect('(free ?x0)')
        # print str(action)

        self.assertEqual(str(action), """(:action pick
    :parameters (?x0)
    :precondition (and (block ?x0) (free ?x0) )
    :effect (and (holding ?x0) (not (free ?x0)) ))""")


class DomainClassTest(unittest.TestCase):

    def test_domain_creation(self):
        domain = representations.Domain('blocks-world')
        domain.predicates.append(representations.Predicate('block', 1))
        domain.predicates.append(representations.Predicate('free', 1))
        domain.predicates.append(representations.Predicate('holding', 1))

        action = representations.Action('move', 3)
        action.add_precondition('(block ?x0)')
        action.add_precondition('(free ?x0)')
        action.add_precondition('(free ?x1)')
        action.add_precondition('(on ?x0 ?x1)')
        action.add_positive_effect('(on ?x0 ?x2)')
        action.add_positive_effect('(free ?x1)')
        action.add_negative_effect('(on ?x0 ?x1)')
        action.add_negative_effect('(free ?x2)')
        domain.actions.append(action)

        # print str(domain)

        self.assertEqual(str(domain), """(define (domain blocks-world)
    (:predicates
        (block ?x0)
        (free ?x0)
        (holding ?x0)
        )

    (:action move
    :parameters (?x0 ?x1 ?x2)
    :precondition (and (block ?x0) (free ?x0) (free ?x1) (on ?x0 ?x1) )
    :effect (and (on ?x0 ?x2) (free ?x1) (not (on ?x0 ?x1)) (not (free ?x2)) ))

    )""")

    def test_multiple_predicate_parsing(self):
        domain = representations.Domain('blocks-world')
        domain.add_all_predicates(['clear(a)', 'clear(b)', 'ontable(a)',
                                   'holding(a)', 'on(a,b)', 'on(b,a)'])
        
        self.assertEqual(str(domain), """(define (domain blocks-world)
    (:predicates
        (clear ?x0)
        (ontable ?x0)
        (holding ?x0)
        (on ?x0 ?x1)
        )

    )""")


if __name__ == '__main__':
    unittest.main()
