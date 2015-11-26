#!/usr/bin/python

import unittest
import planning as p


class PredicateClassTest(unittest.TestCase):

    def test_predicate_creation(self):
        predicate = p.Predicate('on', 2)
        self.assertEqual(str(predicate), '(on ?x0 ?x1)')

    def test_predicate_parsing_double(self):
        predicate_str = '(on a b)'
        predicate = p.Predicate.parse(predicate_str)
        self.assertEqual(str(predicate), '(on ?x0 ?x1)')

    def test_predicate_parsing_single(self):
        predicate_str = '(location a)'
        predicate = p.Predicate.parse(predicate_str)
        self.assertEqual(str(predicate), '(location ?x0)')

    def test_predicate_parsing_triple(self):
        predicate_str = '(connected a b x)'
        predicate = p.Predicate.parse(predicate_str)
        self.assertEqual(str(predicate), '(connected ?x0 ?x1 ?x2)')

    def test_predicate_parse_grounded(self):
        predicate_str = '(connected a b x)'
        predicate = p.Predicate.parse_grounded(predicate_str)
        self.assertEqual(predicate.print_grounded(), '(connected a b x)')


class ActionClassTest(unittest.TestCase):

    def test_action_creation(self):
        action = p.Action('pick', 1)
        action.add_precondition(p.Predicate.parse_grounded('(block ?x0)'))
        action.add_precondition(p.Predicate.parse_grounded('(free ?x0)'))
        action.add_positive_effect(p.Predicate.parse_grounded('(holding ?x0)'))
        action.add_negative_effect(p.Predicate.parse_grounded('(free ?x0)'))
        # print str(action)

        self.assertEqual(str(action), """(:action pick
    :parameters (?x0)
    :precondition (and (block ?x0) (free ?x0))
    :effect (and (holding ?x0) (not (free ?x0))))""")


class DomainClassTest(unittest.TestCase):

    def test_domain_creation(self):
        domain = p.Domain('blocks-world')
        domain.predicates.append(p.Predicate('block', 1))
        domain.predicates.append(p.Predicate('free', 1))
        domain.predicates.append(p.Predicate('holding', 1))

        action = p.Action('move', 3)
        action.add_precondition(p.Predicate.parse_grounded('(block ?x0)'))
        action.add_precondition(p.Predicate.parse_grounded('(free ?x0)'))
        action.add_precondition(p.Predicate.parse_grounded('(free ?x1)'))
        action.add_precondition(p.Predicate.parse_grounded('(on ?x0 ?x1)'))
        action.add_positive_effect(p.Predicate.parse_grounded('(on ?x0 ?x2)'))
        action.add_positive_effect(p.Predicate.parse_grounded('(free ?x1)'))
        action.add_negative_effect(p.Predicate.parse_grounded('(on ?x0 ?x1)'))
        action.add_negative_effect(p.Predicate.parse_grounded('(free ?x2)'))
        domain.actions.append(action)

        # print str(domain)

        self.assertEqual(str(domain), """(define (domain blocks-world)
    (:predicates
        (block ?x0)
        (free ?x0)
        (holding ?x0))

    (:action move
    :parameters (?x0 ?x1 ?x2)
    :precondition (and (block ?x0) (free ?x0) (free ?x1) (on ?x0 ?x1))
    :effect (and (on ?x0 ?x2) (free ?x1) (not (on ?x0 ?x1)) (not (free ?x2))))
)""")

    def test_multiple_predicate_parsing(self):
        domain = p.Domain('blocks-world')
        domain.add_all_predicates(['(clear a)', '(clear b)', '(ontable a)',
                                   '(holding a)', '(on a b)', '(on b a)'])

        self.assertEqual(str(domain), """(define (domain blocks-world)
    (:predicates
        (clear ?x0)
        (ontable ?x0)
        (holding ?x0)
        (on ?x0 ?x1))
)""")

    def test_action_inference(self):
        example_action = "unstack(a b)"
        example_preconditions = ["(on a b)", "(clear a)"]
        example_effects = ["(clear b)", "(holding a)"]

        domain = p.Domain('blocksworld')
        domain.add_all_predicates(example_preconditions)
        domain.add_all_predicates(example_effects)
        domain.add_actions([example_action], example_preconditions,
                           example_effects)
        print str(domain)
        expected = """(define (domain blocksworld)
    (:predicates
        (on ?x0 ?x1)
        (clear ?x0)
        (holding ?x0))

    (:action unstack
    :parameters (?x0 ?x1)
    :precondition (and (on ?x0 ?x1) (clear ?x0))
    :effect (and (holding ?x0) (clear ?x1) """\
    """(not (on ?x0 ?x1)) (not (clear ?x0))))
)"""

        # print str(domain)

        self.assertEqual(str(domain), expected)


if __name__ == '__main__':
    unittest.main()
