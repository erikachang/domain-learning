
if __name__ == '__main__':
    
    predicate = 'on(a,b)'

    instantiated = InstantiatedPredicate.parse(predicate)

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
