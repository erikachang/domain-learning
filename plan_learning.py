import domain as d

if __name__ == '__main__':
    f = open('training.txt')

    examples = []
    
    line = f.readline().replace('\n','')
    while line:
        triple = line.split('|')
        example = (triple[0], triple[1], triple[2])
        examples.append(example)
        line = f.readline().replace('\n','')

    f.close()

#    print examples

    domain_definition = d.Domain()

    for e in examples:
        preconditions = e[0].replace('[', '').replace(']', '').split(',')
        operators = e[1].replace('[', '').replace(']', '').split(',')
        effects = e[2].replace('[', '').replace(']', '').split(',')

        for p in preconditions:
            domain_definition.add_predicate(p)

        for e in effects:
            domain_definition.add_predicate(e)
            
        for o in operators:
            domain_definition.add_operator(o, preconditions, effects)
