""" plan_learning.py 
    - This module contain the procedure used for learning plans from experience.
Copyright (C) 2016 Stephan Chang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program, located in the root of this repository.
If not, see <http://www.gnu.org/licenses/>.
"""
#!/usr/bin/python

import pdb
import planning
import sys
import random


def main(args):
    verbose = '-v' in args
    n_arg = '-n' in args

    try:
        i = 1 + int(verbose)
        examples_file = args[i]
        domain_name = args[i+1]
    except:
        print "usage: {cmd} [-v] examples_file"\
            " domain_name".format(cmd=args[0])
        return

    examples = []
    print "Parsing examples..."
    with open(examples_file) as f:
        line = f.readline().replace('\n', '')
        while line:
            triple = line.split('|')
            example = (triple[0], triple[1], triple[2])
            examples.append(example)
            line = f.readline().replace('\n', '')
    print "Done reading {n_examples} training examples!".format(n_examples=len(examples))

    if not f.closed:
        print "Warning: file stream is still open."

    if n_arg:
        n_examples = int(args[i+3])
    else:
        n_examples = len(examples)

    print "Creating domain..."
    domain = planning.Domain(domain_name)

#    random.shuffle(examples)

    for i in range(n_examples):
        preconditions = examples[i][0].split(',')
        operators = examples[i][1].split(',')
        effects = examples[i][2].split(',')

        domain.add_all_predicates(preconditions)
        domain.add_all_predicates(effects)
        domain.add_actions(operators, preconditions, effects)

    print "Done!"
    if verbose:
        print str(domain)
    else:
        print "Outputting to file..."
        output_file_name = "{domain_name}.pddl".format(domain_name=domain_name)
        with open(output_file_name, 'w') as f:
            f.write(str(domain))
        print "Done!"


if __name__ == '__main__':
    main(sys.argv)
