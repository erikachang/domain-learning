import pdb


class Domain():

    def __init__(self, domain_name):
        self.name = domain_name
        self.predicates = []
        self.actions = []

    def add_all_predicates(self, predicate_list):
        """ Add a list of predicates of the form p(a,b)
        """
        for p in predicate_list:
            self.add_predicate(p)

    def add_predicate(self, predicate_str):
        """ Parse the predicate in the form p(a,b). Add it if it doesn't already exist.
        """
        predicate = Predicate.parse(predicate_str)
        existent = next((x for x in self.predicates
                         if x.predicate == predicate.predicate),
                        None)
        if not existent:
            self.predicates.append(predicate)

    def add_actions(self, operators, preconditions, effects):
        for o in operators:
            action = Action.parse(o, preconditions, effects)
            existent = next((x for x in self.actions
                             if x.name == action.name),
                            None)
            if not existent:
                self.actions.append(action)
            else:
                existent.merge(action)

    def __str__(self):
        """ Print the domain definition in PDDL
        """
        string = ['(define', ' ', '(domain ', self.name, ')', '\n',
                  '    ', '(:predicates', '\n        ']
        for p in self.predicates:
            string += [str(p), '\n        ']
        string += [')', '\n\n    ']
        for a in self.actions:
            string += [str(a), '\n\n    ']
        string += ')'
        return ''.join(string)


class Predicate():
    def __init__(self, predicate, arity):
        self.predicate = predicate
        self.arity = arity
        self.terms = []
        for i in range(0, self.arity):
            # Add this to a predicate
            self.terms.append(['?x' + str(i), None])

    def add_term(self, term):
        self.terms.append(term)

    def __str__(self):
        """ Print the unground predicate in PDDL format """
        string = ['(', self.predicate]
        for t in self.terms:
            string += ([' ', t[0]])
        string += ')'
        return ''.join(string)

    def print_grounded(self):
        """ Print the ground predicate in PDDL format """
        string = ['(', self.predicate]
        for t in self.terms:
            string += ([' ', t[1]])
        string += ')'
        return ''.join(string)

    @classmethod
    def parse_grounded(cls, predicate_str):
        trimmed_str = predicate_str.replace('(', '').replace(')', '')
        tokenized_str = trimmed_str.split(' ')
        predicate = tokenized_str[0]
        args = tokenized_str[1:]
        arity = len(args)
        instantiated_predicate = Predicate(predicate, arity)
        for i in range(0, arity):
            # Add this to a predicate
            instantiated_predicate.terms[i][1] = args[i]
        return instantiated_predicate

    @classmethod
    def parse(cls, predicate_str):
        trimmed_str = predicate_str.replace('(', '').replace(')', '')
        tokenized_str = trimmed_str.split(' ')
        predicate = tokenized_str[0]
        args = tokenized_str[1:]
        arity = len(args)
        instantiated_predicate = Predicate(predicate, arity)
        return instantiated_predicate


class Action():
    def __init__(self, action_name, n_args):
        self.name = action_name
        self.n_args = n_args
        self.parameters = []
        for i in range(n_args):
            self.parameters.append('?x' + str(i))
        self.preconditions = []
        self.effects_positive = []
        self.effects_negative = []
        self.remove_precondition_list = []
        self.remove_positive_effects_list = []
        self.remove_negative_effects_list = []

    def add_precondition(self, predicate):
        self.preconditions.append(predicate.print_grounded())

    def add_positive_effect(self, effect):
        self.effects_positive.append(effect.print_grounded())

    def add_negative_effect(self, effect):
        self.effects_negative.append(effect.print_grounded())

    def merge(self, action):
        """ Updates current action with new information
        """
        difference = set(self.preconditions) - set(action.preconditions)
        remove = set(self.preconditions) & difference
        self.remove_precondition_list = set(
            self.remove_precondition_list) | remove
        self.preconditions = list((set(self.preconditions)
                                   | set(action.preconditions))
                                  - set(self.remove_precondition_list))

        difference = set(self.effects_positive) - set(action.effects_positive)
        remove = set(self.effects_positive) & difference
        self.remove_positive_effects_list = set(
            self.remove_positive_effects_list) | remove
        self.effects_positive = list((set(self.effects_positive)
                                      | set(action.effects_positive))
                                     - set(self.remove_positive_effects_list))

        difference = set(self.effects_negative) - set(action.effects_negative)
        remove = set(self.effects_negative) & difference
        self.remove_negative_effects_list = set(
            self.remove_negative_effects_list) | remove
        self.effects_negative = list((set(self.effects_negative)
                                      | set(action.effects_negative))
                                     - set(self.remove_negative_effects_list))

        # self.effects_positive = list(set(self.effects_positive)
        #                              | set(action.effects_positive))
        # self.effects_negative = list(set(self.effects_negative)
        #                              | set(action.effects_negative))

    @classmethod
    def parse(cls, action_name, preconditions, effects):
        parameter_mapping = []
        action_str_tokenized = action_name.split('(')
        action_name = action_str_tokenized[0]
        args = action_str_tokenized[1].replace(')', '').split(' ')
        arity = len(args)
        action = Action(action_name, arity)

        for i in range(arity):
            parameter_mapping.append((args[i], action.parameters[i]))

        for p in preconditions:
            predicate = Predicate.parse_grounded(p)
            for i in range(len(predicate.terms)):
                has_correspondence = False
                for j in range(len(parameter_mapping)):
                    # If there is a mapping between parameter and precondition
                    if predicate.terms[i][1] == parameter_mapping[j][0]:
                        # Update precondition with parameter value
                        predicate.terms[i][1] = parameter_mapping[j][1]
                        has_correspondence = True
                        break
                # if not has_correspondence:
                #     variable_index = len(parameter_mapping)
                #     variable = '?x' + str(variable_index)
                #     parameter_mapping.append((predicate.terms[i][1], variable))
                #     predicate.terms[i][1] = variable
            if has_correspondence:
                action.add_precondition(predicate)

        state_intersection = set(preconditions) & set(effects)
        effects_positive = list(set(effects) - state_intersection)
        effects_negative = list(set(preconditions) - state_intersection)

        for ep in effects_positive:
            predicate = Predicate.parse_grounded(ep)
            for i in range(len(predicate.terms)):
                has_correspondence = False
                for j in range(len(parameter_mapping)):
                    # If there is a mapping between parameter and precondition
                    if predicate.terms[i][1] == parameter_mapping[j][0]:
                        # Update precondition with parameter value
                        predicate.terms[i][1] = parameter_mapping[j][1]
                        has_correspondence = True
                        break
                # if not has_correspondence:
                #     i = len(parameter_mapping)
                #     variable = '?x' + str(i)
                #     parameter_mapping.append((predicate.terms[i][1], variable))
                #     predicate.terms[i][1] = variable
            if has_correspondence:
                action.add_positive_effect(predicate)

        for ep in effects_negative:
            predicate = Predicate.parse_grounded(ep)
            for i in range(len(predicate.terms)):
                has_correspondence = False
                for j in range(len(parameter_mapping)):
                    # If there is a mapping between parameter and precondition
                    if predicate.terms[i][1] == parameter_mapping[j][0]:
                        # Update precondition with parameter value
                        predicate.terms[i][1] = parameter_mapping[j][1]
                        has_correspondence = True
                        break
                # if not has_correspondence:
                #     i = len(parameter_mapping)
                #     variable = '?x' + str(i)
                #     parameter_mapping.append((predicate.terms[i][1], variable))
                #     predicate.terms[i][1] = variable
            if has_correspondence:
                action.add_negative_effect(predicate)

        return action

    def __str__(self):
        """ Print the action in PDDL format """
        string = ['(:action', ' ', self.name, '\n', '    ',
                  ':parameters', ' ', '(']

        for i in range(len(self.parameters)):
            string += self.parameters[i]
            if i < (len(self.parameters) - 1):
                string += ' '

        string += [')', '\n', '    ', ':precondition', ' ', '(', 'and', ' ']

        for p in self.preconditions:
            string += (p)
            string += ' '

        string += [')', '\n', '    ', ':effect', ' ', '(', 'and', ' ']

        for e in self.effects_positive:
            string += (e)
            string += ' '

        for e in self.effects_negative:
            effect_negated = ['(not', ' ', e, ')']
            string += (effect_negated)
            string += ' '

        string += [')', ')']

        return ''.join(string)
