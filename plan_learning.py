
class Predicate():
    def __init__(self, predicate, arity):
        self.predicate = predicate
        self.arity = arity
        self.terms = []

    def add_term(self, term):
        self.terms.append(term)

    def __str__(self):
        string = ['(', self.predicate]
        for t in self.terms:
            string += ([' ', t])
        string += ')'
        return ''.join(string)


class PredicateDefinition(Predicate):
    
    @classmethod
    def parse(cls, predicate_str):
        tokenized_str = predicate_str.split('(')
        predicate = tokenized_str[0]
        args = tokenized_str[1].replace(')','').split(',')
        arity = len(args)

        instantiated_predicate = Predicate(predicate, arity)
        
        for i in range(0, arity):
            # Add this to a predicate
            instantiated_predicate.add_term('?x' + str(i))

        return instantiated_predicate


class Action():
    def __init__(self, handle):
        self.operator = handle
        self.parameters = [] # TODO: Parse parameters
        self.preconditions = []
        self.positive_effects = []
        self.negative_effects = []

    def add_precondition(self, fluent):
        self.preconditions.append(fluent)

    def add_positive_effect(self, effect):
        self.positive_effects.append(effect)

    def add_negative_effect(self, effect):
        self.negative_effects.append(effect)


if __name__ == '__main__':
    
    predicate = 'on(a,b)'

    instantiated = Predicate.parse_predicate(predicate)

    print str(instantiated)
                
## example = ([on(a, b), on(b, c), on(c, table)], pick(a), [holding(a), on(b, c), on(c,table)])

## example_precondition = example[0]
## example_action = example[1]
## example_effects = example[2]

## actions = []
## predicates = []

## for example in example_precondition:
##     # Create predicates

## action = Action()

## for precondition in example_precondition:
##     action.add_precondition(precondition)

## for effect in example_effects:
##     action.add_positive_effects(effect)

## domain_str = '(define (domain learned)'
