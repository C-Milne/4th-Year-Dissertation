import re
import sys
from Solver.model import Model
from Solver.search_queue import SearchQueue
from Internal_Representation.method import Method
from Internal_Representation.action import Action
from Internal_Representation.task import Task
from Internal_Representation.reg_parameter import RegParameter
from Internal_Representation.subtasks import Subtasks
from Internal_Representation.Object import Object
from Internal_Representation.problem_predicate import ProblemPredicate
from Internal_Representation.state import State
from Internal_Representation.Type import Type
from Internal_Representation.list_parameter import ListParameter
from Internal_Representation.effects import Effects
"""Space for importing heuristic functions"""
from Solver.Heuristics.Heuristic import Heuristic
from Solver.Heuristics.breadth_first_by_actions import BreadthFirstActions
from Solver.Heuristics.breadth_first_by_operations import BreadthFirstOperations
from Solver.Heuristics.breadth_first_by_operations_with_pruning import BreadthFirstOperationsPruning
"""Space for importing parameter selection functions"""
from Solver.Parameter_Selection.ParameterSelector import ParameterSelector
from Solver.Parameter_Selection.All_Parameters import AllParameters
from Solver.Parameter_Selection.Requirement_Selection import RequirementSelection
"""Importing from sys modules"""
Precondition = sys.modules['Internal_Representation.precondition'].Precondition
ForallCondition = sys.modules['Internal_Representation.conditions'].ForAllCondition


class Solver:
    def __init__(self, domain, problem):
        self.domain = domain
        self.problem = problem

        self.has_goal_conditions = self.problem.has_goal_conditions()

        self.search_models = SearchQueue()
        heuristic = BreadthFirstOperationsPruning(self.domain, self.problem, self, self.search_models)
        self.search_models.add_heuristic(heuristic)
        self.parameter_selector = RequirementSelection(self)
        self.task_expansion_given_param_check = True

    def set_heuristic(self, heuristic):
        if type(heuristic) == type:
            heuristic = heuristic(self.domain, self.problem, self, self.search_models)
        assert isinstance(heuristic, Heuristic)
        self.search_models.add_heuristic(heuristic)

    def set_parameter_selector(self, selector):
        if type(selector) == type:
            selector = selector(self)
        assert isinstance(selector, ParameterSelector)
        self.parameter_selector = selector

    def solve(self):
        self.parameter_selector.presolving_processing(self.domain, self.problem)
        self.search_models.heuristic.presolving_processing()
        task_counter = 0
        subtasks = self.problem.subtasks.get_tasks()
        list_subT = []
        num_tasks = len(subtasks)
        while task_counter < num_tasks:
            subT = subtasks[task_counter]
            if subT == "and" or subT == "or":
                del subtasks[task_counter]
                num_tasks -= 1
                continue

            print("Subtask:", task_counter, "-", subT.get_name() + str([p.name for p in subT.parameters]))

            # Create initial search model
            param_dict = self.__generate_param_dict(subT.task, subT.parameters)
            subT.add_given_parameters(param_dict)
            list_subT.append(subT)
            task_counter += 1

        if len(list_subT) == 1:
            waiting_subT = []
        else:
            waiting_subT = list_subT[1:]
            list_subT = [list_subT[0]]

        initial_model = Model(State.reproduce(self.problem.initial_state), list_subT, self.problem, waiting_subT)

        self.search_models.add(initial_model)

        return self.__search()

    def __search(self, step_control=False):
        """:parameter   - step_control  - If True, then loop will only execute once"""
        while True:
            # New model to operate on
            search_model = self.search_models.pop()
            if search_model is None:
                return None

            # Check what needs to be done to this model
            next_modifier = search_model.get_next_modifier()
            assert type(next_modifier) == Subtasks.Subtask

            if type(next_modifier.task) == Task:
                self.__expand_task(next_modifier, search_model)
            elif type(next_modifier.task) == Method:
                self.__expand_method(next_modifier, search_model)
            elif type(next_modifier.task) == Action:
                self.__expand_action(next_modifier, search_model)
            else:
                raise NotImplementedError

            # Loop exit conditions
            if self.search_models.get_num_search_models() == 0 and self.search_models.get_num_completed_models() == 0:
                return None
            elif step_control:
                break
            elif self.search_models.get_num_completed_models() > 0:
                for m in self.search_models.get_completed_models():
                    eval = self.problem.evaluate_goal(m)
                    if eval is None or eval == True:
                        m.num_models_used = Model.model_counter
                        return m
                self.search_models.clear_completed_models()

    def __expand_task(self, subtask: Subtasks.Subtask, search_model: Model):
        if len(subtask.task.tasks) != 0:
            for new_task in subtask.task.tasks:
                self.__expand_task(Subtasks.Subtask(new_task, self.reproduce_parameter_list(subtask.parameters)),
                                   self.reproduce_model(search_model))
        else:
            # For each method, create a new search model
            for method in subtask.task.methods:
                # Check parameters for new_model
                # Is all the required parameters present or do some need to be chosen
                parameters = {}
                i = 0
                for k in subtask.given_params.keys():
                    parameters[method.task['params'][i].name] = subtask.given_params[k]
                    i += 1

                # Check if the given parameters satisfy preconditions that only use the given parameters
                if self.task_expansion_given_param_check and not method.evaluate_preconditions_conditions_given_params(parameters, search_model, self.problem):
                    continue

                param_options = self.parameter_selector.get_potential_parameters(method, parameters, search_model)

                for param_option in param_options:
                    subT = Subtasks.Subtask(method, method.parameters)
                    subT.add_given_parameters(param_option)
                    # Create new model and add to search_models
                    new_model = self.reproduce_model(search_model, [subT] + search_model.search_modifiers)
                    new_model.add_operation(subtask.task, subtask.given_params)
                    self.search_models.add(new_model)

    def __expand_method(self, subtask: Subtasks.Subtask, search_model: Model):
        # Add actions to search model - with parameters
        i = 0
        if subtask.task.subtasks is None:
            search_model.add_operation(subtask.task, subtask.given_params)
            self.search_models.add(search_model)
            return
        for mod in subtask.task.subtasks.tasks:
            try:
                assert type(mod.task) == Action or type(mod.task) == Task
            except:
                if mod.task is None:
                    continue

            mod = Subtasks.Subtask(mod.task, mod.parameters)

            # Check parameter count
            parameters = {}
            param_keys = [p.name for p in mod.parameters]
            action_keys = [p.name for p in mod.task.parameters]
            if len(action_keys) > 0:
                for j in range(len(action_keys)):
                    try:
                        parameters[action_keys[j]] = subtask.given_params[param_keys[j]]
                    except IndexError:
                        pass
            else:
                for j in range(len(param_keys)):
                    parameters[param_keys[j]] = subtask.given_params[param_keys[j]]

            mod.add_given_parameters(parameters)

            # Add mod to search_model
            search_model.insert_modifier(mod, i)
            i += 1
        search_model.add_operation(subtask.task, subtask.given_params)
        self.search_models.add(search_model)

    def __expand_action(self, subtask: Subtasks.Subtask, search_model: Model):
        assert type(subtask) == Subtasks.Subtask and type(subtask.task) == Action

        # Check if all the required parameters are given
        comparison_result = self.parameter_selector.compare_parameters(subtask.task, subtask.given_params)

        assert comparison_result[0] == True

        # Check preconditions
        if not subtask.evaluate_preconditions(search_model, subtask.given_params, self.problem):
            return

        if not subtask.task.effects is None:
            for eff in subtask.task.effects.effects:

                if type(eff) == Effects.Effect:
                    param_list = []
                    for i in eff.parameters:
                        param_list.append(subtask.given_params[i])

                    if eff.negated:
                        # Predicate needs to be removed
                        search_model.current_state.remove_element(eff.predicate, param_list)
                    else:
                        # Predicate needs to be added
                        new_predicate = ProblemPredicate(eff.predicate, param_list)
                        search_model.current_state.add_element(new_predicate)
                elif type(eff) == Effects.ForAllEffect:
                    # Get parameters
                    assert type(eff.precondition.head) == ForallCondition
                    obs = eff.precondition.head.get_satisfying_objects(subtask.given_params, search_model, self.problem)
                    forall_var_name = eff.precondition.head.selected_variable
                    # Iterate over found parameters
                    for o in obs:
                        for e in eff.effects:
                            param_list = []
                            for i in e.parameters:
                                if i.name == forall_var_name:
                                    param_list.append(o)
                                else:
                                    param_list.append(subtask.given_params[i.name])

                            if eff.negated:
                                # Predicate needs to be removed
                                search_model.current_state.remove_element(e.predicate, param_list)
                            else:
                                # Predicate needs to be added
                                new_predicate = ProblemPredicate(e.predicate, param_list)
                                search_model.current_state.add_element(new_predicate)
                else:
                    raise NotImplementedError

        search_model.add_operation(subtask.task, subtask.given_params)
        self.search_models.add(search_model)

    def __generate_param_dict(self, modifier, params):
        assert type(modifier) == Method or type(modifier) == Action or type(modifier) == Task
        # Check number of params is the amount expected
        if type(params) == ListParameter:
            len_params = 1
        else:
            len_params = len(params)

        if type(params) == ListParameter:
            param_dict = {modifier.get_parameters()[0].name: params}
        else:
            # Map params to self.parameters
            i = 0
            param_dict = {}
            while i < modifier.get_number_parameters():
                param_name = modifier.parameters[i]
                if type(param_name) == RegParameter:
                    param_name = param_name.name
                try:
                    param_dict[param_name] = params[i]
                except:
                    pass
                i += 1
        return param_dict

    def compute_derived_predicates(self, search_model: Model):
        # Remove derived predicates from search model state

        # Check derived predicates
        for i in self.domain.derived_predicates:
            pred = self.domain.derived_predicates[i]
            assert len(pred.conditions) == len(pred.cond_requirements)
            found_predicates = []   # Used to make sure only one of each combination of variables is selected

            for j in range(len(pred.conditions)):
                # Choose variables
                found_params = self.__find_satisfying_parameters(search_model, pred.cond_requirements[j])
                for param_option in found_params:
                    # Evaluate predicate
                    result = pred.conditions[j].evaluate(param_option, search_model, self.problem)
                    if result and param_option not in found_predicates:
                        found_predicates.append(param_option)
                        obs = self.convert_param_dict_to_list(param_option, pred.parameters)
                        search_model.current_state.add_element(ProblemPredicate(pred, obs))

    @staticmethod
    def check_duplicate_values_dictionary(d: dict):
        """https://www.geeksforgeeks.org/python-find-keys-with-duplicate-values-in-dictionary/
        :returns True if a duplicate is present
        :returns False if there is no duplicates"""
        flipped = {}
        for key, value in d.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                return True
        return False

    @staticmethod
    def reproduce_dict(d: dict):
        return_dict = {}
        keys = list(d.keys())
        for k in keys:
            return_dict[k] = d[k]
        return return_dict

    @staticmethod
    def convert_param_dict_to_list(param_dict, parameters: list):
        return_list = []
        for i in parameters:
            return_list.append(param_dict[i.name])
        return return_list

    @staticmethod
    def reproduce_parameter_list(param_list):
        new_list = []
        for p in param_list:
            new_list.append(p)
        return new_list

    @staticmethod
    def reproduce_state(state):
        return State.reproduce(state)

    def reproduce_model(self, model, search_mods=None):
        if search_mods is None:
            new_model = Model(State.reproduce(model.current_state),
                  model.search_modifiers, self.problem, [])
        else:
            new_model = Model(State.reproduce(model.current_state),
                              search_mods, self.problem, [])

        i = 0
        for i in model.waiting_subtasks:
            new_model.waiting_subtasks.append(i)

        new_model.populate_actions_taken(Model.reproduce_actions_taken(model))
        new_model.populate_operations_taken(Model.reproduce_operations_list(model))
        return new_model

    def output(self, resulting_model: Model):
        assert type(resulting_model) == Model or resulting_model is None

        if not resulting_model is None:
            print("\nActions Taken:")
            for a in resulting_model.actions_taken:
                print(a)
            if len(resulting_model.actions_taken) == 0:
                print("No Actions")

            print("\nOperations Taken:")
            for a in resulting_model.operations_taken:
                print(a)

            # print("\nFinal State:")
            # print(resulting_model.current_state)

            print("\nSearch Models Created During Search: {}".format(Model.model_counter))
        else:
            print("plan not found")
