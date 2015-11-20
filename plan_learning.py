import pdb
import representations as r
import sys


if __name__ == '__main__':
    domain_name = sys.argv[1]
    f = open(domain_name)

    examples = []

    line = f.readline().replace('\n', '')
    while line:
        triple = line.split('|')
        example = (triple[0], triple[1], triple[2])
        examples.append(example)
        line = f.readline().replace('\n', '')

    f.close()

    domain = r.Domain(domain_name)

    for e in examples:
        preconditions = e[0].split(',')
        operators = e[1].split(',')
        effects = e[2].split(',')

        domain.add_all_predicates(preconditions)
        domain.add_all_predicates(effects)
        domain.add_actions(operators, preconditions, effects)

    print str(domain)
