import unittest
import domain

class PredicateClassTest(unittest.TestCase):

    def test_predicate_creation(self):
        predicate = domain.InstantiatedPredicate('on', 2)
        self.assertEqual(str(predicate), '(on ?x0 ?x1)')
    
    def test_predicate_parsing_double(self):
        predicate_str = 'on(a,b)'
        predicate = domain.InstantiatedPredicate.parse(predicate_str)
        self.assertEqual(str(predicate),'(on ?x0 ?x1)')

    def test_predicate_parsing_single(self):
        predicate_str = 'location(a)'
        predicate = domain.InstantiatedPredicate.parse(predicate_str)
        self.assertEqual(str(predicate),'(location ?x0)')

    def test_predicate_parsing_triple(self):
        predicate_str = 'connected(a,b,x)'
        predicate = domain.InstantiatedPredicate.parse(predicate_str)
        self.assertEqual(str(predicate),'(connected ?x0 ?x1 ?x2)')


class ActionClassTest(unittest.TestCase):

    def test_action_creation(self):
        action = domain.Action('pick')
        action.add_parameter('?b')
        action.add_precondition('(block ?b)')
        action.add_precondition('(free ?b)')
        action.add_positive_effect('(holding ?b)')
        action.add_negative_effect('(free ?b)')
        # print str(action)

        self.assertEqual(str(action), """(:action pick
	:parameters (?b)
	:precondition (and (block ?b) (free ?b) )
	:effect (and (holding ?b) (not (free ?b)) ))""")
        
        
class DomainClassTest(unittest.TestCase):

    def test_domain_creation(self):
        domain_specification = domain.Domain()
        domain_specification.predicates.append(domain.Predicate('block', 1))
        domain_specification.predicates.append(domain.Predicate('free', 1))
        domain_specification.predicates.append(domain.Predicate('holding', 1))

        action = domain.Action('move')
        action.add_parameter('?block')
        action.add_parameter('?from')
        action.add_parameter('?to')
        action.add_precondition('(block ?block)')
        action.add_precondition('(free ?block)')
        action.add_precondition('(free ?to)')
        action.add_precondition('(on ?block ?from)')
        action.add_positive_effect('(on ?block ?to)')
        action.add_positive_effect('(free ?from)')
        action.add_negative_effect('(on ?block ?from)')
        action.add_negative_effect('(free ?to)')
        domain_specification.actions.append(action)

        print str(domain_specification)
        
        self.assertEqual(str(domain_specification), """(define (domain learned)
	(:predicates
		(block ?x0)
		(free ?x0)
		(holding ?x0)
		)

	(:action move
	:parameters (?block ?from ?to)
	:precondition (and (block ?block) (free ?block) (free ?to) (on ?block ?from) )
	:effect (and (on ?block ?to) (free ?from) (not (on ?block ?from)) (not (free ?to)) ))

	)""")
                        
if __name__ == '__main__':
    unittest.main()
